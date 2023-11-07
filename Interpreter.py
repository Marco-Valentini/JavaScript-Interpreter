# From Lark's Documentation:
# The interpreter walks the tree starting at the root, it visits the tree from the root to the leaves (top-down).
# For each node it calls its methods (inherited) according to tree.data. Differently from transformer, the interpreter
# does not automatically visit the sub-branches, unless it is explicitly told to do so.
from copy import deepcopy

# Interpreter allows to implement branching, loops and functions
from lark.visitors import Interpreter
from Transformer import TreeToJS
from SymbolTable import symbol_table, SymbolTable
from error_handling import *

# the transformer is used to visit the tree from the leaves to the root (bottom-up)
js_transformer = TreeToJS(symbol_table=symbol_table)

js_falsy_values = ['undefined', 'null', 'NaN', False, 0, "", "0"]

class JavaScriptInterpreter(Interpreter):

    def start(self, tree):
        return self.visit_children(tree)

    def if_statement(self, tree):
        condition = js_transformer.transform(tree.children[0])
        if condition not in js_falsy_values:  # JavaScript falsy values
            true_branch = self.visit(tree.children[1])  # visit the true branch
            if not true_branch:
                return 'undefined'
            elif type(true_branch) == list:
                return true_branch[-1]
            else:
                return true_branch
        elif len(tree.children) == 3:  # if there is else branch
            false_branch = self.visit(tree.children[2])  # visit the false branch
            if not false_branch:
                return 'undefined'
            elif type(false_branch) == list:
                return false_branch[-1]
            else:
                return false_branch

    def while_statement(self, tree):
        condition = js_transformer.transform(tree.children[0])
        while condition not in js_falsy_values:  # JavaScript falsy values
            val = self.visit(tree.children[1])
            condition = js_transformer.transform(tree.children[0]) # update the condition
        if type(val) == list:
            return val[-1]
        else:
            return val

    def ternary_condition_statement(self, tree):
        condition = js_transformer.transform(tree.children[0])
        if condition not in js_falsy_values:
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

    @staticmethod
    def function_declaration(tree):
        try:
            declaration = tree.children[0]
            identifier = tree.children[1]
            if identifier in reserved_words:
                raise ReservedWordAsIdentifier
            if len(tree.children) == 5:  # if there are no parameters
                parameter_list = []
                function_body = tree.children[4]  # it is a subtree
            else:
                if str(type(tree.children[3])) == "<class 'lark.lexer.Token'>":
                    parameter_list = [tree.children[3]]
                elif str(type(tree.children[3])) == "<class 'lark.tree.Tree'>":
                    parameter_list = tree.children[3].children
                function_body = tree.children[5]  # it is a subtree
            symbol_table.insert(identifier, {'declaration': declaration, 'parameter_list': parameter_list,
                                             'body': function_body, 'type': declaration}) # insert the function body a subtree to be evaluated later
            return 'undefined'
        except ReservedWordAsIdentifier:
            print('SyntaxError: Unexpected token ' + identifier)

    def function_call(self, tree):
        try:
            identifier = tree.children[0]

            # take the argument list
            if len(tree.children) == 3:
                argument_list = []  # if there are no arguments
            elif len(tree.children[2].children) > 1:  # if there are more than one argument
                argument_list = js_transformer.transform(tree.children[2]).children
            else:  # if there is only one argument convert to list to adapt to the interface used for other cases
                argument_list = [js_transformer.transform(tree.children[2])]
            # search for the function in the symbol table
            function = symbol_table.find(identifier)
            # check if the identifier is associated with function
            if function['declaration'] == 'function':
                # take the parameter list
                parameter_list = function['parameter_list']

                # create a new symbol table for the function
                new_symbol_table = SymbolTable(parent=deepcopy(js_transformer.symbol_table))

                # take the function body
                function_body = function['body']

                for i in range(len(parameter_list)):
                    # insert the parameter in the new symbol table
                    new_symbol_table.insert(parameter_list[i], {'declaration': 'var', 'value': argument_list[i],
                                                                'type': type(argument_list[i])})

                # update the symbol table of the transformer
                js_transformer.symbol_table = new_symbol_table

                if function_body.data == 'block':
                    for i in range(len(function_body.children)): # in case of a block, execute all the statements in it
                        if function_body.children[i].data == 'return_statement':
                            out = js_transformer.transform(function_body.children[i])
                            # update the symbol table of the transformer
                            js_transformer.symbol_table = deepcopy(new_symbol_table.parent)
                            return out
                        else:
                            visited_body = self.visit(function_body.children[i])
                    # update the symbol table of the transformer
                    js_transformer.symbol_table = deepcopy(new_symbol_table.parent)
                    return 'undefined'
                elif function_body.data == 'return_statement':
                    out = js_transformer.transform(function_body)
                    # update the symbol table of the transformer
                    js_transformer.symbol_table = deepcopy(new_symbol_table.parent)
                    return out
                else: # the body doesn't contain a return statement, neither a block
                    visited_body = self.visit(function_body)
                # update the symbol table of the transformer
                js_transformer.symbol_table = deepcopy(new_symbol_table.parent)
                return 'undefined'
            else:
                raise IsNotAFunction # the identifier is not associated with a function
        except IsNotAFunction:
            print('TypeError: ' + identifier + ' is not a function')
        except ReferenceError:
            print('ReferenceError: ' + identifier + ' is not defined')

    @staticmethod
    def return_statement(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def print_statement(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def input_statement(tree):
        return js_transformer.transform(tree)

    def variable_statement(self, tree):
        for i in range(len(tree.children)):
            if str(type(tree.children[i])) == "<class 'lark.tree.Tree'>":
                if tree.children[i].data == 'function_call':
                    tree.children[i] = self.visit(tree.children[i])  # this is required to assign the value of a function call to a variable
        return js_transformer.transform(tree)

    @staticmethod
    def variable_assignment(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def logical_and(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def logical_or(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def equality(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def inequality(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def strict_equality(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def strict_inequality(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def greater_than(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def greater_than_or_equal(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def less_than(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def less_than_or_equal(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def add(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def sub(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def mul(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def div(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def negative(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def logical_not(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def template_literal(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def factor(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def term(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def expression(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def array(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def array_access(tree):
        return js_transformer.transform(tree)

    @staticmethod
    def array_length(tree):
        return js_transformer.transform(tree)
