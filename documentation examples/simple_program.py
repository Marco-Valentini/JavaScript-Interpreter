from lark import Lark

l = Lark('''start: sentence
            punteggiature: "," | "!"
            sentence : word+ punteggiature word+ punteggiature
            word:WORD
            
            %import common.WORD   // imports from terminal library
            %ignore " "           // Disregard spaces in text
         ''') # this is the parser

print(l.parse("Hello, World!") ) # this is the parser in action
