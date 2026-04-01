import Lexer
import Parser
import Transpiler

code = '''

def fuck(x):
    return x + 3

a = fuck("fuck")

'''

lexer = Lexer.Lexer(code)
lexer.analyze()

for token in lexer.tokens:
    print(token)

parser = Parser.Parser(lexer.tokens)
parser.parse()

transpiler = Transpiler.Transpiler(parser.nodes)
transpiler.transpile()

print('-------------------- PYTHON --------------------')
print(code)
print('------------------ JAVASCRIPT ------------------')
print(transpiler.code)