from lark import Lark, UnexpectedInput
from lark.exceptions import UnexpectedToken
from Interpreter import JavaScriptInterpreter
from error_handling import *

# the grammar is contained in the file JavaScript_grammar.lark
parser = Lark.open("JavaScript_grammar.lark", parser='lalr', debug=True)


def parse(javascript_script):
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

def main(script="javascript_tests/arithmetic_operations.js",console=False, verbose=True):
    if script is None or console is True:
        while True:
            try:
                console = input('JS>>> ')
                if console == "":
                    continue
            except EOFError:
                break
            try:
                tree = parse(console)
            except UnexpectedInput as u:
                print(f"Internal Lark error: parsing failed \n")  # gestisce anche lexical errors?
                print(u)
                continue
            except UnexpectedToken as e:
                print(f"Internal Lark error: parsing failed due to unexpected token\n")
                print(e)
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
                continue  # in console vogliamo continuare
            except UnexpectedEndOfInput as e:
                print(e)
                continue
            try:
                interpeted_tree = JavaScriptInterpreter().visit(tree)
            except IsNotAFunction as e:
                print(e)
                continue
            if verbose:
                print(interpeted_tree)
    else:
        with open(script, "r") as f:
            for line in f:
                try:
                    tree = parse(line)
                except UnexpectedInput as u:
                    print(f"Internal Lark error: parsing failed due to unexprected input\n" + u)  # gestisce anche lexical errors?
                    exit()
                except UnexpectedToken as e:
                    print(f"Internal Lark error: parsing failed due to unexpected token\n" + e)
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
                    interpeted_tree = JavaScriptInterpreter().visit(tree)
                except IsNotAFunction as e:
                    print(e)
                    exit()
                if verbose:
                    print(interpeted_tree)


if __name__ == '__main__':
    main()

# TODO serve implementare una logica che prenda gli statement uno alla volta dai file e quindi

