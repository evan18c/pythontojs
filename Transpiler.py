# Converts AST to JavaScript
# Author: Evan Cassidy
# Date: 3/31/2026

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

        if node is None:
            return ''
        