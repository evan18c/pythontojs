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
    WHILE = 'WHILE'
    STATEMENT_CALL = 'STATEMENT_CALL'

    # Expressions
    BINARY = 'BINARY'
    CALL = 'CALL'
    ACCESS = 'ACCESS'

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

class NodeReturn(Node):
    def __init__(self, expr: Node):
        super().__init__(Nodes.RETURN)
        self.expr = expr

class NodeIf(Node):
    def __init__(self, cond: Node, body: list[Node], else_body: list[Node]):
        super().__init__(Nodes.IF)
        self.cond = cond
        self.body = body
        self.else_body = else_body

class NodeWhile(Node):
    def __init__(self, cond: Node, body: list[Node]):
        super().__init__(Nodes.WHILE)
        self.cond = cond
        self.body = body

class NodeStatementCall(Node):
    def __init__(self, func: Node, args: list[Node]):
        super().__init__(Nodes.STATEMENT_CALL)
        self.func = func
        self.args = args

class NodeBinary(Node):
    def __init__(self, left: Node, operation: TokenSubtypes, right: Node):
        super().__init__(Nodes.BINARY)
        self.left = left
        self.operation = operation
        self.right = right

class NodeCall(Node):
    def __init__(self, func: Node, args: list[Node]):
        super().__init__(Nodes.CALL)
        self.func = func
        self.args = args

class NodeAccess(Node):
    def __init__(self, obj: Node, attr: str):
        super().__init__(Nodes.ACCESS)
        self.obj = obj
        self.attr = attr

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
        
        # While
        if self.peek().type == TokenTypes.KEYWORD and self.peek().subtype == TokenSubtypes.KEYWORD_WHILE:
            return self.ParseWhile()
        
        # Statement Call
        if self.peek().type == TokenTypes.IDENTIFIER and self.peek(1).subtype == TokenSubtypes.DELIMITER_LPAREN:
            return self.ParseStatementCall()
        
        # Access Statement Call
        if self.peek().type == TokenTypes.IDENTIFIER and self.peek(1).subtype == TokenSubtypes.DELIMITER_DOT:
            return self.ParseStatementCall()
        
        # Comment
        if self.peek().type == TokenTypes.DELIMITER and self.peek().subtype == TokenSubtypes.DELIMITER_COMMENT:
            return self.ParseComment()
        
        # New Line
        if self.peek().type == TokenTypes.EOL:
            self.SkipEOL()
            return None

        # Unknown Statement
        raise SyntaxError(f'Unexpected {self.peek().type}, {self.peek().subtype}.')
        
    def ParseExpression(self) -> Node:
        return self.ParseExpressionLevelTwo()

    
    # ========== EXPRESSIONS ========== #

    # Values parsed here
    def ParseExpressionLevelZero(self) -> Node:

        # Vars
        token = self.consume()
        node = None

        # Literal
        if token.type == TokenTypes.LITERAL:
            node = NodeLiteral(token.value)
        
        # Identifier
        if token.type == TokenTypes.IDENTIFIER:
            node = NodeIdentifier(token.value)
        
        # Parentheses
        if token.subtype == TokenSubtypes.DELIMITER_LPAREN:
            node = self.ParseExpression()
            self.consume() # )
        
        # Call + Access
        while self.peek().subtype in [TokenSubtypes.DELIMITER_LPAREN, TokenSubtypes.DELIMITER_DOT]:

            # Call
            if self.peek().subtype == TokenSubtypes.DELIMITER_LPAREN:
                self.consume() # (
                args = []
                while self.peek().subtype != TokenSubtypes.DELIMITER_RPAREN:
                    if len(args) != 0:
                        self.consume() # ,
                    args.append(self.ParseExpression())
                self.consume() # )
                node = NodeCall(node, args)
            
            # Access 
            if self.peek().subtype == TokenSubtypes.DELIMITER_DOT:
                self.consume() # .
                attr = self.consume().value
                node = NodeAccess(node, attr)
            
        # Return
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
    

    # ========== STATEMENTS ========== #

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
            body.append(self.ParseStatement())
            self.SkipEOL()
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

        # Parse Body
        self.indents += 1
        body = []
        while self.GetLeadingTabs() == self.indents:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            body.append(self.ParseStatement())
            self.SkipEOL()
        self.indents -= 1

        # Check for ELSE
        else_body = []
        if self.GetLeadingTabs() == self.indents and self.peek(self.indents).subtype == TokenSubtypes.KEYWORD_ELSE:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            self.consume() # else
            self.consume() # :
            self.consume() # new line
            self.indents += 1
            while self.GetLeadingTabs() == self.indents:
                for _ in range(self.indents):
                    self.consume() # consume the tabs
                else_body.append(self.ParseStatement())
                self.SkipEOL()
            self.indents -= 1

        return NodeIf(cond, body, else_body)
    
    def ParseWhile(self) -> Node:

        self.consume() # while

        cond = self.ParseExpression()

        self.consume() # :

        self.consume() # new line

        # Parse Body
        self.indents += 1
        body = []
        while self.GetLeadingTabs() == self.indents:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            body.append(self.ParseStatement())
            self.SkipEOL()
        self.indents -= 1

        return NodeWhile(cond, body)
    
    def ParseStatementCall(self) -> Node:
        
        node = self.ParseExpressionLevelZero()

        self.consume() # new line

        return NodeStatementCall(node.func, node.args)
    
    def ParseComment(self) -> Node:

        while self.peek().type != TokenTypes.EOL:
            self.consume()

        self.consume() # EOL

        return None

    # ========== HELPER ========== #

    # Helper Function: returns how many consecutive tabs are following.
    def GetLeadingTabs(self) -> int:
        i = 0
        while self.peek(i).subtype == TokenSubtypes.DELIMITER_TAB:
            i += 1
        return i
    
    # Helper Function: skips over every EOL token
    def SkipEOL(self) -> None:
        while self.peek().type == TokenTypes.EOL:
            self.consume()