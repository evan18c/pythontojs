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

js = open('code.js','w')
js.write(transpiler.code)
js.close()