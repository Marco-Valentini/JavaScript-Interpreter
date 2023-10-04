# From Lark's Documentation:
# The transfomer processes the parse tree bottom-up, starting from the leaves and going up to the root.
# For each node it calls the related method according to the nodes's data, and uses the returned value to replace the
# node, creating a new structure. When the transformer doesn't find the method for a node, it simply returns the node.

from lark.visitors import Transformer
from SymbolTable import symbol_table
from error_handling import *


class TreeToJS(Transformer):
    """
    This class extends Lark's transformer class, which provides a convenient interface to process the parse tree that
    Lark returns. Each method of the class corresponds to one of the rules in the grammar.
    """
    @staticmethod
    def print_statement(args):
        if not args:
            print('undefined')  # when no message is specified
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

    @staticmethod
    def variable_statement(args):
        try:
            if len(args) == 2:  # variable declaration (es. let a)
                if args[1].value in reserved_words:
                    wrong_id = args[1].value
                    raise ReservedWordAsIdentifier
                symbol_table.insert(args[1].value, {'declaration': args[0].value, 'value': 'undefined',
                                                    'type': 'undefined'})
                return 'undefined'
            elif len(args) == 3:  # variable assignment (es. a = 2)
                if args[0].value in reserved_words:
                    wrong_id = args[0].value
                    raise ReservedWordAsIdentifier
                if args[0].value in symbol_table.table.keys():
                    if symbol_table.find(args[0].value)['declaration'] == 'const':
                        raise ConstAssignmentTypeError
                    else:
                        symbol_table.update(args[0].value,
                                            {'declaration': symbol_table.find(args[0].value)['declaration'],
                                             'value': args[2], 'type': type(args[2])})
                else:  # the variable has not been declared yet
                    symbol_table.insert(args[0].value, {'declaration': 'var', 'value': args[2], 'type': type(args[2])})
                return args[2]
            elif len(args) == 4:  # variable declaration and assignment (es. let a = 2)
                if args[1].value in reserved_words:
                    wrong_id = args[1].value
                    raise ReservedWordAsIdentifier
                if args[1].value in symbol_table.table.keys():
                    if args[0].value == symbol_table.find(args[1].value)['declaration']:
                        symbol_table.update(args[1].value, {'declaration': args[0].value, 'value': args[3],
                                                            'type': type(args[3])})
                    else:
                        raise IdentifierAlreadyDeclared
                else:
                    symbol_table.insert(args[1].value, {'declaration': args[0].value, 'value': args[3],
                                                        'type': type(args[3])})
                return 'undefined'
            elif len(args) == 6: # assignment to a cell of the array
                if args[0].value in reserved_words:
                    wrong_id = args[0].value
                    raise ReservedWordAsIdentifier
                if args[0].value in symbol_table.table.keys():
                    arr = symbol_table.find(args[0].value)['value']
                    if args[2] >= len(arr):
                        # fill intermediate cells with undefined
                        for i in range(len(arr), args[2]):
                            arr.append('undefined')
                        arr.append(args[5])
                    else:
                        arr[args[2]] = args[5] # update the value
                symbol_table.update(args[0].value, {'declaration': symbol_table.find(args[0].value)['declaration'],
                                                    'value': arr, 'type': type(arr)})
        except IdentifierAlreadyDeclared:
            print('SyntaxError: Identifier ' + args[1].value + ' has already been declared')
        except ConstAssignmentTypeError:
            print('TypeError: Assignment to constant variable')
        except ReservedWordAsIdentifier:
            print('SyntaxError: Unexpected token ' + wrong_id)

    def variable_assignment(self, args):
        if args[0] == '++':  # pre increment
            value = symbol_table.find(args[1])['value']
            if type(value) in [int, float]:
                value += 1
                symbol_table.update(args[1], {'declaration': symbol_table.find(args[1])['declaration'], 'value': value,
                                              'type': type(value)})
            else:
                value = 'NaN'
                symbol_table.update(args[1], {'declaration': symbol_table.find(args[1])['declaration'], 'value': 'NaN',
                                              'type': 'NaN'})
            return value
        elif args[0] == '--':  # pre decrement
            value = symbol_table.find(args[1])['value']
            if type(value) in [int, float]:
                value -= 1
                symbol_table.update(args[1], {'declaration': symbol_table.find(args[1])['declaration'], 'value': value,
                                              'type': type(value)})
            else:
                value = 'NaN'
                symbol_table.update(args[1], {'declaration': symbol_table.find(args[1])['declaration'], 'value': 'NaN',
                                              'type': 'NaN'})
            return value
        elif args[1] == '+=':
            value = self.add([symbol_table.find(args[0])['value'], args[2]])
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': value,
                                          'type': type(value)})
            return value
        elif args[1] == '-=':
            value = self.sub([symbol_table.find(args[0])['value'], args[2]])
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': value,
                                          'type': type(value)})
            return value
        elif args[1] == '*=':
            value = self.mul([symbol_table.find(args[0])['value'], args[2]])
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': value,
                                          'type': type(value)})
            return value
        elif args[1] == '/=':
            value = self.div([symbol_table.find(args[0])['value'], args[2]])
            symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': value,
                                          'type': type(value)})
            return value
        elif args[1] == '++':  # post increment
            value = symbol_table.find(args[0])['value']
            if type(value) in [int, float]:
                symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'],
                                              'value': value + 1, 'type': type(value + 1)})
            else:
                value = 'NaN'
                symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': 'NaN',
                                              'type': 'NaN'})
            return value
        elif args[1] == '--':  # post decrement
            value = symbol_table.find(args[0])['value']
            if type(value) in [int, float]:
                symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'],
                                              'value': value - 1, 'type': type(value - 1)})
            else:
                value = 'NaN'
                symbol_table.update(args[0], {'declaration': symbol_table.find(args[0])['declaration'], 'value': 'NaN',
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
        :param args:
        :return:
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
        This method is used to check if two values are not equal. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        so does not simulate the JavaScript type coercition
        :param args:
        :return:
        """
        return args[0] == args[1]

    @staticmethod
    def strict_inequality(args):
        """
        This method is used to check if two values are not equal. It is the !== JavaScript operator,
        so does not simulate the JavaScript type coercition
        :param args:
        :return:
        """
        return args[0] != args[1]

    @staticmethod
    def array(args):
        return args

    @staticmethod
    def greater_than(args):
        """
        This method is used to check if the first value is greater than the second one. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        This method is used to check if the first value is greater than or equal to the second one. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        This method is used to check if the first value is less than the second one. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        This method is used to check if the first value is less than or equal to the second one. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        This method is used to add two values. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        This method is used to subtract two values. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        This method is used to multiply two values. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        This method is used to divide two values. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        This method is used to negate a value. It simulates the JavaScript type coercition
        :param args:
        :return:
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
        This method is used to negate a boolean value. It simulates the JavaScript type coercition
        :param args:
        :return:
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

    @staticmethod
    def factor(args):
        """
        Substitute the value in the explored nodes
        :param args:
        :return:
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
            try:
                return symbol_table.find(args[0].value)['value']
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

    @staticmethod
    def array_access(args):
        try:
            if type(args[1]) == str:
                args[1] = int(args[1])
            arr = symbol_table.find(args[0].value)['value']
            return arr[args[1]]
        except IndexError:  # es index out of bounds
            return 'undefined'
        except TypeError:  # es float index
            return 'undefined'
        except ValueError:  # es string index
            return 'undefined'

    @staticmethod
    def array_length(args):
        try:
            arr = symbol_table.find(args[0])['value']
            return len(arr)
        except TypeError:
            return 'undefined'
        except ValueError:
            return 'undefined'
