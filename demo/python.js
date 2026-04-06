// Load a Python script
function python(code) {

    // Lexer
    lexer = new Lexer(code);
    lexer.analyze();

    // Parser
    parser = new Parser(lexer.tokens);
    parser.parse();
    
    // Transpile
    transpiler = new Transpiler(parser.nodes);
    transpiler.transpile();

    // Eval
    eval(transpiler.code);
}
