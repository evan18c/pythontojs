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
    STATEMENT_BINARY = 'STATEMENT_BINARY'
    CLASS = 'CLASS'
    FOR = 'FOR'
    CONTINUE = 'CONTINUE'

    # Expressions
    BINARY = 'BINARY'
    CALL = 'CALL'
    ACCESS = 'ACCESS'
    INDEX = 'INDEX'
    UNARY = 'UNARY'

    # Objects
    LITERAL = 'LITERAL'
    IDENTIFIER = 'IDENTIFIER'

    # Python Objects
    LIST = 'LIST'
    DICT = 'DICT'
    TUPLE = 'TUPLE'

class Node:
    def __init__(self, type: str, statement: bool):
        self.type = type
        self.statement = statement
    def __str__(self):
        return f'{self.type}'
    def __repr__(self):
        return self.__str__()

class NodeAssignment(Node):
    def __init__(self, var: str, expr: Node):
        super().__init__(Nodes.ASSIGNMENT, True)
        self.var = var
        self.expr = expr
    
class NodeDefinition(Node):
    def __init__(self, func: str, args: list[str], body: list[Node]):
        super().__init__(Nodes.DEFINITION, True)
        self.func = func
        self.args = args
        self.body = body

class NodeReturn(Node):
    def __init__(self, expr: Node):
        super().__init__(Nodes.RETURN, True)
        self.expr = expr

class NodeIf(Node):
    def __init__(self, cond: Node, body: list[Node], else_body: list[Node]):
        super().__init__(Nodes.IF, True)
        self.cond = cond
        self.body = body
        self.else_body = else_body

class NodeWhile(Node):
    def __init__(self, cond: Node, body: list[Node]):
        super().__init__(Nodes.WHILE, True)
        self.cond = cond
        self.body = body

class NodeStatementCall(Node):
    def __init__(self, func: Node, args: list[Node]):
        super().__init__(Nodes.STATEMENT_CALL, True)
        self.func = func
        self.args = args

class NodeStatementBinary(Node):
    def __init__(self, left: Node, operation: TokenSubtypes, right: Node):
        super().__init__(Nodes.STATEMENT_BINARY, True)
        self.left = left
        self.operation = operation
        self.right = right

class NodeFor(Node):
    def __init__(self, var: str, iter: Node, body: list[Node]):
        super().__init__(Nodes.FOR, True)
        self.var = var
        self.iter = iter
        self.body = body

class NodeClass(Node):
    def __init__(self, name: str, body: list[Node]):
        super().__init__(Nodes.CLASS, True)
        self.name = name
        self.body = body

class NodeContinue(Node):
    def __init__(self):
        super().__init__(Nodes.CONTINUE, True)

class NodeBinary(Node):
    def __init__(self, left: Node, operation: TokenSubtypes, right: Node):
        super().__init__(Nodes.BINARY, False)
        self.left = left
        self.operation = operation
        self.right = right

class NodeUnary(Node):
    def __init__(self, operand: Node, operation: TokenSubtypes):
        super().__init__(Nodes.UNARY, False)
        self.operand = operand
        self.operation = operation

class NodeCall(Node):
    def __init__(self, func: Node, args: list[Node]):
        super().__init__(Nodes.CALL, False)
        self.func = func
        self.args = args

class NodeAccess(Node):
    def __init__(self, obj: Node, attr: str):
        super().__init__(Nodes.ACCESS, False)
        self.obj = obj
        self.attr = attr

class NodeIndex(Node):
    def __init__(self, obj: Node, index: Node):
        super().__init__(Nodes.INDEX, False)
        self.obj = obj
        self.index = index

class NodeLiteral(Node):
    def __init__(self, value):
        super().__init__(Nodes.LITERAL, False)
        self.value = value

class NodeIdentifier(Node):
    def __init__(self, id: str):
        super().__init__(Nodes.IDENTIFIER, False)
        self.id = id

class NodeList(Node):
    def __init__(self, arr: list):
        super().__init__(Nodes.LIST, False)
        self.arr = arr

class NodeDict(Node):
    def __init__(self, dict_: dict):
        super().__init__(Nodes.DICT, False)
        self.dict_ = dict_

class NodeTuple(Node):
    def __init__(self, arr: list):
        super().__init__(Nodes.TUPLE, False)
        self.arr = arr

