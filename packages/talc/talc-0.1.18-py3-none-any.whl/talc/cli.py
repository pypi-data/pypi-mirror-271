import datetime
import os
import csv as csvmod
import time
from typing import Literal
import click
import random
from pdfminer.high_level import extract_text
from talc.utils.cli.io import print_single_case, get_failures_and_warnings
from talc.evals import (
    Document,
    EvalsClient,
    TestCaseWithRubric,
    RunInfo,
    GradedTestCase,
)
from talc.grading import (
    GraderConfig,
    FactualityGraderConfig,
    GradingSet,
    TestCaseResponse,
    ScoringRule,
    GradingPipeline,
)
from talc.utils.grading.defaults import DEFAULT_GRADER_CONFIG


talc_api_key: str | None = os.getenv("TALC_API_KEY", None)
talc_base_url: str | None = os.getenv(
    "TALC_BASE_URL", "http://evals-webserver-webapp.azurewebsites.net"
)


def poll_results(
    client: EvalsClient,
    print_passed: bool,
    out_file: str | None,
    scoring_rules: list[ScoringRule],
):
    while True:
        run_info = client.get_results()
        print(f"Progress: {run_info.completion_progress * 100}%")
        if run_info.completion_progress >= 1:
            print("\n============================================================")
            print("Grading complete.")
            for key in run_info.grades.keys():
                print(f"{key}: {run_info.grades[key] * 100}%")

            print("============================================================\n")

            assert run_info.test_cases is not None

            failures, warnings = get_failures_and_warnings(
                run_info.test_cases, scoring_rules
            )

            passed = [case for case in run_info.test_cases if case not in failures and case not in warnings]

            if out_file is not None:
                with open(out_file, "w", newline="") as csvfile:
                    writer = csvmod.writer(csvfile)
                    writer.writerow(
                        [
                            "id",
                            "question",
                            "expected_answer",
                            "result",
                            "failure",
                            "warning",
                            "grades",
                        ]
                    )
                    for case in run_info.test_cases:
                        writer.writerow(
                            [
                                case.id,
                                case.question,
                                case.expected_response,
                                case.response,
                                True if case in failures else False,
                                True if case in warnings else False,
                                case.grades,
                            ]
                        )

            if print_passed and len(passed) > 0:
                print("=================PASSED=================")
                for case in passed:
                    print_single_case(case, "green")
            if len(warnings) > 0:
                print("=================WARNINGS=================")
                for warning in warnings:
                    print_single_case(warning, "yellow")
            if len(failures) > 0:
                print("=================FAILURES=================")
                for failure in failures:
                    print_single_case(failure, "red")
            if len(failures) > 0:
                return 1
            else:
                return 0

        time.sleep(2)


@click.group()
def evals():
    pass


