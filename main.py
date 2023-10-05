from lark import Lark, UnexpectedInput
from lark.exceptions import UnexpectedToken
from Interpreter import JavaScriptInterpreter
from error_handling import *
from argparse import ArgumentParser  # to provide Command Line Interface (CLI)

# the grammar is contained in the file JavaScript_grammar.lark
parser = Lark.open("JavaScript_grammar.lark", parser='lalr', debug=True)


def parse(javascript_script):
    """
    Wrapper for the parser.parse method including error handling
    :param javascript_script:
    :return:
    """
    try:
        tree = parser.parse(javascript_script)
    except UnexpectedInput as u:
        exc_class = u.match_examples(parser.parse, {
            MissingClosingParenthesisInArgumentList: ['(fo',
                                                      '(foo, fo',
                                                      '(fooo, foo, fo'],
            MissingClosingParenthesisAfterCondition: ['if (a == b',
                                                      'if (a > b',
                                                      'if (a < b',
                                                      'if (a',
                                                      'if (true',
                                                      'if (false',
                                                      'if (a == b && c != d',
                                                      'while (a == b',
                                                      'while (a > b',
                                                      'while (a < b',
                                                      'while (a',
                                                      'while (true',
                                                      'while (false',
                                                      'while (a == b && c != d'
                                                      ],
            MissingClosingParenthesisAfterElementList: ['[fo',
                                                        '[foo, fo',
                                                        '[fooo, foo, fo'],
            MissingClosingParenthesisAfterFunctionBody: ['function foo() {',
                                                         'function foo() { return 1',
                                                         'function foo() { return 1 + 2',
                                                         'function foo(a,b) { return a+ b'],
            MissingEqualInConstDeclaration: ['const foo 1',
                                             'const foo',
                                             'const foo;'],
            UnexpectedEndOfInput: ['const foo =',
                                   'foo(']
        }, use_accepts=True)  # True because it is recommended by Lark documentation
        if not exc_class:
            raise
        raise exc_class(u.get_context(javascript_script), u.line, u.column)
    else:
        return tree


def main():
    argument_parser = ArgumentParser(description="JavaScript Interpreter", epilog="Enjoy the interpreter!")
    argument_parser.add_argument("-s", "--script", help="JavaScript script to be interpreted", type=str)
    argument_parser.add_argument("-c", "--console", help="Starts the interpreter in console mode", action="store_true")
    argument_parser.add_argument("-d", "--debug", help="Prints the tree of the process for debug purposes",
                                 action="store_true")
    # get the arguments from the command line instruction
    args = argument_parser.parse_args()
    # args.script = "./javascript_tests/test_2.js"
    # args.console = False

    if args.console or args.script is None:  # if no script is provided, the interpreter starts in console mode
        while True:
            try:
                console = input('JS> ')
                if console == "" or console.startswith("//") or (console.startswith("/*") and console.endswith("*/")):
                    continue
            except EOFError:
                break
            try:
                tree = parse(console)
            except UnexpectedInput as i:
                print(f"LexicalError: scanning failed due to unexpected input at line {i.line} and column {i.column}\n")  # gestisce anche lexical errors?
                continue
            except UnexpectedToken as t:
                print(f"LexicalError: scanning failed due to unexpected token at line {t.line} and column {t.column}\n")
                continue
            except MissingClosingParenthesisInArgumentList as e:
                print(e)
                continue
            except MissingClosingParenthesisAfterCondition as e:
                print(e)
                continue
            except MissingClosingParenthesisAfterElementList as e:
                print(e)
                continue
            except MissingClosingParenthesisAfterFunctionBody as e:
                print(e)
                continue
            except MissingEqualInConstDeclaration as e:
                print(e)
                continue
            except UnexpectedEndOfInput as e:
                print(e)
                continue
            try:
                interpeted_tree = JavaScriptInterpreter().visit(tree)
            except IsNotAFunction as e:
                print(e)
                continue
            if args.debug:
                print("Here the parse tree for debug purposes: \n")
                print(tree.pretty())
            if type(interpeted_tree) == list:
                for out in interpeted_tree:
                    if out is not None:
                        print(out)
            elif interpeted_tree is not None:
                print(interpeted_tree)
    elif args.script:

        with open(args.script, "r") as f:
            file = f.read()
            try:
                tree = parse(file)
            except UnexpectedInput as i:
                print(f"LexicalError: scanning failed due to unexpected input at line {i.line} column {i.column}\n")  # gestisce anche lexical errors?
                exit()
            except UnexpectedToken as t:
                print(f"LexicalError: scanning failed due to unexpected token at line {t.line} column {t.column}\n")
                exit()
            except MissingClosingParenthesisInArgumentList as e:
                print(e)
                exit()
            except MissingClosingParenthesisAfterCondition as e:
                print(e)
                exit()
            except MissingClosingParenthesisAfterElementList as e:
                print(e)
                exit()
            except MissingClosingParenthesisAfterFunctionBody as e:
                print(e)
                exit()
            except MissingEqualInConstDeclaration as e:
                print(e)
                exit()
            except UnexpectedEndOfInput as e:
                print(e)
                exit()
            try:
                JavaScriptInterpreter().visit(tree)
            except IsNotAFunction as e:
                print(e)
                exit()
            if args.debug:
                print("Here the parse tree for debug purposes: \n")
                print(tree.pretty())  # print the parse tree


if __name__ == '__main__':
    main()