class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0
        self.nodes = []
        self.indents = 0

    def peek(self, n: int = 0) -> Token:
        if (self.pos + n) < len(self.tokens):
            return self.tokens[self.pos + n]
        else:
            return self.tokens[-1]
    
    def consume(self) -> Token:
        token = self.peek()
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
            return self.ParseExpressionStatement()
        
        # Comment
        if self.peek().type == TokenTypes.DELIMITER and self.peek().subtype == TokenSubtypes.DELIMITER_COMMENT:
            return self.ParseComment()
        
        # Statement Binary
        if self.peek().type == TokenTypes.IDENTIFIER and self.peek(1).type == TokenTypes.OPERATOR:
            return self.ParseStatementBinary()
        
        # Class
        if self.peek().type == TokenTypes.KEYWORD and self.peek().subtype == TokenSubtypes.KEYWORD_CLASS:
            return self.ParseClass()
        
        # For
        if self.peek().type == TokenTypes.KEYWORD and self.peek().subtype == TokenSubtypes.KEYWORD_FOR:
            return self.ParseFor()
        
        # Import
        if self.peek().type == TokenTypes.KEYWORD and self.peek().subtype == TokenSubtypes.KEYWORD_IMPORT:
            return self.ParseImport()
        
        # From
        if self.peek().type == TokenTypes.KEYWORD and self.peek().subtype == TokenSubtypes.KEYWORD_FROM:
            return self.ParseFrom()
        
        # Continue
        if self.peek().type == TokenTypes.KEYWORD and self.peek().subtype == TokenSubtypes.KEYWORD_CONTINUE:
            return self.ParseContinue()
        
        # New Line
        if self.peek().type == TokenTypes.EOL:
            self.SkipEOL()
            return None

        # Unknown Statement
        raise SyntaxError(f'Unexpected {self.peek()}')
        
    def ParseExpression(self) -> Node:
        return self.ParseExpressionLevelFour()

    
    # ========== EXPRESSIONS ========== #

    # Values parsed here
    def ParseExpressionLevelZero(self) -> Node:

        # Vars
        self.SkipComment()
        self.SkipEOLTAB()
        token = self.consume()
        node = None

        # Literal
        if token.type == TokenTypes.LITERAL:
            node = NodeLiteral(token.value)

        # Array
        if token.subtype == TokenSubtypes.DELIMITER_LSQUARE:
            arr = []
            while self.peek().subtype != TokenSubtypes.DELIMITER_RSQUARE:
                if len(arr) != 0:
                    self.consume() # ,
                self.SkipComment()
                self.SkipEOLTAB()
                arr.append(self.ParseExpression())
                self.SkipComment()
                self.SkipEOLTAB()
            self.consume() # ]
            node = NodeList(arr)

        # Dictionary
        if token.subtype == TokenSubtypes.DELIMITER_LBRACE:
            dict_ = {}
            while self.peek().subtype != TokenSubtypes.DELIMITER_RBRACE:
                if len(dict_) != 0:
                    self.consume() # ,
                self.SkipComment()
                self.SkipEOLTAB()
                key = self.ParseExpression()
                self.consume() # :
                val = self.ParseExpression()
                self.SkipComment()
                self.SkipEOLTAB()
                dict_[key] = val
            self.consume() # }
            node = NodeDict(dict_)
        
        # Identifier
        if token.type == TokenTypes.IDENTIFIER:
            node = NodeIdentifier(token.value)
        
        # Parentheses (Expressions + Tuples)
        if token.subtype == TokenSubtypes.DELIMITER_LPAREN:

            # ()
            if self.peek().subtype == TokenSubtypes.DELIMITER_RPAREN:
                self.consume() # )
                return NodeTuple([])
            
            node = self.ParseExpression()

            # tuple check
            if self.peek().subtype == TokenSubtypes.DELIMITER_COMMA:
                els = [node]
                while self.peek().subtype != TokenSubtypes.DELIMITER_RPAREN:
                    self.consume() # ,
                    self.SkipComment()
                    self.SkipEOLTAB()
                    els.append(self.ParseExpression())
                    self.SkipComment()
                    self.SkipEOLTAB()
                node = NodeTuple(els)

            self.consume() # )
        
        # Call + Access
        while self.peek().subtype in [TokenSubtypes.DELIMITER_LPAREN, TokenSubtypes.DELIMITER_LSQUARE, TokenSubtypes.DELIMITER_DOT]:

            # Call
            if self.peek().subtype == TokenSubtypes.DELIMITER_LPAREN:
                self.consume() # (
                args = []
                while self.peek().subtype != TokenSubtypes.DELIMITER_RPAREN:
                    if len(args) != 0:
                        self.consume() # ,
                    self.SkipComment()
                    self.SkipEOLTAB()
                    args.append(self.ParseExpression())
                    self.SkipComment()
                    self.SkipEOLTAB()
                self.consume() # )
                node = NodeCall(node, args)

            # Access
            if self.peek().subtype == TokenSubtypes.DELIMITER_LSQUARE:
                self.consume() # [
                self.SkipComment()
                self.SkipEOLTAB()
                index = self.ParseExpression()
                self.SkipComment()
                self.SkipEOLTAB()
                self.consume() # ]
                node = NodeIndex(node, index)
            
            # Access 
            if self.peek().subtype == TokenSubtypes.DELIMITER_DOT:
                self.consume() # .
                attr = self.consume().value
                node = NodeAccess(node, attr)
            
        # Return
        return node

    def ParseExpressionLevelOne(self) -> Node:

        if self.peek().subtype in [
            TokenSubtypes.OPERATOR_NOT
        ]:
            op = self.consume().subtype
            operand = self.ParseExpressionLevelOne()
            return NodeUnary(operand, op)

        return self.ParseExpressionLevelZero()
        
    # * / % parsed here
    def ParseExpressionLevelTwo(self) -> Node:

        node = self.ParseExpressionLevelOne()

        while self.peek().subtype in [
            TokenSubtypes.OPERATOR_EXPONENT,
            TokenSubtypes.OPERATOR_MULTIPLY,
            TokenSubtypes.OPERATOR_DIVIDE,
            TokenSubtypes.OPERATOR_MODULO,
            TokenSubtypes.OPERATOR_MULTIPLYEQUAL,
            TokenSubtypes.OPERATOR_DIVIDEEQUAL,
            TokenSubtypes.OPERATOR_MODULOEQUAL
        ]:
            left = node
            op = self.consume().subtype
            right = self.ParseExpressionLevelOne()
            node = NodeBinary(left, op, right)

        return node
    
    # + - parsed here
    def ParseExpressionLevelThree(self) -> Node:

        node = self.ParseExpressionLevelTwo()

        while self.peek().subtype in [
            TokenSubtypes.OPERATOR_ADD,
            TokenSubtypes.OPERATOR_SUBTRACT,
            TokenSubtypes.OPERATOR_ADDEQUAL,
            TokenSubtypes.OPERATOR_SUBTRACTEQUAL,
        ]:
            left = node
            op = self.consume().subtype
            right = self.ParseExpressionLevelTwo()
            node = NodeBinary(left, op, right)

        return node
    
    # = < > <= >= != == in and or parsed here
    def ParseExpressionLevelFour(self) -> Node:

        node = self.ParseExpressionLevelThree()

        while self.peek().subtype in [
            TokenSubtypes.OPERATOR_EQUAL,
            TokenSubtypes.OPERATOR_LESS,
            TokenSubtypes.OPERATOR_GREATER,
            TokenSubtypes.OPERATOR_LESSEQUAL,
            TokenSubtypes.OPERATOR_GREATEREQUAL,
            TokenSubtypes.OPERATOR_NOTEQUAL,
            TokenSubtypes.OPERATOR_EQUALEQUAL,
            TokenSubtypes.OPERATOR_IN,
            TokenSubtypes.OPERATOR_AND,
            TokenSubtypes.OPERATOR_OR
        ]:
            left = node
            op = self.consume().subtype
            right = self.ParseExpressionLevelThree()
            node = NodeBinary(left, op, right)

        return node
    

    # ========== STATEMENTS ========== #

    def ParseAssignment(self) -> Node:
        
        var = self.consume().value

        self.consume() # =

        expr = self.ParseExpression()

        self.SkipComment()

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
            if self.peek().subtype == TokenSubtypes.DELIMITER_COLON:
                self.consume() # :
                self.consume() # type
        
        self.consume() # )

        if self.peek().subtype == TokenSubtypes.KEYWORD_ARROW:
            self.consume() # ->
            self.consume() # type
        
        self.consume() # :

        self.SkipComment()

        self.SkipEOL() # new lines

        self.indents += 1
        body = []
        while self.GetLeadingTabs() == self.indents:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            body.append(self.ParseStatement())
            self.SkipComment()
            self.SkipEOL()
        self.indents -= 1

        return NodeDefinition(func, args, body)

    def ParseReturn(self) -> Node:

        self.consume() # return

        expr = self.ParseExpression()

        self.SkipComment()

        self.consume() # new line

        return NodeReturn(expr)
    
    def ParseIf(self) -> Node:

        self.consume() # if

        cond = self.ParseExpression()

        self.consume() # :

        self.SkipComment()

        self.SkipEOL() # new lines

        # Parse Body
        self.indents += 1
        body = []
        while self.GetLeadingTabs() == self.indents:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            body.append(self.ParseStatement())
            self.SkipComment()
            self.SkipEOL()
        self.indents -= 1

        # Check for ELSE
        else_body = []
        if self.GetLeadingTabs() == self.indents and self.peek(self.indents).subtype == TokenSubtypes.KEYWORD_ELSE:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            self.consume() # else
            self.consume() # :
            self.SkipComment()
            self.consume() # new line
            self.indents += 1
            while self.GetLeadingTabs() == self.indents:
                for _ in range(self.indents):
                    self.consume() # consume the tabs
                else_body.append(self.ParseStatement())
                self.SkipComment()
                self.SkipEOL()
            self.indents -= 1

        return NodeIf(cond, body, else_body)
    
    def ParseWhile(self) -> Node:

        self.consume() # while

        cond = self.ParseExpression()

        self.consume() # :

        self.SkipComment()

        self.SkipEOL() # new lines

        # Parse Body
        self.indents += 1
        body = []
        while self.GetLeadingTabs() == self.indents:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            body.append(self.ParseStatement())
            self.SkipComment()
            self.SkipEOL()
        self.indents -= 1

        return NodeWhile(cond, body)
    
    def ParseStatementCall(self) -> Node:
        
        node = self.ParseExpressionLevelZero()

        self.SkipComment()

        self.consume() # new line

        node.statement = True

        return NodeStatementCall(node.func, node.args)
    
    def ParseComment(self) -> Node:

        self.SkipComment()

        self.consume() # EOL

        return None
    
    def ParseStatementBinary(self) -> Node:

        node = self.ParseExpression()

        self.SkipComment()

        self.consume() # new line

        node.statement = True

        return NodeStatementBinary(node.left, node.operation, node.right)
    
    def ParseClass(self) -> Node:

        self.consume() # class

        name = self.consume().value

        self.consume() # :

        self.SkipComment()

        self.SkipEOL() # new lines

        # Parse Body
        self.indents += 1
        body = []
        while self.GetLeadingTabs() == self.indents:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            body.append(self.ParseStatement())
            self.SkipComment()
            self.SkipEOL()
        self.indents -= 1

        return NodeClass(name, body)
    
    # This should ideally replace statement_call and statement_binary
    def ParseExpressionStatement(self) -> Node:
        
        node = self.ParseExpression()

        self.SkipComment()

        self.consume() # new line

        node.statement = True

        return node
    
    def ParseFor(self) -> Node:

        self.consume() # for

        var = self.consume().value

        self.consume() # in

        iter = self.ParseExpression()

        self.consume() # :

        self.SkipComment()

        self.SkipEOL() # new lines

        # Parse Body
        self.indents += 1
        body = []
        while self.GetLeadingTabs() == self.indents:
            for _ in range(self.indents):
                self.consume() # consume the tabs
            body.append(self.ParseStatement())
            self.SkipComment()
            self.SkipEOL()
        self.indents -= 1

        return NodeFor(var, iter, body)
    
    def ParseImport(self) -> Node:
        while self.peek().type != TokenTypes.EOL:
            self.consume()
        self.consume()
        return None
    
    def ParseFrom(self) -> Node:
        while self.peek().type != TokenTypes.EOL:
            self.consume()
        self.consume()
        return None
    
    def ParseContinue(self) -> Node:
        self.consume() # continue
        self.SkipComment()
        self.consume() # new line
        return NodeContinue()

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

    # Helper Function: skips over every TAB token
    def SkipTAB(self) -> None:
        while self.peek().type == TokenSubtypes.DELIMITER_TAB:
            self.consume()

    # Helper Function: skips over a comment if there is one
    def SkipComment(self) -> None:
        if self.peek().subtype == TokenSubtypes.DELIMITER_COMMENT:
            self.consume()
            while self.peek().type != TokenTypes.EOL:
                self.consume()


    # Helper Function: skips over all TAB or EOL tokens
    def SkipEOLTAB(self) -> None:
        while self.peek().type == TokenTypes.EOL or self.peek().subtype == TokenSubtypes.DELIMITER_TAB:
            self.consume()