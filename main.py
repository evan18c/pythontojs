import Lexer
import Parser
import Transpiler

code = open('code.py').read()

lexer = Lexer.Lexer(code)
lexer.analyze()

parser = Parser.Parser(lexer.tokens)
parser.parse()

transpiler = Transpiler.Transpiler(parser.nodes)
transpiler.transpile()

file = open('code.js', 'w')
file.write(transpiler.code)
file.close()