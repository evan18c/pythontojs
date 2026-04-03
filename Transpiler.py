# Converts AST to JavaScript
# Author: Evan Cassidy
# Date: 3/31/2026

from Lexer import TokenSubtypes
from Parser import Nodes, Node

# Flags that can be passed to nodeToJs
class Flags:
    CLASS = 1
    CONSTRUCTOR = 2
    METHOD = 3

class Transpiler:
    def __init__(self, ast: list[Node]):
        self.ast = ast
        self.code = ''
        self.functions = []
        self.classes = []

    # Builds in standard Python functions
    def builtin(self) -> None:

        # Constants
        self.code += 'window.True=true;'
        self.code += 'window.False=false;'
        self.code += 'window.None=null;'

        # Functions (TODO: only add functions required)
        self.code += 'function abs(x){return Math.abs(x);};'
        self.code += 'function all(x){for(var i of x){if(!i){return False;}};return True;};'
        self.code += 'function any(x){for(var i of x){if(i){return True;}};return False;};'
        self.code += 'function int(x){return Math.floor(x);};'
        self.code += 'function len(x){return x.length;};'
        self.code += 'function max(x){var m=x[0];var i=0;while((i<x.length)){if((x[i]>m)){var m=x[i];};i+=1;};return m;};'
        self.code += 'function min(x){var m=x[0];var i=0;while((i<x.length)){if((x[i]<m)){var m=x[i];};i+=1;};return m;};'
        self.code += 'function print(x){console.log(x);};'
        self.code += 'function range(n){var a=[];var i=0;while((i<n)){a.push(i);i+=1;};return a;};'
        self.code += 'function str(n){return String(n);};'

    # Converts AST to JavaScript
    def transpile(self) -> None:
        self.builtin()
        for node in self.ast:
            self.code += self.nodeToJs(node, [])
    
    # Converts node to JavaScript
    # Optional flags parameter to pass to objects that may need it
    def nodeToJs(self, node: Node, flags: list):

        # === Helpers === 
        operators = {
            TokenSubtypes.OPERATOR_EQUAL: '=',
            TokenSubtypes.OPERATOR_ADD: '+',
            TokenSubtypes.OPERATOR_SUBTRACT: '-',
            TokenSubtypes.OPERATOR_MULTIPLY: '*',
            TokenSubtypes.OPERATOR_DIVIDE: '/',
            TokenSubtypes.OPERATOR_MODULO: '%',
            TokenSubtypes.OPERATOR_EXPONENT: '**',
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
            TokenSubtypes.OPERATOR_EQUALEQUAL: '==',
            TokenSubtypes.OPERATOR_IN: ' in ',
            TokenSubtypes.OPERATOR_NOT: '!',
            TokenSubtypes.OPERATOR_AND: '&&',
            TokenSubtypes.OPERATOR_OR: '||'
        }

        # === None ===
        if node is None:
            return ''
        

        # === Statements ===
        if node.type == Nodes.ASSIGNMENT:
            type = 'static' if (Flags.CLASS in flags and Flags.METHOD not in flags) else 'var'
            var = node.var
            expr = self.nodeToJs(node.expr, flags.copy())
            return f'{type} {var}={expr};'
        
        if node.type == Nodes.DEFINITION:
            func = node.func
            self.functions.append(func)
            if Flags.CLASS in flags and func == '__init__':
                args = ','.join(node.args[1:])
                body = ''.join(self.nodeToJs(n, flags.copy()) for n in node.body)    # edit here
                return f'{func}({args}){{{body}}};'
            elif Flags.CLASS in flags:
                args = ','.join(node.args[1:])
                body = ''.join(self.nodeToJs(n, flags.copy() + [Flags.METHOD]) for n in node.body)
                return f'{func}({args}){{{body}}};'
            else:
                args = ','.join(node.args)
                body = ''.join(self.nodeToJs(n, flags.copy() + [Flags.METHOD]) for n in node.body)
                return f'function {func}({args}){{{body}}};'
        
        if node.type == Nodes.RETURN:
            expr = self.nodeToJs(node.expr, flags.copy())
            return f'return {expr};'
        
        if node.type == Nodes.IF:
            cond = self.nodeToJs(node.cond, flags.copy())
            body = ''.join(self.nodeToJs(n, flags.copy()) for n in node.body)
            else_body = ''.join(self.nodeToJs(n, flags.copy()) for n in node.else_body)
            return f'if({cond}){{{body}}}else{{{else_body}}};'
        
        if node.type == Nodes.WHILE:
            cond = node.cond
            body = ''.join(self.nodeToJs(n, flags.copy()) for n in node.body)
            return f'while({self.nodeToJs(cond, flags.copy())}){{{body}}};'
        
        if node.type == Nodes.STATEMENT_CALL:
            func = self.nodeToJs(node.func, flags.copy())
            args = ','.join(self.nodeToJs(arg, flags.copy()) for arg in node.args)
            return f'{func}({args});'
        
        if node.type == Nodes.STATEMENT_BINARY:
            left = self.nodeToJs(node.left, flags.copy())
            op = operators[node.operation]
            right = self.nodeToJs(node.right, flags.copy())
            return f'{left}{op}{right};'
        
        if node.type == Nodes.CLASS:
            name = node.name
            self.classes.append(name)
            body = ''.join(self.nodeToJs(n, flags.copy() + [Flags.CLASS]) for n in node.body)
            return f'class {name}{{{body}}};'
        
        if node.type == Nodes.BINARY and node.statement:
            left = self.nodeToJs(node.left, flags.copy())
            op = operators[node.operation]
            right = self.nodeToJs(node.right, flags.copy())
            return f'{left}{op}{right};'
        
        if node.type == Nodes.FOR:
            var = node.var
            iter = self.nodeToJs(node.iter, flags.copy())
            body = ''.join(self.nodeToJs(n, flags.copy()) for n in node.body)
            return f'for(var {var} of {iter}){{{body}}};'
        
        if node.type == Nodes.CONTINUE:
            return f'continue;'


        # === Expressions ===
        if node.type == Nodes.BINARY:
            left = self.nodeToJs(node.left, flags.copy())
            op = operators[node.operation]
            right = self.nodeToJs(node.right, flags.copy())
            return f'({left}{op}{right})' + (';' if node.statement else '')
        
        if node.type == Nodes.CALL:
            func = self.nodeToJs(node.func, flags.copy())
            new = 'new ' if func in self.classes else ''
            args = ','.join(self.nodeToJs(arg, flags.copy()) for arg in node.args)
            return f'{new}{func}({args})' + (';' if node.statement else '')
        
        if node.type == Nodes.ACCESS:
            obj = self.nodeToJs(node.obj, flags.copy())
            if obj == 'self' and Flags.CLASS in flags:
                obj = 'this'
            attr = node.attr
            if attr == 'append': # add dict for this
                attr = 'push'
            return f'{obj}.{attr}' + (';' if node.statement else '')
        
        if node.type == Nodes.INDEX:
            obj = self.nodeToJs(node.obj, flags.copy())
            index = self.nodeToJs(node.index, flags.copy())
            return f'{obj}[{index}]' + (';' if node.statement else '')
        
        if node.type == Nodes.UNARY:
            operand = self.nodeToJs(node.operand, flags.copy())
            op = operators[node.operation]
            return f'{op}{operand}' + (';' if node.statement else '')


        # === Objects ===
        if node.type == Nodes.LITERAL:
            value = node.value
            return f'{value}'

        if node.type == Nodes.IDENTIFIER:
            id = node.id
            return f'{id}'
        
        if node.type == Nodes.LIST:
            els = ','.join(self.nodeToJs(el, flags.copy()) for el in node.arr)
            return f'[{els}]'
        
        if node.type == Nodes.TUPLE:
            els = ','.join(self.nodeToJs(el, flags.copy()) for el in node.arr)
            return f'[{els}]'
        
        if node.type == Nodes.DICT:
            els = ','.join(f'{self.nodeToJs(k, flags.copy())}:{self.nodeToJs(node.dict_[k], flags.copy())}' for k in node.dict_)
            return f'{{{els}}}'
        

        # === Unknown === #
        raise SyntaxError(f'Unknown Node: {node.type}')