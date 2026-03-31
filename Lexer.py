# Converts text into tokens.
# Author: Evan Cassidy
# Date: 3/31/2026

class Tokens:
    KEYWORD = 'KEYWORD'
    LITERAL = 'LITERAL'
    IDENTIFIER = 'IDENTIFIER'
    OPERATOR = 'OPERATOR'
    DELIMITER = 'DELIMITER'
    EOL = 'EOL'
    EOF = 'EOF'

class Types:
    NONE = 'NONE'

    KEYWORD_DEF = 'DEF'
    KEYWORD_RETURN = 'RETURN'
    KEYWORD_IF = 'IF'
    KEYWORD_ELIF = 'ELIF'
    KEYWORD_ELSE = 'ELSE'
    KEYWORD_WHILE = 'WHILE'

    LITERAL_STRING = 'STRING'
    LITERAL_INTEGER = 'INTEGER'
    LITERAL_FLOAT = 'FLOAT'
    LITERAL_BOOL = 'BOOL'
    LITERAL_NONE = 'NONE'

    OPERATOR_EQUAL = 'EQUAL'
    OPERATOR_ADD = 'ADD'
    OPERATOR_SUBTRACT = 'SUBTRACT'
    OPERATOR_MULTIPLY = 'MULTIPLY'
    OPERATOR_DIVIDE = 'DIVIDE'
    OPERATOR_MODULO = 'MODULO'

    OPERATOR_ADDEQUAL = 'ADDEQUAL'
    OPERATOR_SUBTRACTEQUAL = 'SUBTRACTEQUAL'
    OPERATOR_MULTIPLYEQUAL = 'MULTIPLYEQUAL'
    OPERATOR_DIVIDEEQUAL = 'DIVIDEEQUAL'
    OPERATOR_MODULOEQUAL = 'MODULOEQUAL'

    OPERATOR_LESS = 'LESS'
    OPERATOR_GREATER = 'GREATER'
    OPERATOR_LESSEQUAL = 'LESSEQUAL'
    OPERATOR_GREATEREQUAL = 'GREATEREQUAL'
    OPERATOR_NOTEQUAL = 'NOTEQUAL'
    OPERATOR_EQUALEQUAL = 'EQUALEQUAL'

    DELIMITER_LPAREN = 'LPAREN'
    DELIMITER_RPAREN = 'RPAREN'
    DELIMITER_COLON = 'COLON'
    DELIMITER_COMMA = 'COMMA'
    DELIMITER_TAB = 'TAB'

