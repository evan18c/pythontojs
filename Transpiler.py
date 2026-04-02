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

    # Adds Python functions to JavaScript
    def builtin(self) -> None:
        self.code += 'var range=function(n){return Array.from({length:n},(_,i)=>i);};' # range

    # Converts AST to JavaScript
    def transpile(self) -> None:
        self.builtin()
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
            var = node.var
            expr = self.nodeToJs(node.expr)
            return f'{type} {var}={expr};'
        
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
            expr = self.nodeToJs(node.expr)
            return f'return {expr};'
        
        if node.type == Nodes.IF:
            cond = self.nodeToJs(node.cond)
            body = ''.join(self.nodeToJs(n) for n in node.body)
            else_body = ''.join(self.nodeToJs(n) for n in node.else_body)
            return f'if({cond}){{{body}}}else{{{else_body}}};'
        
        if node.type == Nodes.WHILE:
            cond = node.cond
            body = ''.join(self.nodeToJs(n) for n in node.body)
            return f'while({self.nodeToJs(cond)}){{{body}}};'
        
        if node.type == Nodes.STATEMENT_CALL:
            func = self.nodeToJs(node.func)
            args = ','.join(self.nodeToJs(arg) for arg in node.args)
            return f'{func}({args});'
        
        if node.type == Nodes.STATEMENT_BINARY:
            left = self.nodeToJs(node.left)
            op = operators[node.operation]
            right = self.nodeToJs(node.right)
            return f'{left}{op}{right};'
        
        if node.type == Nodes.CLASS:
            name = node.name
            body = ''.join(self.nodeToJs(n, flag=Flags.CLASS) for n in node.body)
            return f'class {name}{{{body}}};'
        
        if node.type == Nodes.BINARY and node.statement:
            left = self.nodeToJs(node.left)
            op = operators[node.operation]
            right = self.nodeToJs(node.right)
            return f'{left}{op}{right};'
        
        if node.type == Nodes.FOR:
            var = node.var
            iter = self.nodeToJs(node.iter)
            body = ''.join(self.nodeToJs(n) for n in node.body)
            return f'for(var {var} in {iter}){{{body}}};'


        # === Expressions ===
        if node.type == Nodes.BINARY:
            left = self.nodeToJs(node.left)
            op = operators[node.operation]
            right = self.nodeToJs(node.right)
            return f'{left}{op}{right}' + (';' if node.statement else '')
        
        if node.type == Nodes.CALL:
            func = self.nodeToJs(node.func)
            args = ','.join(self.nodeToJs(arg) for arg in node.args)
            return f'{func}({args})' + (';' if node.statement else '')
        
        if node.type == Nodes.ACCESS:
            obj = self.nodeToJs(node.obj)
            attr = node.attr
            return f'{obj}.{attr}' + (';' if node.statement else '')
        
        if node.type == Nodes.INDEX:
            obj = self.nodeToJs(node.obj)
            index = self.nodeToJs(node.index)
            return f'{obj}[{index}]' + (';' if node.statement else '')


        # === Objects ===
        if node.type == Nodes.LITERAL:
            value = node.value
            return f'{value}'

        if node.type == Nodes.IDENTIFIER:
            id = node.id
            return f'{id}'
        
        if node.type == Nodes.LIST:
            els = ','.join(self.nodeToJs(el) for el in node.arr)
            return f'[{els}]'
        

        # === Unknown ===
        return f'Untranspiled: {node.type}!'