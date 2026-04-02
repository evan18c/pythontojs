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
    def nodeToJs(self, node: Node, flag=None, indents=0):

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
        
        # === None ===
        tabs = '    ' * indents
        
        # === Statements ===
        if node.type == Nodes.ASSIGNMENT:
            type = 'static' if flag == Flags.CLASS else 'var'
            return tabs + f'{type} {node.var} = {self.nodeToJs(node.expr)};\n'
        
        if node.type == Nodes.DEFINITION:
            func = node.func
            args = ', '.join(node.args)
            body = ''.join(self.nodeToJs(n, indents=indents+1) for n in node.body)
            if flag == Flags.CLASS:
                if func == '__init__':
                    func = 'constructor'
                args = ', '.join(node.args[1:])
                return tabs + f'{func}({args}){{\n{body}}};'
            else:
                return tabs + f'var {func}=function({args}){{\n{body}}};\n'
        
        if node.type == Nodes.RETURN:
            return tabs + f'return {self.nodeToJs(node.expr)};'
        
        if node.type == Nodes.IF:
            cond = node.cond
            body = ''.join(self.nodeToJs(n, indents=indents+1) for n in node.body)
            else_body = ''.join(self.nodeToJs(n) for n in node.else_body)
            return tabs + f'if ({self.nodeToJs(cond)}){{\n{body}}} else {{\n{else_body}}};\n'
        
        if node.type == Nodes.WHILE:
            cond = node.cond
            body = ''.join(self.nodeToJs(n, indents=indents+1) for n in node.body)
            return tabs + f'while ({self.nodeToJs(cond)}) {{\n{body}}};\n'
        
        if node.type == Nodes.STATEMENT_CALL:
            func = self.nodeToJs(node.func)
            args = ', '.join(self.nodeToJs(arg) for arg in node.args)
            return tabs + f'{func}({args});\n'
        
        if node.type == Nodes.STATEMENT_BINARY:
            return tabs + f'{self.nodeToJs(node.left)} {operators[node.operation]} {self.nodeToJs(node.right)};\n'
        
        if node.type == Nodes.CLASS:
            name = node.name
            body = ''.join(self.nodeToJs(n, flag=Flags.CLASS, indents=indents+1) for n in node.body)
            return tabs + f'class {name} {{\n{body}}};\n'
        
        if node.type == Nodes.BINARY and node.statement:
            return tabs + f'{self.nodeToJs(node.left)} {operators[node.operation]} {self.nodeToJs(node.right)};'

        # === Expressions ===
        if node.type == Nodes.BINARY and not node.statement:
            return tabs + f'({self.nodeToJs(node.left)} {operators[node.operation]} {self.nodeToJs(node.right)})'
        
        if node.type == Nodes.CALL:
            func = self.nodeToJs(node.func)
            args = ', '.join(self.nodeToJs(arg) for arg in node.args)
            return tabs + f'{func}({args})'
        
        if node.type == Nodes.ACCESS:
            return tabs + f'{self.nodeToJs(node.obj)}.{node.attr}'
        
        if node.type == Nodes.INDEX:
            return tabs + f'{self.nodeToJs(node.obj)}[{self.nodeToJs(node.index)}]'

        # === Objects ===
        if node.type == Nodes.LITERAL:
            return tabs + f'{node.value}'

        if node.type == Nodes.IDENTIFIER:
            return tabs + f'{node.id}'
        
        if node.type == Nodes.LIST:
            els = ', '.join(self.nodeToJs(el) for el in node.arr)
            return tabs + f'[{els}]'
        
        return f'---> {node.type} <---'