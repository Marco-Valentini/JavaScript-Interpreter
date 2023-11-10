# From Lark's Documentation:
# The transformer processes the parse tree bottom-up, starting from the leaves and going up to the root.
# For each node it calls the related method according to the data in it, and uses the returned value to replace the
# node, creating a new structure. When the transformer doesn't find the method for a node, it simply returns the node.

from lark.visitors import Transformer
from error_handling import *


class TreeToJS(Transformer):
    """
    This class extends Lark's transformer class, which provides a convenient interface to process the parse tree that
    Lark returns. Each method of the class corresponds to one of the rules in the grammar.
    """
    def __init__(self, symbol_table):
        super().__init__()
        self.symbol_table = symbol_table

    @staticmethod
    def print_statement(args):
        if not args:
            print('undefined')  # when no message is specified (this changes if executed in Chrome console or in replit workspace)
        else:
            print(args[0])

    @staticmethod
    def input_statement(args):
        if not args:
            x = input()  # when no input message is specified
        else:
            x = input(args[0])
        try:
            x = int(x)
        except ValueError:
            try:
                x = float(x)
            except ValueError:
                pass
        return x

    def variable_statement(self, args):
        try:
            if len(args) == 2:  # variable declaration (es. let a)
                if args[1].value in reserved_words:  # check that the chosen identifier can be used
                    wrong_id = args[1].value
                    raise ReservedWordAsIdentifier
                if args[1].value in self.symbol_table.table.keys() and \
                        self.symbol_table.find(args[1].value)['declaration'] == 'let':
                    raise IdentifierAlreadyDeclared
                else:
                    self.symbol_table.insert(args[1].value, {'declaration': args[0].value, 'value': 'undefined',
                                                        'type': 'undefined'})
                return 'undefined'

            elif len(args) == 3:  # variable assignment (es. a = 2) there is included also the assignment of an array to a binding (es. a = [1,2,3])
                if args[0].value in reserved_words:
                    wrong_id = args[0].value
                    raise ReservedWordAsIdentifier
                if self.symbol_table.exist(args[0].value):
                    if self.symbol_table.find(args[0].value)['declaration'] == 'const':
                        raise ConstAssignmentTypeError
                    else:
                        self.symbol_table.update(args[0].value,
                                            {'declaration': self.symbol_table.find(args[0].value)['declaration'],
                                             'value': args[2], 'type': type(args[2])})
                else:  # the variable has not been declared yet
                    self.symbol_table.insert(args[0].value, {'declaration': 'var', 'value': args[2], 'type': type(args[2])})
                return args[2]

            elif len(args) == 4:  # variable declaration and assignment (es. let a = 2)
                if args[1].value in reserved_words:
                    wrong_id = args[1].value
                    raise ReservedWordAsIdentifier
                if args[1].value in self.symbol_table.table.keys():
                    if self.symbol_table.find(args[1].value)['declaration'] == 'var':
                        self.symbol_table.update(args[1].value, {'declaration': args[0].value, 'value': args[3],
                                                            'type': type(args[3])})
                    else:
                        raise IdentifierAlreadyDeclared
                else:
                    self.symbol_table.insert(args[1].value, {'declaration': args[0].value, 'value': args[3],
                                                        'type': type(args[3])})
                return 'undefined'

            elif len(args) == 6:  # assignment to a cell of the array
                if args[0].value in reserved_words:
                    wrong_id = args[0].value
                    raise ReservedWordAsIdentifier
                if self.symbol_table.exist(args[0].value):
                    arr = self.symbol_table.find(args[0].value)['value']
                    if args[2] >= len(arr):
                        # pad intermediate cells with undefined
                        for i in range(len(arr), args[2]):
                            arr.append('undefined')
                        arr.append(args[5])
                    else:
                        arr[args[2]] = args[5]  # update the value
                    self.symbol_table.update(args[0].value, {'declaration': self.symbol_table.find(args[0].value)['declaration'],
                                                    'value': arr, 'type': type(arr)})
        except IdentifierAlreadyDeclared:
            print('SyntaxError: Identifier ' + args[1].value + ' has already been declared') # print customized error messages
        except ConstAssignmentTypeError:
            print('TypeError: Assignment to constant variable')
        except ReservedWordAsIdentifier:
            print('SyntaxError: Unexpected token ' + wrong_id)

    def variable_assignment(self, args):
        if args[0] == '++':  # pre increment
            value = self.symbol_table.find(args[1])['value']
            if type(value) in [int, float]:
                value += 1
                self.symbol_table.update(args[1], {'declaration': self.symbol_table.find(args[1])['declaration'], 'value': value,
                                              'type': type(value)})
            else:
                value = 'NaN'
                self.symbol_table.update(args[1], {'declaration': self.symbol_table.find(args[1])['declaration'], 'value': 'NaN',
                                              'type': 'NaN'})
            return value
        elif args[0] == '--':  # pre decrement
            value = self.symbol_table.find(args[1])['value']
            if type(value) in [int, float]:
                value -= 1
                self.symbol_table.update(args[1], {'declaration': self.symbol_table.find(args[1])['declaration'], 'value': value,
                                              'type': type(value)})
            else:
                value = 'NaN'
                self.symbol_table.update(args[1], {'declaration': self.symbol_table.find(args[1])['declaration'], 'value': 'NaN',
                                              'type': 'NaN'})
            return value
        elif args[1] == '+=':
            value = self.add([self.symbol_table.find(args[0])['value'], args[2]])
            self.symbol_table.update(args[0], {'declaration': self.symbol_table.find(args[0])['declaration'], 'value': value,
                                          'type': type(value)})
            return value
        elif args[1] == '-=':
            value = self.sub([self.symbol_table.find(args[0])['value'], args[2]])
            self.symbol_table.update(args[0], {'declaration': self.symbol_table.find(args[0])['declaration'], 'value': value,
                                          'type': type(value)})
            return value
        elif args[1] == '*=':
            value = self.mul([self.symbol_table.find(args[0])['value'], args[2]])
            self.symbol_table.update(args[0], {'declaration': self.symbol_table.find(args[0])['declaration'], 'value': value,
                                          'type': type(value)})
            return value
        elif args[1] == '/=':
            value = self.div([self.symbol_table.find(args[0])['value'], args[2]])
            self.symbol_table.update(args[0], {'declaration': self.symbol_table.find(args[0])['declaration'], 'value': value,
                                          'type': type(value)})
            return value
        elif args[1] == '++':  # post increment
            value = self.symbol_table.find(args[0])['value']
            if type(value) in [int, float]:
                self.symbol_table.update(args[0], {'declaration': self.symbol_table.find(args[0])['declaration'],
                                              'value': value + 1, 'type': type(value + 1)})
            else:
                value = 'NaN'
                self.symbol_table.update(args[0], {'declaration': self.symbol_table.find(args[0])['declaration'], 'value': 'NaN',
                                              'type': 'NaN'})
            return value
        elif args[1] == '--':  # post decrement
            value = self.symbol_table.find(args[0])['value']
            if type(value) in [int, float]:
                self.symbol_table.update(args[0], {'declaration': self.symbol_table.find(args[0])['declaration'],
                                              'value': value - 1, 'type': type(value - 1)})
            else:
                value = 'NaN'
                self.symbol_table.update(args[0], {'declaration': self.symbol_table.find(args[0])['declaration'], 'value': 'NaN',
                                              'type': 'NaN'})
            return value

    @staticmethod
    def return_statement(args):
        return args[1]

    @staticmethod
    def logical_and(args):
        return args[0] and args[1]

    @staticmethod
    def logical_or(args):
        return args[0] or args[1]

    @staticmethod
    def equality(args):
        """
        This method is used to check if two values are equal. It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int] and type(args[1]) in [float, int]:
            return args[0] == args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                try:
                    return int(args[0]) == args[1]
                except ValueError:
                    try:
                        return float(args[0]) == args[1]
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                try:
                    return args[0] == int(args[1])
                except ValueError:
                    try:
                        return args[0] == float(args[1])
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == bool:
                if args[1]:
                    return args[0] == 1
                else:
                    return args[0] == 0
            elif type(args[0]) == bool and type(args[1]) in [float, int]:
                if args[0]:
                    return 1 == args[1]
                else:
                    return 0 == args[1]
            else:
                return args[0] == args[1]

    @staticmethod
    def inequality(args):
        """
        This method is used to check if two values are not equal. It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int] and type(args[1]) in [float, int]:
            return args[0] != args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                try:
                    return int(args[0]) != args[1]
                except ValueError:
                    try:
                        return float(args[0]) != args[1]
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                try:
                    return args[0] != int(args[1])
                except ValueError:
                    try:
                        return args[0] != float(args[1])
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == bool:
                if args[1]:
                    return args[0] != 1
                else:
                    return args[0] != 0
            elif type(args[0]) == bool and type(args[1]) in [float, int]:
                if args[0]:
                    return 1 != args[1]
                else:
                    return 0 != args[1]
            else:
                return args[0] != args[1]

    @staticmethod
    def strict_equality(args):
        """
        This method is used to check if two values are equal. It is the === JavaScript operator,
        so does not simulate the JavaScript type coercion
        """
        return args[0] == args[1]

    @staticmethod
    def strict_inequality(args):
        """
        This method is used to check if two values are not equal. It is the !== JavaScript operator,
        so does not simulate the JavaScript type coercion
        """
        return args[0] != args[1]

    @staticmethod
    def array(args):
        return args

    @staticmethod
    def greater_than(args):
        """
        This method is used to check if the first value is greater than the second one.
        It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int] and type(args[1]) in [float, int]:
            return args[0] > args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                try:
                    return int(args[0]) > args[1]
                except ValueError:
                    try:
                        return float(args[0]) > args[1]
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                try:
                    return args[0] > int(args[1])
                except ValueError:
                    try:
                        return args[0] > float(args[1])
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == bool:
                if args[1]:
                    return args[0] > 1
                else:
                    return args[0] > 0
            elif type(args[0]) == bool and type(args[1]) in [float, int]:
                if args[0]:
                    return 1 > args[1]
                else:
                    return 0 > args[1]
            else:
                return False

    @staticmethod
    def greater_than_or_equal(args):
        """
        This method is used to check if the first value is greater than or equal to the second one.
        It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int] and type(args[1]) in [float, int]:
            return args[0] >= args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                try:
                    return int(args[0]) >= args[1]
                except ValueError:
                    try:
                        return float(args[0]) >= args[1]
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                try:
                    return args[0] >= int(args[1])
                except ValueError:
                    try:
                        return args[0] >= float(args[1])
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == bool:
                if args[1]:
                    return args[0] >= 1
                else:
                    return args[0] >= 0
            elif type(args[0]) == bool and type(args[1]) in [float, int]:
                if args[0]:
                    return 1 >= args[1]
                else:
                    return 0 >= args[1]
            else:
                return False

    @staticmethod
    def less_than(args):
        """
        This method is used to check if the first value is less than the second one.
        It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int] and type(args[1]) in [float, int]:
            return args[0] < args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                try:
                    return int(args[0]) < args[1]
                except ValueError:
                    try:
                        return float(args[0]) < args[1]
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                try:
                    return args[0] < int(args[1])
                except ValueError:
                    try:
                        return args[0] < float(args[1])
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == bool:
                if args[1]:
                    return args[0] < 1
                else:
                    return args[0] < 0
            elif type(args[0]) == bool and type(args[1]) in [float, int]:
                if args[0]:
                    return 1 < args[1]
                else:
                    return 0 < args[1]
            else:
                return False

    @staticmethod
    def less_than_or_equal(args):
        """
        This method is used to check if the first value is less than or equal to the second one.
        It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int] and type(args[1]) in [float, int]:
            return args[0] <= args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                try:
                    return int(args[0]) <= args[1]
                except ValueError:
                    try:
                        return float(args[0]) <= args[1]
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                try:
                    return args[0] <= int(args[1])
                except ValueError:
                    try:
                        return args[0] <= float(args[1])
                    except ValueError:
                        return False
            elif type(args[0]) in [float, int] and type(args[1]) == bool:
                if args[1]:
                    return args[0] <= 1
                else:
                    return args[0] <= 0
            elif type(args[0]) == bool and type(args[1]) in [float, int]:
                if args[0]:
                    return 1 <= args[1]
                else:
                    return 0 <= args[1]
            else:
                return False

    @staticmethod
    def add(args):
        """
        This method is used to add two values. It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int, bool] and type(args[1]) in [float, int, bool] or type(args[0]) == type(args[1]):
            return args[0] + args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                return args[0] + str(args[1])
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                return str(args[0]) + args[1]
            elif type(args[0]) == str and type(args[1]) == bool:
                if args[1]:
                    return args[0] + "true"
                else:
                    return args[0] + "false"
            elif type(args[0]) == bool and type(args[1]) == str:
                if args[0]:
                    return "true" + args[1]
                else:
                    return "false" + args[1]
            else:
                return 'NaN'

    @staticmethod
    def sub(args):
        """
        This method is used to subtract two values. It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int, bool] and type(args[1]) in [float, int, bool]:
            return args[0] - args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                try:
                    return int(args[0]) - args[1]
                except ValueError:
                    try:
                        return float(args[0]) - args[1]
                    except ValueError:
                        return 'NaN'
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                try:
                    return args[0] - int(args[1])
                except ValueError:
                    try:
                        return args[0] - float(args[1])
                    except ValueError:
                        return 'NaN'
            elif type(args[0]) in [float, int] and type(args[1]) == bool:
                if args[1]:
                    return args[0] - 1
                else:
                    return args[0] - 0
            elif type(args[0]) == bool and type(args[1]) in [float, int]:
                if args[0]:
                    return 1 - args[1]
                else:
                    return 0 - args[1]
            elif type(args[0]) == bool and type(args[1]) == str:
                if args[0]:
                    try:
                        return 1 - int(args[1])
                    except ValueError:
                        try:
                            return 1 - float(args[1])
                        except ValueError:
                            return 'NaN'
                else:
                    try:
                        return 0 - int(args[1])
                    except ValueError:
                        try:
                            return 0 - float(args[1])
                        except ValueError:
                            return 'NaN'
            elif type(args[0]) == str and type(args[1]) == bool:
                if args[1]:
                    try:
                        return int(args[0]) - 1
                    except ValueError:
                        try:
                            return float(args[0]) - 1
                        except ValueError:
                            return 'NaN'
                else:
                    try:
                        return int(args[0]) - 0
                    except ValueError:
                        try:
                            return float(args[0]) - 0
                        except ValueError:
                            return 'NaN'
            elif type(args[0]) == str and type(args[1]) == str:
                try:
                    return int(args[0]) - int(args[1])
                except ValueError:
                    try:
                        return float(args[0]) - float(args[1])
                    except ValueError:
                        try:
                            return int(args[0]) - float(args[1])
                        except ValueError:
                            try:
                                return float(args[0]) - int(args[1])
                            except ValueError:
                                return 'NaN'
            else:
                return 'NaN'

    @staticmethod
    def mul(args):
        """
        This method is used to multiply two values. It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int, bool] and type(args[1]) in [float, int, bool]:
            return args[0] * args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                try:
                    return int(args[0]) * args[1]
                except ValueError:
                    try:
                        return float(args[0]) * args[1]
                    except ValueError:
                        return 'NaN'
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                try:
                    return args[0] * int(args[1])
                except ValueError:
                    try:
                        return args[0] * float(args[1])
                    except ValueError:
                        return 'NaN'
            elif type(args[0]) in [float, int] and type(args[1]) == bool:
                if args[1]:
                    return args[0] * 1
                else:
                    return args[0] * 0
            elif type(args[0]) == bool and type(args[1]) in [float, int]:
                if args[0]:
                    return 1 * args[1]
                else:
                    return 0 * args[1]
            elif type(args[0]) == bool and type(args[1]) == str:
                if args[0]:
                    try:
                        return 1 * int(args[1])
                    except ValueError:
                        try:
                            return 1 * float(args[1])
                        except ValueError:
                            return 'NaN'
                else:
                    try:
                        return 0 * int(args[1])
                    except ValueError:
                        try:
                            return 0 * float(args[1])
                        except ValueError:
                            return 'NaN'
            elif type(args[0]) == str and type(args[1]) == bool:
                if args[1]:
                    try:
                        return int(args[0]) * 1
                    except ValueError:
                        try:
                            return float(args[0]) * 1
                        except ValueError:
                            return 'NaN'
                else:
                    try:
                        return int(args[0]) * 0
                    except ValueError:
                        try:
                            return float(args[0]) * 0
                        except ValueError:
                            return 'NaN'
            elif type(args[0]) == str and type(args[1]) == str:
                try:
                    return int(args[0]) * int(args[1])
                except ValueError:
                    try:
                        return float(args[0]) * float(args[1])
                    except ValueError:
                        try:
                            return int(args[0]) * float(args[1])
                        except ValueError:
                            try:
                                return float(args[0]) * int(args[1])
                            except ValueError:
                                return 'NaN'
            else:
                return 'NaN'

    @staticmethod
    def div(args):
        """
        This method is used to divide two values. It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int, bool] and type(args[1]) in [float, int, bool]:
            return args[0] / args[1]
        else:
            if type(args[0]) == str and type(args[1]) in [float, int]:
                try:
                    return int(args[0]) / args[1]
                except ValueError:
                    try:
                        return float(args[0]) / args[1]
                    except ValueError:
                        return 'NaN'
            elif type(args[0]) in [float, int] and type(args[1]) == str:
                try:
                    return args[0] / int(args[1])
                except ValueError:
                    try:
                        return args[0] / float(args[1])
                    except ValueError:
                        return 'NaN'
            elif type(args[0]) in [float, int] and type(args[1]) == bool:
                if args[1]:
                    return args[0] / 1
                else:
                    return args[0] / 0
            elif type(args[0]) == bool and type(args[1]) in [float, int]:
                if args[0]:
                    return 1 / args[1]
                else:
                    return 0 / args[1]
            elif type(args[0]) == bool and type(args[1]) == str:
                if args[0]:
                    try:
                        return 1 / int(args[1])
                    except ValueError:
                        try:
                            return 1 / float(args[1])
                        except ValueError:
                            return 'NaN'
                else:
                    try:
                        return 0 / int(args[1])
                    except ValueError:
                        try:
                            return 0 / float(args[1])
                        except ValueError:
                            return 'NaN'
            elif type(args[0]) == str and type(args[1]) == bool:
                if args[1]:
                    try:
                        return int(args[0]) / 1
                    except ValueError:
                        try:
                            return float(args[0]) / 1
                        except ValueError:
                            return 'NaN'
                else:
                    try:
                        return int(args[0]) / 0
                    except ValueError:
                        try:
                            return float(args[0]) / 0
                        except ValueError:
                            return 'NaN'
            elif type(args[0]) == str and type(args[1]) == str:
                try:
                    return int(args[0]) / int(args[1])
                except ValueError:
                    try:
                        return float(args[0]) / float(args[1])
                    except ValueError:
                        try:
                            return int(args[0]) / float(args[1])
                        except ValueError:
                            try:
                                return float(args[0]) / int(args[1])
                            except ValueError:
                                return 'NaN'
            else:
                return 'NaN'

    @staticmethod
    def negative(args):
        """
        This method is used to negate a value. It simulates the JavaScript type coercion
        """
        if type(args[0]) in [float, int]:
            return -args[0]
        elif type(args[0]) == bool:
            if args[0]:
                return -1
            else:
                return -0
        elif type(args[0]) == str:
            try:
                return - int(args[0])
            except ValueError:
                try:
                    return - float(args[0])
                except ValueError:
                    return 'NaN'
        else:
            return 'NaN'

    @staticmethod
    def logical_not(args):
        """
        This method is used to negate a boolean value. It simulates the JavaScript type coercion
        """
        if type(args[0]) == bool:
            return not args[0]
        elif type(args[0]) == float:
            if args[0] == 0:
                return True
            else:
                return False
        elif type(args[0]) == str:
            if args[0] == '':
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def template_literal(args):
        temp = ""
        for arg in args:
            if type(arg) in [float, int, bool, str]:
                temp += str(arg) + " "
            else:
                temp += str(arg)
        return temp

    def factor(self, args):
        """
        This method is used to substitute the nodes of the parse tree passed in the args parameter with computed value.
        """
        if type(args[0]) in [str, int, float, list]:  # case of template literal or array
            return args[0]
        elif args[0].type == 'FLOAT':
            return float(args[0].value)
        elif args[0].type == 'INT':
            return int(args[0].value)
        elif args[0].type == 'STRING':
            return str(args[0].value[1:-1])
        elif args[0].type == 'BOOL':
            if args[0].value == 'true':
                return True
            elif args[0].value == 'false':
                return False
        elif args[0].type == 'IDENTIFIER':
            # an identifier can be associated with a function or with a value
            try:
                if self.symbol_table.find(args[0].value)['declaration'] == 'function':
                    return f"function {args[0].value}"
                else:
                    return self.symbol_table.find(args[0].value)['value']
            except ReferenceError:
                print('ReferenceError: ' + args[0].value + ' is not defined')
        elif args[0].type == 'ARRAY':
            return args[0]

    @staticmethod
    def term(args):
        return args[0]

    @staticmethod
    def expression(args):
        return args[0]

    def array_access(self, args):
        try:
            if type(args[1]) == str:
                args[1] = int(args[1])
            arr = self.symbol_table.find(args[0].value)['value']
            return arr[args[1]]
        except IndexError:  # es index out of bounds
            return 'undefined'
        except TypeError:  # es float index
            return 'undefined'
        except ValueError:  # es string index
            return 'undefined'

    def array_length(self, args):
        try:
            arr = self.symbol_table.find(args[0])['value']
            if type(arr) == list:
                return len(arr)
            elif type(arr) == str:
                if arr == 'NaN':
                    return 'undefined'
                return len(arr)
        except TypeError: # es if is not an array, neither a string
            return 'undefined'
        except ValueError:
            return 'undefined'
