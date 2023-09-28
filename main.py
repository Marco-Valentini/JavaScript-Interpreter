from lark import Lark, Transformer, v_args

# the grammar is JavaScript_grammar.lark

class TreeToJS(Transformer):

    def print_statement(self, args):
        return args[0]

    def variable_declaration(self, args):
        pass

    def logical_and(self, args):
        return args[0] and args[1]

    def logical_or(self, args):
        return args[0] or args[1]

    def logical_not(self, args):
        return not args[0]

    def equality(self, args):
        return args[0] == args[1]

    def inequality(self, args):
        return args[0] != args[1]

    def greater_than(self, args):
        return args[0] > args[1]

    def greater_than_or_equal(self, args):
        return args[0] >= args[1]

    def less_than(self, args):
        return args[0] < args[1]

    def less_than_or_equal(self, args):
        return args[0] <= args[1]

    def add(self, args):
        if args[0].type == 'NUMBER' and args[0].type == 'NUMBER':
            return int(args[0]) + int(args[1])
        if args[0].type == 'STRING' and args[0].type == 'STRING':  # concatenation
            return args[0] + args[1]

    def sub(self, args):
        if args[0].type == 'NUMBER' and args[0].type == 'NUMBER':
            return int(args[0]) - int(args[1])

    def mul(self, args):
        if args[0].type == 'NUMBER' and args[0].type == 'NUMBER':
            return int(args[0]) * int(args[1])

    def div(self, args):
        if args[0].type == 'NUMBER' and args[0].type == 'NUMBER':
            return int(args[0]) / int(args[1])

    def neg(self, args):
        if args[0].type == 'NUMBER' and args[0].type == 'NUMBER':
            return -int(args[0])

    def not_(self, args):
        return not args[0]


parser = Lark.open("JavaScript_grammar.lark", parser='lalr')


def main():
    while True:
        try:
            s = input('JS>>> ')
        except EOFError:
            break
        print(parser.parse(s))

if __name__ == '__main__':
    main()