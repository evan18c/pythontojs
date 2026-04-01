import Lexer
import Parser
import Transpiler

code = '''

a = b[0]

'''

lexer = Lexer.Lexer(code)
lexer.analyze()

print('-------------------- TOKENS --------------------')
for token in lexer.tokens:
    print(token)

parser = Parser.Parser(lexer.tokens)
parser.parse()

transpiler = Transpiler.Transpiler(parser.nodes)
transpiler.transpile()

print('-------------------- PYTHON --------------------')
print(code.strip('\n'))
print('------------------ JAVASCRIPT ------------------')
print(transpiler.code)