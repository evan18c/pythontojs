import Lexer
import Parser
import Transpiler

code = '''

a = [1, 2, 3 + 99]

print(a[2])

'''

lexer = Lexer.Lexer(code)
lexer.analyze()

parser = Parser.Parser(lexer.tokens)
parser.parse()

transpiler = Transpiler.Transpiler(parser.nodes)
transpiler.transpile()

print('-------------------- PYTHON --------------------')
print(code.strip('\n'))
print('------------------ JAVASCRIPT ------------------')
print(transpiler.code)