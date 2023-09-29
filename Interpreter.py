# From Lark's Documentation:
# The interpreter walks the tree starting at the root, it visits the tree from the root to the leaves (top-down).
# For each node it calls its methods (inherited) according to tree.data. Differently from transformer, the interpreter
# does not visit the sub branches, unless it is explicitly told to do so.

# Interpreter allows to implement branching and loops

from lark.visitors import Interpreter

class JavaScriptInterpreter(Interpreter):
    pass

# TODO capire cosa si trova all'interno di tree.data