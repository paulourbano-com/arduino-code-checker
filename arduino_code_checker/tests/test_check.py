import os
from arduino_code_checker.src.code_check import (
    compare_solution_assigment,
    compare_set_inner_func_calls,
)


def test_check_01():
    percent_match = compare_solution_assigment(
        os.path.join(os.path.dirname(__file__), "solution_01", "solution.ino"),
        os.path.join(os.path.dirname(__file__), "assigments_01", "assigment.ino"),
    )

    assert percent_match == 100.0


def test_non_existant_file():
    percent_match = compare_solution_assigment(
        os.path.join(os.path.dirname(__file__), "solution_01", "solution.ino"),
        os.path.join(os.path.dirname(__file__), "assigments_01", "not_there.ino"),
    )

    assert percent_match == -1.0


def test_parse_error():
    percent_match = compare_solution_assigment(
        os.path.join(os.path.dirname(__file__), "solution_01", "solution.ino"),
        os.path.join(
            os.path.dirname(__file__), "assigments_01", "assigment_syntax_error.ino"
        ),
    )

    assert percent_match == -1.0


def test_missing_definition():
    percent_match = compare_solution_assigment(
        os.path.join(os.path.dirname(__file__), "solution_01", "solution.ino"),
        os.path.join(
            os.path.dirname(__file__), "assigments_01", "assigment_missing_def.ino"
        ),
    )

    assert percent_match == -1.0


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
