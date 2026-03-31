# Converts AST to JavaScript
# Author: Evan Cassidy
# Date: 3/31/2026

from Parser import Nodes, Node

class Transpiler:
    def __init__(self, ast: list[Node]):
        self.ast = ast

    def javascript(self) -> str:
        
        code = ''
        
        for node in self.ast:

            if node is None:
                continue

            if node.type == Nodes.ASSIGNMENT:
                code += f'var {node.var}={node.expr};'

        return code