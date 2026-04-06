# Converts text into tokens.
# Author: Evan Cassidy
# Date: 3/31/2026

class TokenTypes:
    KEYWORD = 'KEYWORD'
    LITERAL = 'LITERAL'
    IDENTIFIER = 'IDENTIFIER'
    OPERATOR = 'OPERATOR'
    DELIMITER = 'DELIMITER'
    EOL = 'EOL'
    EOF = 'EOF'

class TokenSubtypes:
    NONE = 'NONE'

    KEYWORD_DEF = 'DEF'
    KEYWORD_RETURN = 'RETURN'
    KEYWORD_IF = 'IF'
    KEYWORD_ELIF = 'ELIF'
    KEYWORD_ELSE = 'ELSE'
    KEYWORD_WHILE = 'WHILE'
    KEYWORD_CLASS = 'CLASS'
    KEYWORD_FOR = 'FOR'
    KEYWORD_IN = 'IN'
    KEYWORD_IMPORT = 'IMPORT'
    KEYWORD_FROM = 'FROM'
    KEYWORD_ARROW = 'ARROW'
    KEYWORD_CONTINUE = 'CONTINUE'

    LITERAL_STRING = 'STRING'
    LITERAL_INTEGER = 'INTEGER'
    LITERAL_FLOAT = 'FLOAT'
    LITERAL_BOOL = 'BOOL'
    LITERAL_NONE = 'NONE'
    LITERAL_FSTRING = 'FSTRING'

    OPERATOR_EQUAL = 'EQUAL'
    OPERATOR_ADD = 'ADD'
    OPERATOR_SUBTRACT = 'SUBTRACT'
    OPERATOR_MULTIPLY = 'MULTIPLY'
    OPERATOR_DIVIDE = 'DIVIDE'
    OPERATOR_MODULO = 'MODULO'
    OPERATOR_EXPONENT = 'EXPONENT'
    OPERATOR_AND = 'AND'
    OPERATOR_OR = 'OR'

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
    OPERATOR_IN = 'IN'

    OPERATOR_NOT = 'NOT'

    DELIMITER_COMMENT = 'COMMENT'
    DELIMITER_LPAREN = 'LPAREN'
    DELIMITER_RPAREN = 'RPAREN'
    DELIMITER_LSQUARE = 'LSQUARE'
    DELIMITER_RSQUARE = 'RSQUARE'
    DELIMITER_LBRACE = 'LBRACE'
    DELIMITER_RBRACE = 'RBRACE'
    DELIMITER_COLON = 'COLON'
    DELIMITER_COMMA = 'COMMA'
    DELIMITER_DOT = 'DOT'
    DELIMITER_TAB = 'TAB'

