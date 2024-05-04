import os
import csv as csvmod
from textwrap import indent, wrap
from typing import Literal
from termcolor import colored
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


# Ugly terminal output functions
def print_single_case(case: GradedTestCase, color: Literal["red", "yellow", "green"]):

    try:
        terminal_width = max(60, os.get_terminal_size().columns)
    except OSError:
        terminal_width = 80

    response_wrapped = "\n".join(
        wrap(f"Response: {case.response}", terminal_width - 10)
    )
    question_wrapped = "\n".join(
        wrap(f"{case.id}: {case.question}\n", terminal_width - 10)
    )

    print(colored(question_wrapped, color, attrs=["bold"]))
    print(indent(response_wrapped, "\t"))
    for grade in case.grades:
        if grade.score >= 1:
            continue
        else:
            grader_color = color
        grade_wrapped = "\n".join(
            wrap(
                f"{grade.grader} {'PASS' if grade.score >= 1.0 else 'FAIL'}: {grade.reason}",
                terminal_width - 10,
            )
        )
        print(colored(grade_wrapped, grader_color))
    print("---------------------------------------------")


def get_failures_and_warnings(
    test_cases: list[GradedTestCase], scoring_rules: list[ScoringRule]
):

    failures = []
    warnings = []

    # Now we need to loop through the rules defined in the scoring rules and
    # determine which cases need to be considered failures vs warnings.
    # This is ugly because it needs to support "any" and "all" scoring.
    for test_case in test_cases:
        for scoring_rule in scoring_rules:
            # determine if the test case has grades for all of the graders for this rule
            eligible = all(
                [
                    any(map(lambda x: x.grader == grader, test_case.grades))
                    for grader in scoring_rule.graders
                ]
            )
            if eligible and scoring_rule.mode == "allow_any_pass":
                all_fail = all(
                    [
                        all(
                            map(
                                lambda x: x.grader != grader or x.score < 1,
                                test_case.grades,
                            )
                        )
                        for grader in scoring_rule.graders
                    ]
                )
                if all_fail:
                    if scoring_rule.level == "fail":
                        failures.append(test_case)
                    elif scoring_rule.level == "warn":
                        warnings.append(test_case)
            elif eligible and scoring_rule.mode == "require_all_pass":
                any_fail = any(
                    [
                        any(
                            map(
                                lambda x: x.grader == grader and x.score < 1,
                                test_case.grades,
                            )
                        )
                        for grader in scoring_rule.graders
                    ]
                )
                if any_fail:
                    if scoring_rule.level == "fail":
                        failures.append(test_case)
                    elif scoring_rule.level == "warn":
                        warnings.append(test_case)

    return failures, warnings
