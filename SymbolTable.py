# The symbol table is organized as a dictionary,
# where the keys are the variable identifiers and the values are the attributes
from error_handling import *


class SymbolTable:
    def __init__(self, initial_state=None, parent=None):
        if initial_state is None:
            initial_state = {} # symbol table is organized as a dictionary
        self.table = initial_state
        self.parent = parent

    def insert(self, identifier, attributes):
        """
        Inserts a new identifier in the symbol table
        :param identifier: JavaScript variable binding
        :param attributes: can be another dictionary, containing the variable attributes
        :return: None
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

    def exist(self, identifier):
        """
        Checks if the required identifier exists in the symbol table
        :param identifier: JavaScript variable binding
        :return: True if the identifier exists, False otherwise
        """
        # search in the current symbol table, if not search in the parent symbol table until the root
        if identifier in self.table.keys():
            return True
        elif self.parent is not None:
            return self.parent.exist(identifier)
        else:
            return False

    def find(self, identifier):
        """
        Retrieves the attributes of the required identifier
        :param identifier: JavaScript variable binding
        :return: the attributes of the required identifier
        """
        # search in the current symbol table, if not search in the parent symbol table until the root
        if identifier in self.table.keys():
            return self.table[identifier]
        elif self.parent is not None:
            return self.parent.find(identifier)
        else:
            raise ReferenceError

    def delete(self, identifier):
        """
        Deletes the required identifier from the symbol table
        :param identifier: JavaScript variable binding
        :return: None
        """
        # search in the current symbol table, if not search in the parent symbol table until the root
        if identifier in self.table.keys():
            del self.table[identifier]
        elif self.parent is not None:
            self.parent.delete(identifier)
        else:
            raise ReferenceError

    def update(self, identifier, attributes):
        """
        Updates the attributes of the required identifier
        :param identifier: JavaScript variable binding
        :param attributes: can be another dictionary, containing the variable attributes
        :return: None
        """
        # assign the corresponding JavaScript type to the variable
        if attributes['type']:
            if attributes['type'] == float:
                attributes['type'] = 'Number'
            elif attributes['type'] == str:
                attributes['type'] = 'String'
            elif attributes['type'] == bool:
                attributes['type'] = 'Boolean'
            elif attributes['type'] == list:
                attributes['type'] = 'Array'
        # search in the current symbol table, if not search in the parent symbol table until the root
        if identifier in self.table.keys():
            self.table[identifier] = attributes
        elif self.parent is not None:
            self.parent.update(identifier, attributes)
        else:
            raise ReferenceError

# create an instance of symbol table
symbol_table = SymbolTable()
