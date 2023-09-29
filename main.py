from lark import Lark
from Interpreter import JavaScriptInterpreter

# the grammar is contained in the file JavaScript_grammar.lark
parser = Lark.open("JavaScript_grammar.lark", parser='lalr', debug=True)  # TODO capire quale lexer utilizzare

def main():
    while True:
        try:
            s = input('JS>>> ')
        except EOFError:
            break
        tree = parser.parse(s)
        interpeted_tree = JavaScriptInterpreter().visit(tree)
        print(interpeted_tree)


if __name__ == '__main__':
    main()

# TODO serve implementare una logica che prenda gli statement uno alla volta dai file e quindi
with open("test.js", "r") as f:
    for line in f:
        tree = parser.parse(line)
        interpeted_tree = JavaScriptInterpreter().visit(tree)
        print(interpeted_tree)
