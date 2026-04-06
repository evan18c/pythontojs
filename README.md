<br>
<div align="center">
 <img src="assets/logo.png" alt="Logo" width="128" height="128">

 # py2js

 <p align="center">
  Bringing Python to JavaScript.
 </p>
</div>

## About
py2js is a transpiler that converts Python code into JavaScript code.

## Usage:
To use it, import `Compiler` and call `Compile` on your code.
```py
import Compiler

code = open('script.py').read()

print(Compiler.Compile(code))
```
with
```py
from JavaScript import *

def randint(min, max):
    return Math.round(Math.random() * (max - min) + min)

def main():

    canvas = document.createElement('canvas')
    canvas.width = 512
    canvas.height = 512

    ctx = canvas.getContext('2d')

    ctx.fillStyle = 'white'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    for _ in range(10):
        ctx.moveTo(randint(0, 512), randint(0, 512))
        ctx.lineTo(randint(0, 512), randint(0, 512))
        ctx.stroke()

    document.body.appendChild(canvas)

main()
```
This code creates a canvas and draws 10 random lines to it.

## Demo
A compiled version of this project can be tested [here](https://evan18c.github.io/pythontojs/demo/).<br>
Please be aware that the compiled version is even more unstable.

## Notes
This project is mostly a proof of concept and supports only a subset of Python.