@evals.command()
@click.option("--count", default=0, help="Number of cases to sample (0 for all).")
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option("--dataset", prompt="Dataset ID", help="The ID of the dataset to load.")
@click.option(
    "--out_file",
    default=None,
    help="Path to CSV file to save results to.",
    required=False,
)
def get_dataset(count: int, dataset: str, api_key: str, out_file: str) -> None:
    """Download or pretty print a test dataset from the server."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url)
    data = client.get_dataset(dataset)

    if count == 0:
        count = len(dataset)

    random.shuffle(data)

    if out_file is not None:
        with open(out_file, "w", newline="") as csvfile:
            writer = csvmod.writer(csvfile)
            writer.writerow(["id", "question", "expected_answer"])
            for case in data[:count]:
                writer.writerow([case.id, case.question, case.expected_response])

    for case in data[:count]:
        print(case.question)


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option(
    "--in_file",
    prompt="Results CSV path",
    help="Path to CSV file to load results from. Columns should be 'id', 'result'. Header row is required and case sensitive.",
)
@click.option("--print_passed", is_flag=True, help="Print the passed test cases.")
@click.option("--out_file", default=None, help="Optionally save output as CSV.")
@click.option(
    "--config",
    default="all_passed",
    help="The name of the grader configuration to use.",
)
def eval(
    api_key: str,
    in_file: str,
    print_passed: bool,
    out_file: str,
    config: str,
):
    """Grade a test run from a CSV. Columns 'id' and 'result' are required, other columns will be ignored. CSV should have a header row."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url)

    with open(in_file, newline="") as csvfile:
        reader = csvmod.DictReader(csvfile)

        results = [
            TestCaseResponse(id=row["id"], response=row["result"]) for row in reader
        ]

    if config.endswith(".json"):
        loaded_config = GradingPipeline.parse_file(config)
    else:
        loaded_config = DEFAULT_GRADER_CONFIG

    grading_set = GradingSet(
        responses=results,
        pipeline=loaded_config,  # type: ignore
    )
    print("Grading " + str(len(results)) + " test cases.")
    run_info = client.start_run()
    client.submit_responses(grading_set)
    print("Submitted results. Beginning grading for run ID: " + run_info.id)

    res = poll_results(
        client, print_passed, out_file, loaded_config.scoring_rules
    )
    exit(res)


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option("--run_id", prompt="Run ID", help="The ID of the run to get results for.")
@click.option("--print_passed", is_flag=True, help="Print the passed test cases.")
def get_results(api_key: str, run_id: str, print_passed: bool):
    """Get the grades for a test run."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url, run_id)

    res = poll_results(
        client, print_passed, None, DEFAULT_GRADER_CONFIG.scoring_rules
    )

    exit(res)


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option(
    "--csv",
    prompt="CSV path",
    help="Path to CSV file to upload. Column headers should be 'question' and 'expected_answer'. An optional source_text column can be included as well.",
)
@click.option("--name", prompt="Dataset name", help="The name of the dataset.")
def upload_manual_testset(api_key: str, csv: str, name: str):
    """Add a new dataset to the server."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url)

    with open(csv, newline="") as csvfile:
        reader = csvmod.DictReader(csvfile)

        try:
            dataset = [
                TestCaseWithRubric(
                    question=row["question"],
                    expected_response=row["expected_answer"],
                    scenario_data={},
                    id=None,
                    source_content=(
                        [row["source_text"]] if "source_text" in row else []
                    ),
                )
                for row in reader
            ]
        except KeyError:
            raise click.UsageError(
                "CSV file must have columns 'question' and 'expected_answer'. A header is required. An optional source_text column can be included."
            )

    dataset_id = client.upload_dataset(name, dataset)
    print(f"Dataset created with ID: {dataset_id}")


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option(
    "--in_file",
    prompt="Input CSV path",
    help="Path to CSV file to upload. Columns should be 'question', 'expected_answer' and 'user_answer'. An optional source_text column can be included as well.",
)
@click.option(
    "--name",
    help="The name of the dataset.",
    default="Temp Dataset",
    required=False,
)
@click.option(
    "--out_file",
    help="Name of the output file",
    required=False,
)
def upload_and_grade(api_key: str, in_file: str, name: str, out_file: str | None):
    """Upload a CSV with questions, reference answers, and user answers. Grade the user answers and return the grade. Column names must be 'question', 'expected_answer', and 'user_answer'."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url)

    with open(in_file, newline="") as csvfile:
        reader = csvmod.DictReader(csvfile)

        rows = [row for row in reader]

        assert "question" in rows[0]
        assert "expected_answer" in rows[0]
        assert "user_answer" in rows[0]

    dataset = [
        TestCaseWithRubric(
            question=row["question"],
            expected_response=row["expected_answer"],
            scenario_data={},
            id=None,
            source_content=([row["source_text"]] if "source_text" in row else []),
        )
        for row in rows
    ]

    dataset = client.upload_dataset(name, dataset)

    # Download the dataset to get the IDs
    data = client.get_dataset(dataset.id)

    # Map the IDs to the actual responses using the questions as a key

    id_map = {case.question: case.id for case in data}

    results = [
        TestCaseResponse(
            id=id_map[row["question"]],
            response=row["user_answer"] if "user_answer" in row else "",
        )
        for row in rows
    ]

    # Create a run and submit the results
    run_info = client.start_run()

    # MAX TODO: Expose this config to the user
    grading_set = GradingSet(
        responses=results,
        pipeline=DEFAULT_GRADER_CONFIG,
    )
    client.submit_responses(grading_set)
    print("Submitted results. Beginning grading for run ID: " + run_info.id)

    res = poll_results(
        client, True, out_file, DEFAULT_GRADER_CONFIG.scoring_rules
    )

    exit(res)


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option(
    "--in_file",
    prompt="Input folder, single file path, or URL.",
    help="Input folder, single file path, or URL. Multiple allowed.",
    multiple=True,
)
@click.option("--out_file", default=None, help="Path to save the output to.")
@click.option("--dataset_name", default=None, help="The name of the dataset.")
@click.option(
    "--sampling_mode",
    help="The sampling mode to use.",
    type=click.Choice(["main_file", "all_files", "random", "ranked"]),
    default="all_files",
)
@click.option(
    "--generation_mode",
    help="The generation modes to use. Basic types are 'simple', 'complex', 'sweep', and 'hallucination' but others may be supported in custom configurations.",
    default=["sweep"],
    multiple=True,
)
@click.option(
    "--question_limit",
    required=True,
    help="The number of questions to generate. Use 0 to not set a limit.",
)
def generate(
    api_key: str,
    in_file: list[str],
    out_file: str | None,
    dataset_name: str | None,
    sampling_mode: Literal["main_file", "all_files", "random", "ranked"],
    generation_mode: list[
        Literal["simple"]
        | Literal["complex"]
        | Literal["sweep"]
        | Literal["hallucination"]
        | str
    ],
    question_limit: int,
):
    """Generate a dataset from a set of documents."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    if dataset_name is None:
        dataset_name = "questions_" + datetime.datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S"
        )

    if out_file is None:
        out_file = dataset_name + ".csv"

    client = EvalsClient(api_key, talc_base_url)

    documents: list[Document] = []

    # Figure out what kind of document each file is, and load it into a list of Document objects
    # If it's a URL, send the URL and the server will load it (might want to make this local in the future)
    # If it's a directory, load all the markdown files in the directory
    # If it's a file, load the file
    for f in in_file:
        if f.startswith("http") or f.startswith("https"):
            documents.append(Document(url=f, title=f))
        elif os.path.isdir(f):
            for root, _, files in os.walk(f):
                for path in files:
                    if path.endswith(".md"):
                        with open(os.path.join(root, path), "r") as f:
                            documents.append(Document(content=f.read(), title=f.name))
                    elif path.endswith(".pdf"):
                        documents.append(
                            Document(content=extract_text(os.path.join(root, path)))
                        )
                    else:
                        print(
                            f"Skipping file with unknown extension {path} in directory {root}."
                        )
        elif os.path.isfile(f):
            if f.endswith(".pdf"):
                documents.append(Document(content=extract_text(f), title=f))
            elif f.endswith(".md"):
                with open(f, "r") as f:
                    documents.append(Document(content=f.read(), title=f.name))
            else:
                raise click.UsageError(
                    "Unsupported file type. Only .md and .pdf files are supported."
                )

    dataset_job = client.start_generate_dataset(
        dataset_name,
        documents,
        sampling_mode,
        generation_mode,
        sample_count=question_limit,
    )

    while True:
        dataset_job = client.get_dataset_creation_job(dataset_job.id)
        print("Status: " + dataset_job.status)
        if dataset_job.status == "COMPLETE":
            break
        if dataset_job.status == "ERROR":
            print("Generation failed.")
            exit(1)
        time.sleep(2)

    dataset = client.get_dataset(dataset_job.dataset_id)

    with open(out_file, "w", newline="") as csvfile:
        writer = csvmod.writer(csvfile)
        writer.writerow(["id", "question", "expected_answer"])
        for case in dataset:
            writer.writerow([case.id, case.question, case.expected_response])

    print(f"Dataset created with ID: {dataset_job.dataset_id}")
    print(f"Dataset written to {out_file}")


def main():
    evals()
