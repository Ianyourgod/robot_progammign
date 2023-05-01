def run(text: str, debug=False):
    if debug:
        from lexer import Lexer
        from parse import Parser
        from interpreter import Interpreter
        lex = Lexer(text)
        tokens = lex.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        print("Tokens:")
        print(tokens)
        print("AST:")
        for i in ast:
            print(i)
        print("Output:")
        for i in ast:
            ret = interpreter.interpret(i)
            if ret != None:
                print(ret)
        print(interpreter.variables)
    else:
        from lexer import Lexer
        from parse import Parser
        from interpreter import Interpreter
        lex = Lexer(text)
        tokens = lex.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()

        for i in ast:
            ret = interpreter.interpret(i)
            if ret != None:
                print(ret)
if __name__ == "__main__":    
    run("""
    def randint(a) {
        added = ((a + 247) ** 2 + (a + 853) ** 2 + (a + 435) ** 2)
        return added
    }
    randint(6)
    """, True)