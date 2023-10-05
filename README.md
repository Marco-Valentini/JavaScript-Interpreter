# JavaScript-Interpreter in Python
A JavaScript Interpreter coded in Python using Lark parsing and lexing library

Lark: https://lark-parser.readthedocs.io/en/stable/# \
JavaScript grammar reference: https://tc39.es/ecma262/ \
JavaScript Error Reference: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors?retiredLocale=it

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

### Relational Operations (with type coercion simulation)
- equal (==)
- not equal (!=)
- strict equal (===)
- strict not equal (!==)
- greater than (>)
- less than (<)
- greater than or equal to (>=)
- less than or equal to (<=)

### Assignment operations (with type coercion simulation)
- identifier += expression
- identifier -= expression
- identifier *= expression
- identifier /= expression
- identifier ++  (post-increment)
- ++ identifier  (pre-increment)
- identifier --  (post-decrement)
- -- identifier  (pre-decrement)

### Logical operations (with type coercion simulation)
- not (!)
- or (||)
- and (&&)

### Branching operations
- if
- if else
- ternary conditional operator (condition ? true : false)

### Loop operations
- while

### Input instruction
-  keyboard input (prompt)

### Output instruction:
- print in console (console.log)
- template literals

### Function declaration
- function IDENTIFIER (list_of_parameters) { body }

### Function call
- IDENTIFIER (list_of_arguments)

### Array
- array declaration
- array access (with integer index and non integer index)
- array length (length)

### Comments (ignored)
- single line comment (//)
- multi line comment (/* */)

### Managed errors
- Lexical errors (typing error)
- Syntax errors
    - non-matched parenthesis
    - identifier already declared
    - assignment to constant variable
    - redeclaration with different declaration type
    - reserved word used as identifier
    - unexpected end of input
    - missing equal sign in constant declaration
  
- Semantic errors
    - reference error
    - type error

### Tests (folder javascript_tests)
The following test scripts are available:
- `test_1.js`: test the arithmetic and the relational operations and the type coercion.
- `test_2.js`: test the function declaration and the function call and the array declaration, access and length.
- `test_3.js`: test the branching operations (if, if else) and the loop operations (while) and array declaration, access and length.
- `test_4.js`: generate a lexical errors.
- `test_5.js`: generate a syntax errors.
- `test_6.js`: generate a semantic error.
- `test_7.js`: generate a type error.

## Instructions to run the interpreter
1. clone the repository or download the project
2. install python (our python version: 3.8)
3. install lark library: `pip install lark` (our version: 1.1.7)
### Script execution
1. open a terminal
2. go to the project folder
3. run the script: `python main.py -s (--script) <path_to_script>`
4. the output will be printed in the terminal
### Console execution
1. open a terminal
2. go to the project folder
3. run the script: `python main.py -c (--console)` or `python main.py`
4. write the script in the console
5. press enter
6. the output will be printed in the terminal

For both the execution modes, if you specify the flag `-d (--debug)` the debug mode will be activated and the Parse Tree will be printed in the terminal.