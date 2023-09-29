# From Lark's Documentation:
# The interpreter walks the tree starting at the root, it visits the tree from the root to the leaves (top-down).
# For each node it calls its methods (inherited) according to tree.data. Differently from transformer, the interpreter
# does not visit the sub branches, unless it is explicitly told to do so.

# Interpreter allows to implement branching and loops

from lark.visitors import Interpreter
from Transformer import TreeToJS, symbol_table
from SymbolTable import SymbolTable

js_transformer = TreeToJS()  # the transformer is used to visit the tree from the leaves to the root (bottom-up)

class JavaScriptInterpreter(Interpreter):

    def start(self, tree):
        return self.visit_children(tree)

    def if_statement(self, tree):
        pass

    def while_statement(self, tree):
        pass

    def function_declaration(self, tree):
        declaration = tree.children[0]
        identifier = tree.children[1]
        parameter_list = tree.children[3]
        function_body = tree.children[5]
        symbol_table.insert(identifier, {'declaration': declaration, 'parameter_list': parameter_list, 'body': function_body,
                                                 'type': declaration})
        return 'undefined'

    def function_call(self, tree):
        identifier = tree.children[0]
        argument_list = js_transformer.transform(tree.children[1]).children
        function = symbol_table.find(identifier)
        if function['declaration'] == 'function':
            function_body = function['body']
            parameter_list = function['parameter_list'].children
            for i in range(len(parameter_list)):
                symbol_table.insert(parameter_list[i], {'declaration': 'var', 'value': argument_list[i], 'type': type(argument_list[i])})
            return self.visit(function_body)
        else:
            raise Exception('TypeError: ' + identifier + ' is not a function')

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
