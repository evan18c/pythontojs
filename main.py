import Lexer

code = '''
x = 3
y = x + 2

def func():
    fuck = 4
    return fuck
'''

lexer = Lexer.Lexer(code)

lexer.analyze()

for token in lexer.tokens:
    print(token)