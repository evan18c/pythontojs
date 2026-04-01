# Converts AST to JavaScript
# Author: Evan Cassidy
# Date: 3/31/2026

from Lexer import TokenSubtypes
from Parser import Nodes, Node

class Transpiler:
    def __init__(self, ast: list[Node]):
        self.ast = ast
        self.code = ''

    def transpile(self) -> None:
        for node in self.ast:
            self.code += self.nodeToJs(node)
    
    # Converts node to JavaScript
    def nodeToJs(self, node: Node):

        # === Helpers === 
        operators = {
            TokenSubtypes.OPERATOR_EQUAL: '=',
            TokenSubtypes.OPERATOR_ADD: '+',
            TokenSubtypes.OPERATOR_SUBTRACT: '-',
            TokenSubtypes.OPERATOR_MULTIPLY: '*',
            TokenSubtypes.OPERATOR_DIVIDE: '/',
            TokenSubtypes.OPERATOR_MODULO: '%',
            TokenSubtypes.OPERATOR_ADDEQUAL: '+=',
            TokenSubtypes.OPERATOR_SUBTRACTEQUAL: '-=',
            TokenSubtypes.OPERATOR_MULTIPLYEQUAL: '*=',
            TokenSubtypes.OPERATOR_DIVIDEEQUAL: '/=',
            TokenSubtypes.OPERATOR_MODULOEQUAL: '%=',
            TokenSubtypes.OPERATOR_LESS: '<',
            TokenSubtypes.OPERATOR_GREATER: '>',
            TokenSubtypes.OPERATOR_LESSEQUAL: '<=',
            TokenSubtypes.OPERATOR_GREATEREQUAL: '>=',
            TokenSubtypes.OPERATOR_NOTEQUAL: '!=',
            TokenSubtypes.OPERATOR_EQUALEQUAL: '=='
        }

        # === None ===
        if node is None:
            return ''
        
        # === Statements ===
        if node.type == Nodes.ASSIGNMENT:
            return f'var {node.var}={self.nodeToJs(node.expr)};'
        
        if node.type == Nodes.DEFINITION:
            func = node.func
            args = ','.join(node.args)
            body = ''.join(self.nodeToJs(n) for n in node.body)
            return f'var {func}=function({args}){{{body}}}'
        
        if node.type == Nodes.RETURN:
            return f'return {self.nodeToJs(node.expr)};'
        
        # === Expressions ===
        if node.type == Nodes.BINARY:
            return f'({self.nodeToJs(node.left)}{operators[node.operation]}{self.nodeToJs(node.right)})'

        # === Objects ===
        if node.type == Nodes.LITERAL:
            return f'{node.value}'

        if node.type == Nodes.IDENTIFIER:
            return f'{node.id}'
        
        return f'--> {node.type} <---'