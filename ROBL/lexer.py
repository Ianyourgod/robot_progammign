from CONSTS import *

class Token:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        
    def __repr__(self):
        return f"Token({self.name}, {self.value})" if self.value else f"Token({self.name})"
    
    def __str__(self):
        return f"Token({self.name}, {self.value})" if self.value else f"Token({self.name})"
    

class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.pos = -1
        self.current_char = None
        self.advance()
        
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        while self.pos < len(self.text):
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char in CHARS:
                word = ""
                while self.current_char in CHARS + DIGITS and self.pos < len(self.text):
                    word += self.current_char
                    self.advance()
                if word in KEYWORDS:
                    self.tokens.append(Token(word.upper()))
                else:
                    self.tokens.append(Token("IDENTIFIER", word))
            elif self.current_char in DIGITS:
                numb = ""
                dots = 0
                while self.current_char in DIGITS + "." and self.pos < len(self.text):
                    numb += self.current_char
                    if self.current_char == ".":
                        dots += 1
                    if dots > 1:
                        raise Exception("Invalid number")
                    self.advance()
                if dots == 0:
                    self.tokens.append(Token("INT", int(numb)))
                else:
                    self.tokens.append(Token("FLOAT", float(numb)))
            elif self.current_char == '"':
                self.advance()
                string = ""
                while self.current_char != '"':
                    string += self.current_char
                    self.advance()
                self.advance()
                self.tokens.append(Token("STRING", string))
            elif self.current_char == "'":
                self.advance()
                string = ""
                while self.current_char != "'":
                    string += self.current_char
                    self.advance()
                self.advance()
                self.tokens.append(Token("STRING", string))
            elif self.current_char == "+":
                self.advance()
                if self.current_char == "=":
                    self.tokens.append(Token("ADD_ASSIGN"))
                    self.advance()
                else:
                    self.tokens.append(Token("ADD"))
            elif self.current_char == "-":
                self.advance()
                if self.current_char == "=":
                    self.tokens.append(Token("MIN_ASSIGN"))
                    self.advance()
                else:
                    self.tokens.append(Token("MIN"))
            elif self.current_char == "*":
                self.advance()
                if self.current_char == "=":
                    self.tokens.append(Token("MUL_ASSIGN"))
                    self.advance()
                elif self.current_char == "*":
                    self.advance()
                    if self.current_char == "=":
                        self.tokens.append(Token("EXP_ASSIGN"))
                        self.advance()
                    else:
                        self.tokens.append(Token("EXP"))
                else:
                    self.tokens.append(Token("MUL"))
            elif self.current_char == "/":
                self.advance()
                if self.current_char == "=":
                    self.tokens.append(Token("DIV_ASSIGN"))
                    self.advance()
                elif self.current_char == "/":
                    self.advance()
                    if self.current_char == "=":
                        self.tokens.append(Token("INT_DIV_ASSIGN"))
                        self.advance()
                    else:
                        self.tokens.append(Token("INT_DIV"))
                else:
                    self.tokens.append(Token("DIV"))
            elif self.current_char == "%":
                self.advance()
                if self.current_char == "=":
                    self.tokens.append(Token("MOD_ASSIGN"))
                    self.advance()
                else:
                    self.tokens.append(Token("MOD"))
            elif self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    self.tokens.append(Token("EQ"))
                    self.advance()
                else:
                    self.tokens.append(Token("ASSIGN"))
            elif self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    self.tokens.append(Token("NEQ"))
                    self.advance()
                else:
                    self.tokens.append(Token("NOT"))
            elif self.current_char == "&":
                self.advance()
                if self.current_char == "&":
                    self.tokens.append(Token("AND"))
                    self.advance()
                else:
                    raise Exception("Invalid character '&'")
            elif self.current_char == "|":
                self.advance()
                if self.current_char == "|":
                    self.tokens.append(Token("OR"))
                    self.advance()
                else:
                    raise Exception("Invalid character '|'")
            elif self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    self.tokens.append(Token("GTE"))
                    self.advance()
                else:
                    self.tokens.append(Token("GT"))
            elif self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    self.tokens.append(Token("LEQ"))
                    self.advance()
                else:
                    self.tokens.append(Token("LT"))
            elif self.current_char == "(":
                self.tokens.append(Token("LPAREN"))
                self.advance()
            elif self.current_char == ")":
                self.tokens.append(Token("RPAREN"))
                self.advance()
            elif self.current_char == "{":
                self.tokens.append(Token("LBRACE"))
                self.advance()
            elif self.current_char == "}":
                self.tokens.append(Token("RBRACE"))
                self.advance()
            elif self.current_char == "[":
                self.tokens.append(Token("LBRACKET"))
                self.advance()
            elif self.current_char == "]":
                self.tokens.append(Token("RBRACKET"))
                self.advance()
            elif self.current_char == ",":
                self.tokens.append(Token("COMMA"))
                self.advance()
            elif self.current_char == ";":
                raise Exception("DIE")
            elif self.current_char == ":":
                self.tokens.append(Token("COLON"))
                self.advance()
            elif self.current_char == ".":
                self.tokens.append(Token("DOT"))
                self.advance()
            elif self.current_char == "\n":
                self.tokens.append(Token("NEWLINE"))
                self.advance()
            else:
                raise Exception(f"Invalid character '{self.current_char}'")
        self.tokens.append(Token("EOF"))
        return self.tokens