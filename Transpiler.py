# Converts AST to JavaScript
# Author: Evan Cassidy
# Date: 3/31/2026

from Lexer import TokenSubtypes
from Parser import Nodes, Node

# Flags that can be passed to nodeToJs
class Flags:
    CLASS = 1

class Transpiler:
    def __init__(self, ast: list[Node]):
        self.ast = ast
        self.code = ''

    def transpile(self) -> None:
        for node in self.ast:
            self.code += self.nodeToJs(node)
    
    # Converts node to JavaScript
    # Optional flags parameter to pass to objects that may need it
    def nodeToJs(self, node: Node, flag=None):

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
            type = 'static' if flag == Flags.CLASS else 'var'
            return f'{type} {node.var}={self.nodeToJs(node.expr)};'
        
        if node.type == Nodes.DEFINITION:
            func = node.func
            args = ','.join(node.args)
            body = ''.join(self.nodeToJs(n) for n in node.body)
            if flag == Flags.CLASS:
                if func == '__init__':
                    func = 'constructor'
                args = ','.join(node.args[1:])
                return f'{func}({args}){{{body}}};'
            else:
                return f'var {func}=function({args}){{{body}}};'
        
        if node.type == Nodes.RETURN:
            return f'return {self.nodeToJs(node.expr)};'
        
        if node.type == Nodes.IF:
            cond = node.cond
            body = ''.join(self.nodeToJs(n) for n in node.body)
            else_body = ''.join(self.nodeToJs(n) for n in node.else_body)
            return f'if({self.nodeToJs(cond)}){{{body}}}else{{{else_body}}};'
        
        if node.type == Nodes.WHILE:
            cond = node.cond
            body = ''.join(self.nodeToJs(n) for n in node.body)
            return f'while({self.nodeToJs(cond)}){{{body}}};'
        
        if node.type == Nodes.STATEMENT_CALL:
            func = self.nodeToJs(node.func)
            args = ','.join(self.nodeToJs(arg) for arg in node.args)
            return f'{func}({args});'
        
        if node.type == Nodes.STATEMENT_BINARY:
            return f'{self.nodeToJs(node.left)}{operators[node.operation]}{self.nodeToJs(node.right)};'
        
        if node.type == Nodes.CLASS:
            name = node.name
            body = ''.join(self.nodeToJs(n, Flags.CLASS) for n in node.body)
            return f'class {name}{{{body}}};'
        
        # === Expressions ===
        if node.type == Nodes.BINARY:
            if node.statement:
                return f'{self.nodeToJs(node.left)}{operators[node.operation]}{self.nodeToJs(node.right)};'
            else:
                return f'({self.nodeToJs(node.left)}{operators[node.operation]}{self.nodeToJs(node.right)})'
        
        if node.type == Nodes.CALL:
            func = self.nodeToJs(node.func)
            args = ','.join(self.nodeToJs(arg) for arg in node.args)
            return f'{func}({args})'
        
        if node.type == Nodes.ACCESS:
            return f'{self.nodeToJs(node.obj)}.{node.attr}'
        
        if node.type == Nodes.INDEX:
            return f'{self.nodeToJs(node.obj)}[{self.nodeToJs(node.index)}]'

        # === Objects ===
        if node.type == Nodes.LITERAL:
            return f'{node.value}'

        if node.type == Nodes.IDENTIFIER:
            return f'{node.id}'
        
        if node.type == Nodes.LIST:
            els = ','.join(self.nodeToJs(el) for el in node.arr)
            return f'[{els}]'
        
        return f'---> {node.type} <---'