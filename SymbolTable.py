# The symbol table is organized as a dictionary, where the keys are the variable identifiers and the values are the attributes
from error_handling import *



class SymbolTable:
    def __init__(self, initial_state={}):
        self.table = initial_state

    def insert(self, identifier, attributes):
        """
        Inserts a new identifier in the symbol table
        :param identifier: JavaScript variable binding
        :param attributes: can be another dictionary, containing the variable attributes
        :return:
        """
        if attributes['type']:
            if attributes['type'] == float:
                attributes['type'] = 'Number'
            elif attributes['type'] == str:
                attributes['type'] = 'String'
            elif attributes['type'] == bool:
                attributes['type'] = 'Boolean'
            elif attributes['type'] == list:
                attributes['type'] = 'Array'
        self.table[identifier] = attributes

    def find(self, identifier):
        """
        Retieves the attributes of the required identifier
        :param identifier:
        :return:
        """
        if identifier in self.table.keys():
            return self.table[identifier]
        else:
            raise ReferenceError

    def delete(self, identifier):
        """
        Deletes the required identifier from the symbol table
        :param identifier:
        :return:
        """
        del self.table[identifier]

    def update(self, identifier, attributes):
        """
        Updates the attributes of the required identifier
        :param identifier:
        :param attributes:
        :return:
        """
        if attributes['type']:
            if attributes['type'] == float:
                attributes['type'] = 'Number'
            elif attributes['type'] == str:
                attributes['type'] = 'String'
            elif attributes['type'] == bool:
                attributes['type'] = 'Boolean'
            elif attributes['type'] == list:
                attributes['type'] = 'Array'
        self.table[identifier] = attributes

symbol_table = SymbolTable()
