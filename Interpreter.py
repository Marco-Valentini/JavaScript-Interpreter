# From Lark's Documentation:
# The interpreter walks the tree starting at the root, it visits the tree from the root to the leaves (top-down).
# For each node it calls its methods (inherited) according to tree.data. Differently from transformer, the interpreter
# does not visit the sub-branches, unless it is explicitly told to do so.
from copy import deepcopy

# Interpreter allows to implement branching and loops

from lark.visitors import Interpreter
from Transformer import TreeToJS
from SymbolTable import symbol_table
from error_handling import *


js_transformer = TreeToJS()  # the transformer is used to visit the tree from the leaves to the root (bottom-up)


class JavaScriptInterpreter(Interpreter):

    def start(self, tree):
        return self.visit_children(tree)

    def if_statement(self, tree):
        condition = js_transformer.transform(tree.children[0])
        if condition not in ['undefined', 'null', 'NaN', False, 0, ""]:  # JavaScript falsy values
            true_branch = self.visit(tree.children[1])  # visit the true branch
            if true_branch == []:
                return 'undefined'
            else:
                return true_branch
        elif len(tree.children) == 3:  # if there is else branch
            false_branch = self.visit(tree.children[2])  # visit the false branch
            if false_branch == []:
                return 'undefined'
            else:
                return false_branch

    def while_statement(self, tree):
        condition = js_transformer.transform(tree.children[0])
        while condition not in ['undefined', 'null', 'NaN', False, 0, ""]:
            val = self.visit(tree.children[1])
            condition = js_transformer.transform(tree.children[0])
        if type(val) == list:
            return val[-1]
        else:
            return val

    def ternary_condition_statement(self, tree):
        condition = js_transformer.transform(tree.children[0])
        if condition not in ['undefined', 'null', 'NaN', False, 0, ""]:
            true_branch = self.visit(tree.children[1])
            if type(true_branch) == list:
                raise Exception('SyntaxError: Unexpected token')
            else:
                return true_branch
        else:
            false_branch = self.visit(tree.children[2])
            if type(false_branch) == list:
                raise Exception('SyntaxError: Unexpected token')
            else:
                return false_branch

    def function_declaration(self, tree):
        declaration = tree.children[0]
        identifier = tree.children[1]
        if len(tree.children) == 5:
            parameter_list = []
            function_body = tree.children[4]  # it is a subtree
        else:
            if str(type(tree.children[3])) == "<class 'lark.lexer.Token'>":
                parameter_list = [tree.children[3]]
            elif str(type(tree.children[3])) == "<class 'lark.tree.Tree'>":
                parameter_list = tree.children[3].children
            function_body = tree.children[5]  # it is a subtree
        symbol_table.insert(identifier, {'declaration': declaration, 'parameter_list': parameter_list,
                                         'body': function_body, 'type': declaration})
        return 'undefined'

    def function_call(self, tree):
        identifier = tree.children[0]

        # take the argument list
        if len(tree.children) == 3:
            argument_list = []  # if there are no arguments
        elif len(tree.children[2].children) > 1:  # if there are more than one argument
            argument_list = js_transformer.transform(tree.children[2]).children
        else:  # if there is only one argument
            argument_list = [js_transformer.transform(tree.children[2])]

        function = symbol_table.find(identifier)
        try:
            if function['declaration'] == 'function':
                # take the parameter list
                parameter_list = function['parameter_list']
                # copy the global parameter
                temp = {}

                # take the function body
                function_body = function['body']

                for i in range(len(parameter_list)):
                    if parameter_list[i] in symbol_table.table.keys():
                        temp[parameter_list[i]] = deepcopy(symbol_table.table[parameter_list[i]])
                        symbol_table.update(parameter_list[i], {'declaration': 'var', 'value': argument_list[i], 'type': type(argument_list[i])})
                    else:
                        symbol_table.insert(parameter_list[i], {'declaration': 'var', 'value': argument_list[i], 'type': type(argument_list[i])})
                if function_body.data == 'block':
                    for i in range(len(function_body.children)):
                        if function_body.children[i].data == 'return_statement':
                            out = js_transformer.transform(function_body.children[i])
                            for key in temp.keys():
                                symbol_table.update(key, temp[key])
                            return out
                        else:
                            visited_body = self.visit(function_body.children[i])
                    for key in temp.keys():
                        symbol_table.update(key, temp[key])
                    return 'undefined'
                elif function_body.data == 'return_statement':
                    out = js_transformer.transform(function_body)
                    for key in temp.keys():
                        symbol_table.update(key, temp[key])
                    return out
                else:
                    visited_body = self.visit(function_body)
                for key in temp.keys():
                    symbol_table.update(key, temp[key])
                return 'undefined'
            else:
                raise IsNotAFunction
        except IsNotAFunction:
            print('TypeError: ' + identifier + ' is not a function')

    def return_statement(self, tree):
        return js_transformer.transform(tree)

    def print_statement(self, tree):
        return js_transformer.transform(tree)

    def input_statement(self, tree):
        return js_transformer.transform(tree)

    def variable_statement(self, tree):
        return js_transformer.transform(tree)

    def variable_assignment(self, tree):
        return js_transformer.transform(tree)

    def logical_and(self, tree):
        return js_transformer.transform(tree)

    def logical_or(self, tree):
        return js_transformer.transform(tree)

    def equality(self, tree):
        return js_transformer.transform(tree)

    def inequality(self, tree):
        return js_transformer.transform(tree)

    def strict_equality(self, tree):
        return js_transformer.transform(tree)

    def strict_inequality(self, tree):
        return js_transformer.transform(tree)

    def greater_than(self, tree):
        return js_transformer.transform(tree)

    def greater_than_or_equal(self, tree):
        return js_transformer.transform(tree)

    def less_than(self, tree):
        return js_transformer.transform(tree)

    def less_than_or_equal(self, tree):
        return js_transformer.transform(tree)

    def add(self, tree):
        return js_transformer.transform(tree)

    def sub(self, tree):
        return js_transformer.transform(tree)

    def mul(self, tree):
        return js_transformer.transform(tree)

    def div(self, tree):
        return js_transformer.transform(tree)

    def negative(self, tree):
        return js_transformer.transform(tree)

    def logical_not(self, tree):
        return js_transformer.transform(tree)

    def template_literal(self, tree):
        return js_transformer.transform(tree)

    def factor(self, tree):
        return js_transformer.transform(tree)

    def term(self, tree):
        return js_transformer.transform(tree)

    def expression(self, tree):
        return js_transformer.transform(tree)

    def array(self, tree):
        return js_transformer.transform(tree)

    def array_access(self, tree):
        return js_transformer.transform(tree)
