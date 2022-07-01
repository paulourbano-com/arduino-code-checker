from __future__ import print_function
from email.mime import base
from glob import glob
import sys
from typing import List
import os
import re
import traceback
from numpy import spacing
from rich.pretty import pprint
import argparse
from copy import copy
import pandas as pd
import pycparser

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
sys.path.extend([".", ".."])

from pycparser import c_ast, parse_file
from pycparser import c_parser


class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.callees = []

    def visit_FuncCall(self, node):

        self.callees.append(
            {
                node.name.name: [
                    arg.value if isinstance(arg, c_ast.Constant) else arg.name
                    for arg in node.args
                ]
            }
        )

        # nested funccall
        if node.args:
            self.visit(node.args)


class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.def_calls = {}

    def visit_FuncDef(self, node):
        fcv = FuncCallVisitor()
        fcv.visit(node.body)

        # pprint({node.decl.name: fcv.callees})  # calles has all funccall in this funcdef
        self.def_calls.update({node.decl.name: fcv.callees})


def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith("/"):
            return " "  # note: a space and not an empty string
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(pattern, replacer, text)


def get_ast_from_file(filename):
    ast = None

    try:
        file_contents = ""
        with open(filename, "r", encoding="utf-8") as file_handler:
            file_contents = file_handler.read()

        # Remove comments
        file_contents_no_comments = comment_remover(file_contents)
        file_contents_no_comments = file_contents_no_comments.replace("bool", "int")

        parser = c_parser.CParser()
        ast = parser.parse(file_contents_no_comments, filename=filename)
    except (FileNotFoundError, AssertionError, pycparser.plyparser.ParseError) as e:
        pass
        # print(traceback.format_exc())
        # if isinstance(e, pycparser.plyparser.ParseError):
        #     input()

    return ast


def check_basic_elements(ast):
    return_value = False

    if ast is not None:
        v = FuncDefVisitor()
        v.visit(ast)

        if all([def_name in v.def_calls.keys() for def_name in ["loop", "setup"]]):
            return_value = True

    return return_value


def compare_set_inner_func_calls(
    outer_func_name: str, solution_file: str, assignment_file: str
):
    return_value = 100.0

    solution_ast = get_ast_from_file(solution_file)
    assignment_ast = get_ast_from_file(assignment_file)

    if solution_ast is not None and assignment_ast is not None:
        solution_visitor = FuncDefVisitor()
        solution_visitor.visit(solution_ast)
        solution_calls = [
            item
            for x in solution_visitor.def_calls.get(outer_func_name, {})
            for item in x.keys()
        ]

        assignment_visitor = FuncDefVisitor()
        assignment_visitor.visit(assignment_ast)
        assignment_calls = [
            item
            for x in assignment_visitor.def_calls.get(outer_func_name, {})
            for item in x.keys()
        ]

        # print(solution_calls, assignment_calls)

        # If all functions called in the solution are not called in the assignment,
        # lower the match score.
        for call in set(solution_calls):
            if not call in assignment_calls:
                return_value = return_value - (100.0 / len(set(solution_calls)))
    else:
        return_value = 0.0

    return return_value


def compare_solution_assignment(solution_file: str, assignment_file: str):

    return_value = {
        "codigo_valido": 0.0,
        "tem_setup_loop": 0.0,
        "tem_chamadas_no_setup": 0.0,
        "tem_chamadas_no_loop": 0.0,
    }

    assignment_ast = get_ast_from_file(assignment_file)

    # Checks if the assignment can be parsed and if the assignments
    # fullfills the basic requirements of an Arduino source file,
    # e.g. having function definitions for 'loop' and 'setup'
    if assignment_ast is not None:
        return_value["codigo_valido"] = 100.0

    if check_basic_elements(assignment_ast):
        return_value["tem_setup_loop"] = 100.0

    return_value["tem_chamadas_no_setup"] = compare_set_inner_func_calls(
        "setup", solution_file, assignment_file
    )

    return_value["tem_chamadas_no_loop"] = compare_set_inner_func_calls(
        "loop", solution_file, assignment_file
    )

    return return_value


