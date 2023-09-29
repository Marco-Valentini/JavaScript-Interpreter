# From Lark's Documentation:
# The transfomer processes the parse tree bottom-up, starting from the leaves and going up to the root.
# For each node it calls the related method according to the nodes's data, and uses the returned value to replace the
# node, creating a new structure. When the transformer doesn't find the method for a node, it simply returns the node

# A transformer without methods essentially performs a non-memorized partial deepcopy


from lark.visitors import Transformer

# TODO capire se mettere v_args inline=True o no
# con v_args si possono specificare una serie di parametri: inline (i children dell'albero sono passati come *args e non come una lista)
#  meta (if meta=True) dà una serie di info come riga e colonna a cui ci troviamo
# TODO l'interpreter sembra una sorta di estensione del transformer, dove ad esempio si aggiunge la gestione dell'if o del while
class TreeToJS(Transformer):
    """
    This class extends Lark's transformer class, which provides a convenient interface to process the parse tree that
    Lark returns. Each method of the class corresponds to one of the rules in the grammar.
    """

    def print_statement(self, args):
        print(args[0])

    def input_statement(self, args):
        a = input(args[0])
        return a

    def variable_declaration(self, args):
        pass

    def logical_and(self, args):
        return args[0] and args[1]

    def logical_or(self, args):
        return args[0] or args[1]

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