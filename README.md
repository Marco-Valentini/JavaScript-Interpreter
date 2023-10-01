# JavaScript-Interpreter in Python
A JavaScript Interpreter coded in Python using Lark parsing and lexing library

Lark: https://lark-parser.readthedocs.io/en/stable/# \
Chosen starting JavaScript grammar: https://tc39.es/ecma262/ \
Error Reference: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors?retiredLocale=it

## Restriction of the grammar adopted 
### Data types
- Number
- Boolean
- String
- Array

### Arithmetic Operations (with type coercion simulation)
- addition (+)
- subtraction (-)
- multiplication (*)
- division (/)

### Arithmetic Operations (with type coercion simulation)
- equal (==)
- not equal (!=)
- strict equal (===)
- strict not equal (!==)
- greater than (>)
- less than (<)
- greater than or equal to (>=)
- less than or equal to (<=)

### Assignment operations
- identifier += expression
- identifier -= expression
- identifier *= expression
- identifier /= expression
- identifier ++
- ++ identifier
- identifier --
- -- identifier

### Logical operations (with type coercion simulation)
- not (!)
- or (||)
- and (&&)

### Branching operations
- if
- if else
- operatore condizionale ternario (condition ? true : false)

### Loop operations
- while

### Input instruction
-  keyboard input (prompt)

### Output instruction:
- print in console (console.log)
- template literals

### Function declaration
- function ID (parameters) { body }

### Function call
- ID (arguments)

### Array
- array declaration
- array access

### Handled errors
- lexical errors (typing errors)
- syntax error
    - non-matched parenthesis
- semantic errors
    - Reference error
