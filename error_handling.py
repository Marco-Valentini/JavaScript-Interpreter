# Reserved javascript keywords
reserved_words = ['break', 'case', 'catch', 'class', 'const', 'continue', 'debugger', 'default', 'delete', 'do',
                  'else', 'export', 'extends', 'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof',
                  'new', 'return', 'super', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void', 'while',
                  'with', 'yield']


# syntax error are handled with Python SyntaxError exception
class JavaScriptSyntaxError(SyntaxError):
    def __str__(self):  # taken from lark documentation
        context, line, column = self.args
        return '%s at line %s, column %s.\n\n%s' % (self.label, line, column, context)


class UnmatchedParenthesisError(JavaScriptSyntaxError):
    pass


class MissingClosingParenthesisInArgumentList(UnmatchedParenthesisError):
    label = 'Syntax Error: Missing ) in argument list'


class MissingClosingParenthesisAfterCondition(UnmatchedParenthesisError):
    label = 'Syntax Error: Missing ) after condition'


class MissingClosingParenthesisAfterElementList(UnmatchedParenthesisError):
    label = 'Syntax Error: Missing ] after element list'


class MissingClosingParenthesisAfterFunctionBody(UnmatchedParenthesisError):
    label = 'Syntax Error: Missing } after function body'


class MissingEqualInConstDeclaration(JavaScriptSyntaxError):
    label = 'Syntax Error: Missing = in const declaration'


class UnexpectedEndOfInput(JavaScriptSyntaxError):
    label = 'Syntax Error: Unexpected end of input'


class IdentifierAlreadyDeclared(JavaScriptSyntaxError):
    pass


class ReservedWordAsIdentifier(JavaScriptSyntaxError):
    pass


# semantic error are handled with Python Exception class
class JavaScriptSemanticError(Exception):
    pass


class ReferenceError(JavaScriptSemanticError):
    pass


class IsNotAFunction(JavaScriptSemanticError):
    pass


class ConstAssignmentTypeError(JavaScriptSemanticError):
    pass
