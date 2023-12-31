from lark import Lark, UnexpectedInput
from lark.exceptions import UnexpectedToken
from Interpreter import JavaScriptInterpreter
from error_handling import *
from argparse import ArgumentParser  # to provide Command Line Interface (CLI) command and flags (i.e., to execute scripts)

import os

# Get the path to the 'JavaScript_grammar.lark' file relative to the script location
script_dir = os.path.dirname(os.path.realpath(__file__))
grammar_file_path = os.path.join(script_dir, "JavaScript_grammar.lark")

# Now you can use grammar_file_path to access the grammar file

# the grammar is contained in the file JavaScript_grammar.lark
parser = Lark.open(grammar_file_path, parser='lalr', debug=True)


def parse(javascript_script):
    """
    Wrapper for the parser.parse method including error handling
    :param javascript_script: script given as input from CLI command
    :return:
    """
    try:
        tree = parser.parse(javascript_script)
    except UnexpectedInput as u:
        # find some lexical or syntactic error
        exc_class = u.match_examples(parser.parse, {
            MissingClosingParenthesisAfterCondition: ['if (a == b',
                                                      'if (a == b { return foo }',
                                                      'if (a > b',
                                                      'if (a > b { return foo }',
                                                      'if (a < b',
                                                      'if (a < b { return foo }',
                                                      'if (a',
                                                      'if (a { return foo }',
                                                      'if (true',
                                                      'if (true { return foo }',
                                                      'if (false',
                                                      'if (false { return foo }',
                                                      'if (a == b && c != d',
                                                      'if (a == b && c != d { return foo }',
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
                                                        '[fooo, foo, fo',
                                                        '[fooo, foo, fo,',
                                                        '[foo, fo,',
                                                        '[fo,'
                                                        ],
            MissingClosingParenthesisAfterFunctionBody: ['function foo() {',
                                                         'function foo() { return 1',
                                                         'function foo() { return 1 + 2',
                                                         'function foo(a,b) { return a+ b'],
            MissingEqualInConstDeclaration: ['const foo 1',
                                             'const foo',
                                             'const foo;'],
            UnexpectedEndOfInput: ['const foo =',
                                   'foo(',
                                   'function foo(',
                                   'function foo(fo',
                                   'function foo(fo,',
                                   'function foo(foo, fo',
                                   'function foo(foo, fo,',
                                   'function foo(fooo, foo, fo',
                                   'function foo(fooo, foo, fo,',
                                   'let a = [fo',
                                   'let a = [foo, fo',
                                   'let a = [fooo, foo, fo',
                                   'let a = [fo,',
                                   'let a = [foo, fo,',
                                   'let a = [fooo, foo, fo,',
                                   'const a = [fo',
                                   'const a = [foo, fo',
                                   'const a = [fooo, foo, fo',
                                   'const a = [fo,',
                                   'const a = [foo, fo,',
                                   'const a = [fooo, foo, fo,',
                                   'var a = [fo',
                                   'var a = [foo, fo',
                                   'var a = [fooo, foo, fo',
                                   'var a = [fo,',
                                   'var a = [foo, fo,',
                                   'var a = [fooo, foo, fo,'
                                   ]
        }, use_accepts=True)  # True because it is recommended by Lark documentation
        if not exc_class:
            raise
        raise exc_class(u.get_context(javascript_script), u.line, u.column)
    else:
        return tree # return the parse tree


def main():
    argument_parser = ArgumentParser(description="JavaScript Interpreter", epilog="Enjoy the interpreter!")
    argument_parser.add_argument("-s", "--script", help="JavaScript script to be interpreted", type=str) # execute a script from a file
    argument_parser.add_argument("-c", "--console", help="Starts the interpreter in console mode",
                                 action="store_true") # execute the interpreter in console mode
    argument_parser.add_argument("-d", "--debug", help="Prints the tree of the process for debug purposes",
                                 action="store_true") # print the parse tree for debug purposes
    # get the arguments from the command line instruction (e.g., the path of the script to be executed)
    args = argument_parser.parse_args()

    if args.console or args.script is None:  # if no script is provided, the interpreter starts in console mode
        while True:
            try:
                console = input('JS> ')
                if console == "" or console.startswith("//") or (console.startswith("/*") and console.endswith("*/")):
                    # ignore comments
                    continue
            except EOFError:
                break
            try:
                tree = parse(console) # obtain the parse tree by parsing the input from the console
            except UnexpectedInput as i:
                print(f"LexicalError: scanning failed due to unexpected input at line {i.line} and column {i.column}\n")
                continue
            except UnexpectedToken as t:
                print(f"LexicalError: scanning failed due to unexpected token at line {t.line} and column {t.column}\n")
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
                interpreted_tree = JavaScriptInterpreter().visit(tree) # interpret the parse tree
            except IsNotAFunction as e:
                print(e)
                continue
            if args.debug:
                print("Here the parse tree for debug purposes: \n")
                print(tree.pretty())
            if interpreted_tree is not None:
                print(interpreted_tree)
    elif args.script:
        # if a script is given, execute it
        with open(args.script, "r") as f:
            file = f.read()
            try:
                tree = parse(file)
            except UnexpectedInput as i:
                print(f"LexicalError: scanning failed due to unexpected input at line {i.line} column {i.column}\n")
                exit()
            except UnexpectedToken as t:
                print(f"LexicalError: scanning failed due to unexpected token at line {t.line} column {t.column}\n")
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


