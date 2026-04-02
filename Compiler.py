# Converts Python to JavaScript
# Author: Evan Cassidy
# Date: 4/1/2026

import Lexer
import Parser
import Transpiler

def Compile(code: str) -> str:
    lexer = Lexer.Lexer(code)
    lexer.analyze()
    parser = Parser.Parser(lexer.tokens)
    parser.parse()
    transpiler = Transpiler.Transpiler(parser.nodes)
    transpiler.transpile()
    return transpiler.code
