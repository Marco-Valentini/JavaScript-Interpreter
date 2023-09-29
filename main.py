from lark import Lark
from Transformer import TreeToJS

# the grammar is contained in the file JavaScript_grammar.lark
parser = Lark.open("JavaScript_grammar.lark", parser='lalr',transformer=TreeToJS(), ambiguity="explicit", debug=True)  # TODO capire quale lexer utilizzare


def main():
    while True:
        try:
            s = input('JS>>> ')
        except EOFError:
            break
        print(parser.parse(s))

if __name__ == '__main__':
    main()

# TODO serve implementare una logica che prenda gli statement uno alla volta dai file e quindi
with open("test.js", "r") as f:
    for line in f:
        print(parser.parse(line))