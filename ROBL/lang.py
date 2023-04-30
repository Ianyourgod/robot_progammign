def run(text: str, debug=False):
    if debug:
        pass
    from lexer import Lexer
    from parse import Parser
    #from interpreter import Interpreter
    lex = Lexer(text)
    tokens = lex.tokenize()
    parser = Parser(tokens)
    print(parser.parse())
    #from interpreter import Interpreter
    
run("""
def add(a, b) {
    return a + b
}
""", True)