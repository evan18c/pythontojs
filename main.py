import Lexer
import Parser
import Transpiler

code = '''
x = 3
'''

lexer = Lexer.Lexer(code)
lexer.analyze()

parser = Parser.Parser(lexer.tokens)
parser.parse()

transpiler = Transpiler.Transpiler(parser.nodes)

print(transpiler.javascript())