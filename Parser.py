# Converts tokens into AST.
# Author: Evan Cassidy
# Date: 3/31/2026

from Lexer import TokenTypes, TokenSubtypes, Token

class Nodes:

    # Statements
    ASSIGNMENT = 'ASSIGNMENT'

    # Expressions
    BINARY = 'BINARY'

    # Objects
    LITERAL = 'LITERAL'
    IDENTIFIER = 'IDENTIFIER'

class Node:
    def __init__(self, type: str):
        self.type = type
    def __str__(self):
        return f'{self.type}'
    def __repr__(self):
        return self.__str__()

class NodeAssignment(Node):
    def __init__(self, var: str, expr: Node):
        super().__init__(Nodes.ASSIGNMENT)
        self.var = var
        self.expr = expr
    def __str__(self):
        return f'{self.var} = {self.expr}'
    def __repr__(self):
        return self.__str__()

class NodeBinary(Node):
    def __init__(self, left: Node, operation: TokenSubtypes, right: Node):
        super().__init__(Nodes.BINARY)
        self.left = left
        self.operation = operation
        self.right = right
    def __str__(self):
        return f'{self.left} {self.operation} {self.right}'
    def __repr__(self):
        return self.__str__()

class NodeLiteral(Node):
    def __init__(self, type: str, value):
        super().__init__(Nodes.LITERAL)
        self.type = type
        self.value = value
    def __str__(self):
        return f'{self.value}'
    def __repr__(self):
        return self.__str__()

class NodeIdentifier(Node):
    def __init__(self, id: str):
        super().__init__(Nodes.IDENTIFIER)
        self.id = id
    def __str__(self):
        return f'{self.id}'
    def __repr__(self):
        return self.__str__()


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0
        self.nodes = []

    def peek(self, n: int = 0) -> Token:
        return self.tokens[self.pos + n]
    
    def consume(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    
    def parse(self) -> None:
        while self.peek().type != TokenTypes.EOF:
            self.nodes.append(self.ParseStatement())
    
    def ParseStatement(self) -> Node:
        
        # Assignment
        if self.peek().type == TokenTypes.IDENTIFIER and self.peek(1).subtype == TokenSubtypes.OPERATOR_EQUAL:
            return self.ParseAssignment()
        
        # New Line
        elif self.peek().type == TokenTypes.EOL:
            self.consume() # consume past EOL

        # Unknown Statement
        else:
            raise SyntaxError("Unknown statement!")
        
    def ParseExpression(self) -> Node:
        return self.ParseExpressionLevelTwo()


    # Values parsed here
    def ParseExpressionLevelZero(self) -> Node:

        # Token
        token = self.consume()

        # Literal
        if token.type == TokenTypes.LITERAL:
            return NodeLiteral(token.subtype, token.value)
        
        # Identifier
        if token.type == TokenTypes.IDENTIFIER:
            return NodeIdentifier(token.value)
        
        # Parentheses
        if token.subtype == TokenSubtypes.DELIMITER_LPAREN:
            node = self.ParseExpression()
            self.consume() # )
            return node

        
    # * / % parsed here
    def ParseExpressionLevelOne(self) -> Node:

        node = self.ParseExpressionLevelZero()

        while self.peek().subtype in [TokenSubtypes.OPERATOR_MULTIPLY, TokenSubtypes.OPERATOR_DIVIDE, TokenSubtypes.OPERATOR_MODULO]:
            left = node
            op = self.consume().subtype
            right = self.ParseExpressionLevelZero()
            node = NodeBinary(left, op, right)

        return node
    
    # + - parsed here
    def ParseExpressionLevelTwo(self) -> Node:

        node = self.ParseExpressionLevelOne()

        while self.peek().subtype in [TokenSubtypes.OPERATOR_ADD, TokenSubtypes.OPERATOR_SUBTRACT]:
            left = node
            op = self.consume().subtype
            right = self.ParseExpressionLevelOne()
            node = NodeBinary(left, op, right)

        return node
    
    def ParseAssignment(self) -> Node:
        
        var = self.consume().value

        self.consume() # =

        expr = self.ParseExpression()

        self.consume() # new line

        return NodeAssignment(var, expr)