class Token:
    def __init__(self, type: str, subtype: str, value, line: int) -> 'Token':
        self.type = type
        self.subtype = subtype
        self.value = value
        self.line = line
    def __str__(self):
        if self.type in [Tokens.LITERAL]:
            return f'[{self.type}.{self.subtype}({self.value}) @ Line {self.line}]'
        elif self.type in [Tokens.KEYWORD, Tokens.OPERATOR, Tokens.DELIMITER]:
            return f'[{self.type}.{self.subtype} @ Line {self.line}]'
        elif self.type in [Tokens.EOL, Tokens.EOF]:
            return f'[{self.type} @ Line {self.line}]'
        elif self.type in [Tokens.IDENTIFIER]:
            return f'[{self.type}({self.value}) @ Line {self.line}]'
        else:
            return f'[UNKNOWN.{self.subtype}({self.value}) @ Line {self.line}]'
    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text: str) -> 'Lexer':
        self.text = text
        self.tokens = []

    # Scans text into temp tokens
    def scan(self) -> None:

        # Dictionary
        dictionary_breaks = ' =+-*/%(),\n'

        # Current working string
        current = ''

        # Iterate
        i = 0
        line = 0
        cons_space = 0
        while i < len(self.text):

            char = self.text[i]

            if char in dictionary_breaks:
                
                if len(current) != 0:
                    self.tokens.append(Token('temp', None, current, line))
                    current = ''

                if char != ' ':
                    self.tokens.append(Token('temp', None, char, line))

            else:
                current += char

            if char == '\n':
                line += 1

            if char == ' ':
                cons_space += 1
            else:
                cons_space = 0

            if cons_space == 4:
                self.tokens.append(Token(Tokens.DELIMITER, Types.DELIMITER_TAB, None, line))
                cons_space = 0

            i += 1

        # EOF
        self.tokens.append(Token(Tokens.EOF, Types.NONE, None, line))

    # Pattern matches temp tokens into meaningful tokens
    def match(self):

        keywords = {
            'def': Types.KEYWORD_DEF,
            'return': Types.KEYWORD_RETURN,
            'if': Types.KEYWORD_IF,
            'elif': Types.KEYWORD_ELIF,
            'else': Types.KEYWORD_ELSE,
            'while': Types.KEYWORD_WHILE
        }

        operators = {
            '=': Types.OPERATOR_EQUAL, 
            '+': Types.OPERATOR_ADD, 
            '-': Types.OPERATOR_SUBTRACT, 
            '*': Types.OPERATOR_MULTIPLY, 
            '/': Types.OPERATOR_DIVIDE, 
            '%': Types.OPERATOR_MODULO, 

            '+=': Types.OPERATOR_ADDEQUAL, 
            '-=': Types.OPERATOR_SUBTRACTEQUAL, 
            '*=': Types.OPERATOR_MULTIPLYEQUAL, 
            '/=': Types.OPERATOR_DIVIDEEQUAL, 
            '%=': Types.OPERATOR_MODULOEQUAL, 

            '<': Types.OPERATOR_LESS, 
            '>': Types.OPERATOR_GREATER, 
            '<=': Types.OPERATOR_LESSEQUAL, 
            '>=': Types.OPERATOR_GREATEREQUAL, 
            '!=': Types.OPERATOR_NOTEQUAL, 
            '==': Types.OPERATOR_EQUALEQUAL, 
        }

        delimiters = {
            '(': Types.DELIMITER_LPAREN,
            ')': Types.DELIMITER_RPAREN,
            ':': Types.DELIMITER_COLON,
            ',': Types.DELIMITER_COMMA,
        }

        # string integer float bool
        def is_string(val):
            if val[0] == val[-1] == '"':
                return True
            else:
                return False
        
        def is_integer(val):
            return val.lstrip('+-').isdigit()
        
        def is_float(val):
            return val.lstrip('+-').replace('.','').isdigit()
        
        def is_bool(val):
            return val in ['True', 'False']

        for token in self.tokens:
            if token.type == 'temp':

                if token.value in keywords:
                    token.type = Tokens.KEYWORD
                    token.subtype = keywords[token.value]
                    token.value = None

                elif token.value in operators:
                    token.type = Tokens.OPERATOR
                    token.subtype = operators[token.value]
                    token.value = None

                elif token.value == '\n':
                    token.type = Tokens.EOL
                    token.subtype = None
                    token.value = None

                elif token.value in delimiters:
                    token.type = Tokens.DELIMITER
                    token.subtype = delimiters[token.value]
                    token.value = None

                elif is_string(token.value):
                    token.type = Tokens.LITERAL
                    token.subtype = Types.LITERAL_STRING
                    token.value = token.value[1:-1]
                
                elif is_integer(token.value):
                    token.type = Tokens.LITERAL
                    token.subtype = Types.LITERAL_INTEGER
                    token.value = int(token.value)

                elif is_float(token.value):
                    token.type = Tokens.LITERAL
                    token.subtype = Types.LITERAL_FLOAT
                    token.value = float(token.value)

                elif is_bool(token.value):
                    token.type = Tokens.LITERAL
                    token.subtype = Types.LITERAL_BOOL
                    token.value = True if token.value == 'True' else False

                else:
                    token.type = Tokens.IDENTIFIER
                    token.subtype = Types.NONE

    # scan + match
    def analyze(self):
        self.scan()
        self.match()