# Converts tokens into AST.
# Author: Evan Cassidy
# Date: 3/31/2026

from Lexer import TokenTypes, TokenSubtypes, Token

class Nodes:

    # Statements
    ASSIGNMENT = 'ASSIGNMENT'
    DEFINITION = 'DEFINITION'
    RETURN = 'RETURN'
    IF = 'IF'

    # Expressions
    BINARY = 'BINARY'
    CALL = 'CALL'

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
    
class NodeDefinition(Node):
    def __init__(self, func: str, args: list[str], body: list[Node]):
        super().__init__(Nodes.DEFINITION)
        self.func = func
        self.args = args
        self.body = body

class NodeCall(Node):
    def __init__(self, func: str, args: list[Node]):
        super().__init__(Nodes.CALL)
        self.func = func
        self.args = args

class NodeReturn(Node):
    def __init__(self, expr: Node):
        super().__init__(Nodes.RETURN)
        self.expr = expr

class NodeIf(Node):
    def __init__(self, cond: Node, body: list[Node]):
        super().__init__(Nodes.IF)
        self.cond = cond
        self.body = body

class NodeBinary(Node):
    def __init__(self, left: Node, operation: TokenSubtypes, right: Node):
        super().__init__(Nodes.BINARY)
        self.left = left
        self.operation = operation
        self.right = right

class NodeLiteral(Node):
    def __init__(self, value):
        super().__init__(Nodes.LITERAL)
        self.value = value

class NodeIdentifier(Node):
    def __init__(self, id: str):
        super().__init__(Nodes.IDENTIFIER)
        self.id = id

class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0
        self.nodes = []
        self.indents = 0

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
        
        # Definition
        if self.peek().type == TokenTypes.KEYWORD and self.peek().subtype == TokenSubtypes.KEYWORD_DEF:
            return self.ParseDefinition()
        
        # Return
        if self.peek().type == TokenTypes.KEYWORD and self.peek().subtype == TokenSubtypes.KEYWORD_RETURN:
            return self.ParseReturn()
        
        # If
        if self.peek().type == TokenTypes.KEYWORD and self.peek().subtype == TokenSubtypes.KEYWORD_IF:
            return self.ParseIf()
        
        # New Line
        if self.peek().type == TokenTypes.EOL:
            self.consume() # consume EOL
            return None

        # Unknown Statement
        raise SyntaxError(f'Unexpected {self.peek().type}, {self.peek().subtype}.')
        
    def ParseExpression(self) -> Node:
        return self.ParseExpressionLevelTwo()


    # Values parsed here
    def ParseExpressionLevelZero(self) -> Node:

        # Token
        token = self.consume()

        # Call
        if token.type == TokenTypes.IDENTIFIER and self.peek().subtype == TokenSubtypes.DELIMITER_LPAREN:
            print('function call found')
            func = token.value
            self.consume() # (
            args = []
            while self.peek().subtype != TokenSubtypes.DELIMITER_RPAREN:
                if len(args) != 0:
                    self.consume() # ,
                args.append(self.ParseExpression())
            self.consume() # )
            return NodeCall(func, args)
            
        # Literal
        if token.type == TokenTypes.LITERAL:
            return NodeLiteral(token.value)
        
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

        while self.peek().subtype in [
            TokenSubtypes.OPERATOR_MULTIPLY,
            TokenSubtypes.OPERATOR_DIVIDE,
            TokenSubtypes.OPERATOR_MODULO
        ]:
            left = node
            op = self.consume().subtype
            right = self.ParseExpressionLevelZero()
            node = NodeBinary(left, op, right)

        return node
    
    # + - parsed here
    def ParseExpressionLevelTwo(self) -> Node:

        node = self.ParseExpressionLevelOne()

        while self.peek().subtype in [
            TokenSubtypes.OPERATOR_ADD,
            TokenSubtypes.OPERATOR_SUBTRACT,
            TokenSubtypes.OPERATOR_LESS,
            TokenSubtypes.OPERATOR_GREATER,
            TokenSubtypes.OPERATOR_LESSEQUAL,
            TokenSubtypes.OPERATOR_GREATEREQUAL,
            TokenSubtypes.OPERATOR_NOTEQUAL,
            TokenSubtypes.OPERATOR_EQUALEQUAL
        ]:
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
    
    def ParseDefinition(self) -> Node:

        self.consume() # def

        func = self.consume().value

        self.consume() # (

        args = []
        while self.peek().subtype != TokenSubtypes.DELIMITER_RPAREN:
            if len(args) != 0:
                self.consume() # ,
            args.append(self.consume().value)
        
        self.consume() # )
        
        self.consume() # :

        self.consume() # new line

        self.indents += 1
        body = []
        while self.GetLeadingTabs() == self.indents:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            body.append(self.ParseStatement()) # consumes new lines
        self.indents -= 1

        return NodeDefinition(func, args, body)

    def ParseReturn(self) -> Node:

        self.consume() # return

        expr = self.ParseExpression()

        self.consume() # new line

        return NodeReturn(expr)
    
    def ParseIf(self) -> Node:

        self.consume() # if

        cond = self.ParseExpression()

        self.consume() # :

        self.consume() # new line

        self.indents += 1
        body = []
        while self.GetLeadingTabs() == self.indents:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            body.append(self.ParseStatement()) # consumes new lines
        self.indents -= 1

        return NodeIf(cond, body)
    
    # Helper Function: returns how many consecutive tabs are following.
    def GetLeadingTabs(self) -> int:
        i = 0
        while self.peek(i).subtype == TokenSubtypes.DELIMITER_TAB:
            i += 1
        return i