class Token:
    def __init__(self, type: str, subtype: str, value, line: int) -> 'Token':
        self.type = type
        self.subtype = subtype
        self.value = value
        self.line = line
    def __str__(self):
        if self.type in [TokenTypes.LITERAL]:
            return f'[{self.type}.{self.subtype}({self.value}) @ Line {self.line}]'
        elif self.type in [TokenTypes.KEYWORD, TokenTypes.OPERATOR, TokenTypes.DELIMITER]:
            return f'[{self.type}.{self.subtype} @ Line {self.line}]'
        elif self.type in [TokenTypes.EOL, TokenTypes.EOF]:
            return f'[{self.type} @ Line {self.line}]'
        elif self.type in [TokenTypes.IDENTIFIER]:
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
        dictionary_breaks = ' #()[]{}:,.\n'

        # Current working string
        current = ''
        bs = False

        # Iterate
        i = 0
        line = 1
        cons_space = 0
        while i < len(self.text):

            char = self.text[i]

            if char in dictionary_breaks and not bs:
                
                if len(current) != 0:
                    self.tokens.append(Token('temp', None, current, line))
                    current = ''

                if char != ' ':
                    self.tokens.append(Token('temp', None, char, line))

            else:
                current += char

            if char == '\n' and not bs:
                line += 1

            if char == ' ' and not bs:
                cons_space += 1
            else:
                cons_space = 0

            if char == chr(39):
                bs = not bs

            if cons_space == 4:
                self.tokens.append(Token(TokenTypes.DELIMITER, TokenSubtypes.DELIMITER_TAB, None, line))
                cons_space = 0

            i += 1

        # EOL + EOF
        self.tokens.append(Token(TokenTypes.EOL, TokenSubtypes.NONE, None, line))
        self.tokens.append(Token(TokenTypes.EOF, TokenSubtypes.NONE, None, line))

    # Pattern matches temp tokens into meaningful tokens
    def match(self):

        keywords = {
            'def': TokenSubtypes.KEYWORD_DEF,
            'return': TokenSubtypes.KEYWORD_RETURN,
            'if': TokenSubtypes.KEYWORD_IF,
            'elif': TokenSubtypes.KEYWORD_ELIF,
            'else': TokenSubtypes.KEYWORD_ELSE,
            'while': TokenSubtypes.KEYWORD_WHILE,
            'class': TokenSubtypes.KEYWORD_CLASS,
            'for': TokenSubtypes.KEYWORD_FOR,
            'in': TokenSubtypes.KEYWORD_IN,
            'import': TokenSubtypes.KEYWORD_IMPORT,
            'from': TokenSubtypes.KEYWORD_FROM,
            '->': TokenSubtypes.KEYWORD_ARROW,
            'continue': TokenSubtypes.KEYWORD_CONTINUE
        }

        operators = {
            '=': TokenSubtypes.OPERATOR_EQUAL, 
            '+': TokenSubtypes.OPERATOR_ADD, 
            '-': TokenSubtypes.OPERATOR_SUBTRACT, 
            '*': TokenSubtypes.OPERATOR_MULTIPLY, 
            '/': TokenSubtypes.OPERATOR_DIVIDE, 
            '%': TokenSubtypes.OPERATOR_MODULO, 
            '**': TokenSubtypes.OPERATOR_EXPONENT,

            '+=': TokenSubtypes.OPERATOR_ADDEQUAL, 
            '-=': TokenSubtypes.OPERATOR_SUBTRACTEQUAL, 
            '*=': TokenSubtypes.OPERATOR_MULTIPLYEQUAL, 
            '/=': TokenSubtypes.OPERATOR_DIVIDEEQUAL, 
            '%=': TokenSubtypes.OPERATOR_MODULOEQUAL, 

            '<': TokenSubtypes.OPERATOR_LESS, 
            '>': TokenSubtypes.OPERATOR_GREATER, 
            '<=': TokenSubtypes.OPERATOR_LESSEQUAL, 
            '>=': TokenSubtypes.OPERATOR_GREATEREQUAL, 
            '!=': TokenSubtypes.OPERATOR_NOTEQUAL, 
            '==': TokenSubtypes.OPERATOR_EQUALEQUAL,
            'in': TokenSubtypes.OPERATOR_IN,
            'not': TokenSubtypes.OPERATOR_NOT,
            'and': TokenSubtypes.OPERATOR_AND,
            'or': TokenSubtypes.OPERATOR_OR
        }

        delimiters = {
            '#': TokenSubtypes.DELIMITER_COMMENT,
            '(': TokenSubtypes.DELIMITER_LPAREN,
            ')': TokenSubtypes.DELIMITER_RPAREN,
            '[': TokenSubtypes.DELIMITER_LSQUARE,
            ']': TokenSubtypes.DELIMITER_RSQUARE,
            '{': TokenSubtypes.DELIMITER_LBRACE,
            '}': TokenSubtypes.DELIMITER_RBRACE,
            ':': TokenSubtypes.DELIMITER_COLON,
            ',': TokenSubtypes.DELIMITER_COMMA,
            '.': TokenSubtypes.DELIMITER_DOT
        }

        # string integer float bool
        def is_string(val):
            return val[0] == val[-1] == chr(39)
            
        def is_fstring(val):
            if len(val) < 3:
                return False
            else:
                return val[0] == 'f' and val[1] == val[-1] == chr(39)
        
        def is_integer(val):
            return val.lstrip('+-').isdigit()
        
        def is_float(val):
            return val.lstrip('+-').replace('.','').isdigit()
        
        def is_bool(val):
            return val in ['True', 'False']

        for token in self.tokens:
            if token.type == 'temp':

                if token.value in keywords:
                    token.type = TokenTypes.KEYWORD
                    token.subtype = keywords[token.value]
                    token.value = None

                elif token.value in operators:
                    token.type = TokenTypes.OPERATOR
                    token.subtype = operators[token.value]
                    token.value = None

                elif token.value == '\n':
                    token.type = TokenTypes.EOL
                    token.subtype = None
                    token.value = None

                elif token.value in delimiters:
                    token.type = TokenTypes.DELIMITER
                    token.subtype = delimiters[token.value]
                    token.value = None

                elif is_string(token.value):
                    token.type = TokenTypes.LITERAL
                    token.subtype = TokenSubtypes.LITERAL_STRING
                    token.value = token.value

                elif is_fstring(token.value):
                    token.type = TokenTypes.LITERAL
                    token.subtype = TokenSubtypes.LITERAL_FSTRING
                    token.value = token.value

                elif is_integer(token.value):
                    token.type = TokenTypes.LITERAL
                    token.subtype = TokenSubtypes.LITERAL_INTEGER
                    token.value = int(token.value)

                elif is_float(token.value):
                    token.type = TokenTypes.LITERAL
                    token.subtype = TokenSubtypes.LITERAL_FLOAT
                    token.value = float(token.value)

                elif is_bool(token.value):
                    token.type = TokenTypes.LITERAL
                    token.subtype = TokenSubtypes.LITERAL_BOOL
                    token.value = token.value == 'True'

                else:
                    token.type = TokenTypes.IDENTIFIER
                    token.subtype = TokenSubtypes.NONE

    # scan + match
    def analyze(self):
        self.scan()
        self.match()