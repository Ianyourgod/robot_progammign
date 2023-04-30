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
{a: 1, b: 2, c: 3}
""", True)