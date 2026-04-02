<div align="center">
    <img src="assets/logo.png" alt="Logo" width="128" height="128">
    <h1>py2js</h1>
</div>

## About
py2js is a transpiler that converts Python code into JavaScript code.

## Usage:
To use it, import `Compiler` and call `Compile` on your code.
```py
import Compiler

code = '''
def fact(x):
    if x == 1:
        return 1
    else:
        return x * fact(x - 1)

console.log('The first 10 factorials are:')
for i in range(10):
    console.log(fact(i+1))
'''

print(Compiler.Compile(code))
```

## Work In Progress
This project is still a WIP so there are still bugs.