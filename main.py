import Lexer
import Parser
import Transpiler

code = open('code.py','r').read()

lexer = Lexer.Lexer(code)
lexer.analyze()

parser = Parser.Parser(lexer.tokens)
parser.parse()

transpiler = Transpiler.Transpiler(parser.nodes)
transpiler.transpile()

print(transpiler.code)