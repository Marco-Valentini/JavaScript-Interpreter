from lark import Lark, Transformer, v_args

parser = Lark.open("JavaScript_grammar.lark", parser="lalr") #, start=) definisci axiom della grammatica

def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(parser.parse(s))

if __name__ == '__main__':
    # test()  # test can be a function that tests the parser, giving a program as input for the parser
    main()