def batch_compare(
    solutions_folder: str, submissions_folder: str, assignment_list: List[str]
):
    return_value = pd.DataFrame()

    code_solutions: List[str] = glob(os.path.join(solutions_folder, "*.ino"))
    code_submissions: List[str] = glob(os.path.join(submissions_folder, "*.ino"))

    students: pd.DataFrame = pd.read_csv(
        os.path.join(submissions_folder, "student_list.txt"), header=None
    )
    students.columns = ["Nome", "TinkerCAD_Id"]
    students.drop_duplicates(inplace=True)

    # print(code_solutions)
    # print(students)

    partial_solutions = []
    # If there is a assignment to which the student
    # did not submit a solution, compare non-existent
    # files, creating an empty row.

    # all_submission_student_id: List[str] = [
    #     submission.replace(os.path.join(submissions_folder, ""), "").split("_")[0]
    #     for submission in code_submissions
    # ]

    # all_submission_code = [
    #     submission.replace(os.path.join(submissions_folder, ""), "").split("_")[1]
    #     for submission in code_submissions
    # ]

    for id in students.TinkerCAD_Id.unique():
        submitted_by = [
            submission for submission in code_submissions if id in submission
        ]
        submitted_codes = [
            submission.replace(os.path.join(submissions_folder, ""), "").split("_")[1]
            for submission in submitted_by
        ]
        # for current_submission_code in all_submission_code:
        missing_assignment_codes = set(assignment_list) - set(submitted_codes)

        for missing_code in missing_assignment_codes:
            base_return: pd.DataFrame = students.loc[students.TinkerCAD_Id == id].copy()
            base_return["exercicio"] = missing_code

            compare_results = compare_solution_assignment(
                solution_file="non_existent.ino", assignment_file="non_existent.ino"
            )

            for key in compare_results.keys():
                base_return[key] = compare_results.get(key)

            base_return["codigo"] = "Arquivo não encontrado"
            base_return["circuito"] = "Arquivo não encontrado"

            partial_solutions.append(base_return)

    for solution in code_solutions:
        solution_code = solution.replace(os.path.join(solutions_folder, ""), "").split(
            "_"
        )[0]
        if not solution_code in assignment_list:
            continue

        for submission in code_submissions:
            submission_student_id = submission.replace(
                os.path.join(submissions_folder, ""), ""
            ).split("_")[0]

            submission_code = submission.replace(
                os.path.join(submissions_folder, ""), ""
            ).split("_")[1]

            # print(submission_student_id, submission_code)

            if solution_code != submission_code:
                continue

            base_return: pd.DataFrame = students.loc[
                students.TinkerCAD_Id == submission_student_id
            ].copy()

            base_return["exercicio"] = submission_code

            compare_results = compare_solution_assignment(
                solution_file=solution, assignment_file=submission
            )

            for key in compare_results.keys():
                base_return[key] = compare_results.get(key)

            submission_url = os.path.join(os.getcwd(), submission)
            base_return["codigo"] = submission

            # TODO: Add circuit link in circuit evaluation
            brd = submission.replace("code.ino", "circuit.brd")
            brd_url = os.path.join(os.getcwd(), brd)
            base_return["circuito"] = brd

            partial_solutions.append(base_return)

    return_value = pd.concat(partial_solutions)

    # print(return_value)

    return return_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--solution_folder",
        help="Folder containing source code (.ino) and Eagle PCB (.brd) files for base solution.",
        type=str,
        default="solution",
    )

    parser.add_argument(
        "--assignments_folder",
        help="Folder containing source code (.ino) and Eagle PCB (.brd) files for assignment solutions.",
        type=str,
        default="assignments",
    )

    args = parser.parse_args().__dict__

    print(args)
