import Lexer
import Parser
import Transpiler

code = '''
def fact(x):
    if x == 1:
        return 1
    else:
        return x * fact(x - 1)

print(transpiler.code.beans.hello())
'''

lexer = Lexer.Lexer(code)
lexer.analyze()

parser = Parser.Parser(lexer.tokens)
parser.parse()

transpiler = Transpiler.Transpiler(parser.nodes)
transpiler.transpile()

print(transpiler.code)