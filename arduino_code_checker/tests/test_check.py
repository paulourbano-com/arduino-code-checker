import os
import pandas as pd
from arduino_code_checker.src.code_check import (
    compare_solution_assignment,
    compare_set_inner_func_calls,
    batch_compare,
)


def test_check_01():
    result = compare_solution_assignment(
        os.path.join(os.path.dirname(__file__), "solution_01", "solution.ino"),
        os.path.join(os.path.dirname(__file__), "assigments_01", "assigment.ino"),
    )

    assert sum(result.values()) / len(result) == 100.0


def test_non_existant_file():
    result = compare_solution_assignment(
        os.path.join(os.path.dirname(__file__), "solution_01", "solution.ino"),
        os.path.join(os.path.dirname(__file__), "assigments_01", "not_there.ino"),
    )

    assert sum(result.values()) / len(result) == 0.0


def test_parse_error():
    result = compare_solution_assignment(
        os.path.join(os.path.dirname(__file__), "solution_01", "solution.ino"),
        os.path.join(
            os.path.dirname(__file__), "assigments_01", "assigment_syntax_error.ino"
        ),
    )

    assert sum(result.values()) / len(result) == 0.0


def test_missing_definition():
    result = compare_solution_assignment(
        os.path.join(os.path.dirname(__file__), "solution_01", "solution.ino"),
        os.path.join(
            os.path.dirname(__file__), "assigments_01", "assigment_missing_def.ino"
        ),
    )

    assert sum(result.values()) / len(result) == 50.0


def test_compare_setups():
    percent_match = compare_set_inner_func_calls(
        "setup",
        os.path.join(os.path.dirname(__file__), "solution_01", "solution.ino"),
        os.path.join(
            os.path.dirname(__file__),
            "assigments_01",
            "assigment_multiple_setup_calls.ino",
        ),
    )

    assert percent_match == 100.0


def test_compare_folders():
    result = batch_compare("solutions", "sample_student_submissions")

    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
