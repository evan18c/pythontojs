import Lexer
import Parser

code = '''
x = 3
'''

lexer = Lexer.Lexer(code)
lexer.analyze()

parser = Parser.Parser(lexer.tokens)
parser.parse()

for node in parser.nodes:
    print(node)