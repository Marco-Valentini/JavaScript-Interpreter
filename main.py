from lark import Lark, Transformer, v_args

# the grammar is JavaScript_grammar.lark

# TODO capire se mettere v_args inline=True o no
# TODO l'interpreter sembra una sorta di estensione del transformer, dove ad esempio si aggiunge la gestione dell'if o del while
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
        return args[0] + args[1]


    def sub(self, args):
        return args[0] - args[1]

    def mul(self, args):
        return args[0] * args[1]

    def div(self, args):
        return args[0] / args[1]


    def neg(self, args):
        if args[0].type == 'NUMBER' and args[0].type == 'NUMBER':
            return -int(args[0])

    def not_(self, args):
        return not args[0]

    def template_literal(self, args):
        temp = ""
        for arg in args: #TODO rendi più efficiente modificando la grammatica
            if type(arg) in [float, int, bool]:
                temp += str(arg) + " "
            else:
                temp += str(arg)
        return temp

    def factor(self, args):
        """
        Substitute the value in the explored nodes
        :param args:
        :return:
        """
        if args[0].type == 'NUMBER':
            return float(args[0].value)
        elif args[0].type == 'STRING':
            return str(args[0].value[1:-1])
        return args[0].value

    def term(self, args):
        return args[0]

    def expression(self, args):
        return args[0]


parser = Lark.open("JavaScript_grammar.lark", parser='lalr',transformer=TreeToJS())  # TODO capire quale lexer utilizzare


def main():
    while True:
        try:
            s = input('JS>>> ')
        except EOFError:
            break
        print(parser.parse(s))

if __name__ == '__main__':
    main()