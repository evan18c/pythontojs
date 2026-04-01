import Lexer
import Parser
import Transpiler

code = open('code.py').read()

lexer = Lexer.Lexer(code)
lexer.analyze()

for token in lexer.tokens:
    print(token)

parser = Parser.Parser(lexer.tokens)
parser.parse()

transpiler = Transpiler.Transpiler(parser.nodes)
transpiler.transpile()

print(transpiler.code)