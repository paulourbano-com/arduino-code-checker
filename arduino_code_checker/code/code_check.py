from __future__ import print_function
import sys
import re
from rich.pretty import pprint

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
    def visit_FuncDef(self, node):
        fcv = FuncCallVisitor()
        fcv.visit(node.body)

        pprint({node.decl.name: fcv.callees})  # calles has all funccall in this funcdef


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

    v = FuncDefVisitor()
    v.visit(ast)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        raise ValueError

    show_func_defs(filename)
