from __future__ import print_function
import sys
import re
import traceback
from rich.pretty import pprint
import argparse
from copy import copy

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


def show_func_defs(filename):
    file_contents = ""
    with open(filename, "r", encoding="utf-8") as file_handler:
        file_contents = file_handler.read()

    # Remove comments
    file_contents_no_comments = comment_remover(file_contents)

    parser = c_parser.CParser()
    ast = parser.parse(file_contents_no_comments, filename="<none-->")

    # ast.show()

    v = FuncDefVisitor()
    v.visit(ast)


def get_ast_from_file(filename):
    ast = None

    try:
        file_contents = ""
        with open(filename, "r", encoding="utf-8") as file_handler:
            file_contents = file_handler.read()

        # Remove comments
        file_contents_no_comments = comment_remover(file_contents)

        parser = c_parser.CParser()
        ast = parser.parse(file_contents_no_comments, filename=filename)
    except (FileNotFoundError, AssertionError):
        print(traceback.format_exc())

    return ast


def check_basic_elements(ast):
    return_value = False

    v = FuncDefVisitor()
    v.visit(ast)

    if all([def_name in v.def_calls.keys() for def_name in ["loop", "setup"]]):
        return_value = True

    return return_value


def compare_set_inner_func_calls(
    outer_func_name: str, solution_file: str, assigment_file: str
):
    return_value = 100.0

    solution_ast = get_ast_from_file(solution_file)
    assigment_ast = get_ast_from_file(assigment_file)

    solution_visitor = FuncDefVisitor()
    solution_visitor.visit(solution_ast)
    solution_calls = [
        item
        for x in solution_visitor.def_calls.get(outer_func_name)
        for item in x.keys()
    ]

    assigment_visitor = FuncDefVisitor()
    assigment_visitor.visit(assigment_ast)
    assigment_calls = [
        item
        for x in assigment_visitor.def_calls.get(outer_func_name)
        for item in x.keys()
    ]

    # If all functions called in the solution are not called in the assigment,
    # lower the match score.
    for call in set(solution_calls):
        if not call in assigment_calls:
            return_value = return_value - 1 / len(set(solution_calls))

    return return_value


def compare_solution_assigment(solution_file: str, assigment_file: str):

    percent_match = -1.0

    solution_ast = get_ast_from_file(solution_file)
    assigment_ast = get_ast_from_file(assigment_file)

    # Checks if the assigment can be parsed and if the assigments
    # fullfills the basic requirements of an Arduino source file,
    # e.g. having function definitions for 'loop' and 'setup'
    if assigment_ast is not None and check_basic_elements(assigment_ast):
        setup_match = compare_set_inner_func_calls(
            "setup", solution_file, assigment_file
        )
        loop_match = compare_set_inner_func_calls("loop", solution_file, assigment_file)

        percent_match = sum([setup_match, loop_match]) / 2

    return percent_match


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--solution_folder",
        help="Folder containing source code (.ino) and Eagle PCB () files for base solution.",
        type=str,
        default="solution",
    )

    parser.add_argument(
        "--assigments_folder",
        help="Folder containing source code (.ino) and Eagle PCB () files for assignment solutions.",
        type=str,
        default="assigments",
    )

    args = parser.parse_args().__dict__

    print(args)

    # show_func_defs(filename)
