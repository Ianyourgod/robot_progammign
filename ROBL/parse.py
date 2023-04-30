from CONSTS import KEYWORDS

class Node:
    def __init__(self, type, left, right=None):
        self.type = type
        self.left = left
        self.right = right
        
    def __repr__(self):
        return f"[{self.type}, {self.left}, {self.right}]" if self.right else f"[{self.type}, {self.left}]"

class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = -1
        self.line_pos = -1
        self.cur_line = []
        self.lines = []
        line = []
        for i in tokens:
            if i.name == "NEWLINE":
                if line != []:
                    line.append(i)
                    self.lines.append(line)
                line = []
            else:
                line.append(i)
        if line != []:
            self.lines.append(line)
        self.advance()
        
    def advance(self):
        self.pos += 1
        if self.pos >= len(self.cur_line): # type: ignore
            try:
                self.line_pos += 1
                self.cur_line = self.lines[self.line_pos]
                self.pos = 0
            except IndexError:
                self.cur_line = None
        if self.cur_line != None:
            self.current_token = self.cur_line[self.pos]
    
    def parse(self):
        lines = []
        while self.cur_line != None:
            expr = self.expr()
            if expr.type == "EOF":
                break
            if expr.type == "EOL":
                continue
            lines.append(expr)
        return lines
    
    def expr(self):
        node = self.term()
        if self.current_token.name == "ASSIGN":
            self.advance()
            node = Node("ASSIGN", node, self.expr())
        elif self.current_token.name == "ADD_ASSIGN":
            self.advance()
            node = Node("ADD_ASSIGN", node, self.expr())
        elif self.current_token.name == "SUB_ASSIGN":
            self.advance()
            node = Node("SUB_ASSIGN", node, self.expr())
        elif self.current_token.name == "MUL_ASSIGN":
            self.advance()
            node = Node("MUL_ASSIGN", node, self.expr())
        elif self.current_token.name == "DIV_ASSIGN":
            self.advance()
            node = Node("DIV_ASSIGN", node, self.expr())
        elif self.current_token.name == "MOD_ASSIGN":
            self.advance()
            node = Node("MOD_ASSIGN", node, self.expr())
        elif self.current_token.name == "EXP_ASSIGN":
            self.advance()
            node = Node("EXP_ASSIGN", node, self.expr())
        elif self.current_token.name == "EQ":
            self.advance()
            node = Node("EQ", node, self.factor())
        elif self.current_token.name == "NEQ":
            self.advance()
            node = Node("NEQ", node, self.factor())
        elif self.current_token.name == "LT":
            self.advance()
            node = Node("LT", node, self.factor())
        elif self.current_token.name == "GT":
            self.advance()
            node = Node("GT", node, self.factor())
        elif self.current_token.name == "LTE":
            self.advance()
            node = Node("LTE", node, self.factor())
        elif self.current_token.name == "GTE":
            self.advance()
            node = Node("GTE", node, self.factor())
        elif self.current_token.name == "AND":
            self.advance()
            node = Node("AND", node, self.factor())
        elif self.current_token.name == "OR":
            self.advance()
            node = Node("OR", node, self.factor())
        elif self.current_token.name == "NOT":
            self.advance()
            node = Node("NOT", node, self.factor())
        elif node.type == "IDENTIFIER" and self.current_token.name == "LPAREN":
            self.advance()
            exprs = []
            while self.current_token.name != "RPAREN":
                exprs.append(self.expr())
                if not self.current_token.name in ("COMMA", "RPAREN"):
                    raise Exception("Invalid syntax")
                if self.current_token.name == "COMMA":
                    self.advance()
            node = Node("CALL", node, exprs)
            self.advance()
        elif self.current_token.name == "IF":
            self.advance()
            expr = self.expr()
            lines = []
            if self.current_token.name == "LBRACE":
                prev_line_pos = self.line_pos
                self.advance()
                while self.current_token.name != "RBRACE":
                    if prev_line_pos < self.line_pos:
                        lines.append(self.current_token)
                    self.advance()
                self.advance()
            else:
                raise Exception("Invalid syntax")
            temp_parser = Parser(lines)
            lines = temp_parser.parse()
            node = Node("IF", expr, lines)
            while self.current_token == "ELIF":
                self.advance()
                expr = self.expr()
                lines = []
                if self.current_token.name == "LBRACE":
                    prev_line_pos = self.line_pos
                    self.advance()
                    while self.current_token.name != "RBRACE":
                        self.advance()
                    self.advance()
                else:
                    raise Exception("Invalid syntax")
                temp_parser = Parser(lines)
                lines = temp_parser.parse()
                node = Node("ELIF", expr, lines)
            if self.current_token == "ELSE":
                self.advance()
                lines = []
                if self.current_token.name == "LBRACE":
                    prev_line_pos = self.line_pos
                    self.advance()
                    while self.current_token.name != "RBRACE":
                        if prev_line_pos < self.line_pos:
                            lines.append(self.current_token)
                        self.advance()
                    self.advance()
                else:
                    raise Exception("Invalid syntax")
                temp_parser = Parser(lines)
                lines = temp_parser.parse()
                node = Node("ELSE", lines)
        elif self.current_token.name == "WHILE":
            self.advance()
            expr = self.expr()
            lines = []
            if self.current_token.name == "LBRACE":
                prev_line_pos = self.line_pos
                self.advance()
                while self.current_token.name != "RBRACE":
                    if prev_line_pos < self.line_pos:
                        lines.append(self.current_token)
                    self.advance()
                self.advance()
            else:
                raise Exception("Invalid syntax")
            temp_parser = Parser(lines)
            lines = temp_parser.parse()
            node = Node("WHILE", expr, lines)
            self.advance()
        elif self.current_token.name == "FOR":
            self.advance()
            expr = self.expr()
            if expr.type != "TUPLE":
                raise Exception("Invalid syntax")
            if len(expr.left) != 3:
                raise Exception("Invalid syntax")
            lines = []
            if self.current_token.name == "LBRACE":
                prev_line_pos = self.line_pos
                self.advance()
                while self.current_token.name != "RBRACE":
                    if prev_line_pos < self.line_pos:
                        lines.append(self.current_token)
                    self.advance()
                self.advance()
            else:
                raise Exception("Invalid syntax")
            temp_parser = Parser(lines)
            lines = temp_parser.parse()
            node = Node("FOR", expr, lines)
            self.advance()
        elif self.current_token.name == "FOREACH":
            self.advance()
            expr = self.expr()
            if expr.type != "TUPLE":
                raise Exception("Invalid syntax")
            if len(expr.left) != 2:
                raise Exception("Invalid syntax")
            lines = []
            if self.current_token.name == "LBRACE":
                prev_line_pos = self.line_pos
                self.advance()
                while self.current_token.name != "RBRACE":
                    if prev_line_pos < self.line_pos:
                        lines.append(self.current_token)
                    self.advance()
                self.advance()
            else:
                raise Exception("Invalid syntax")
            temp_parser = Parser(lines)
            lines = temp_parser.parse()
            node = Node("FOREACH", expr, lines)
            self.advance()
        elif self.current_token.name == "DEF":
            self.advance()
            if self.current_token.name == "IDENTIFIER":
                name = self.current_token.value
                self.advance()
                if self.current_token.name == "LPAREN":
                    self.advance()
                    args = []
                    while self.current_token.name != "RPAREN":
                        if self.current_token.name == "IDENTIFIER":
                            args.append(self.current_token.value)
                            self.advance()
                            if not self.current_token.name in ("COMMA", "RPAREN"):
                                raise Exception("Invalid syntax")
                            if self.current_token.name == "COMMA":
                                self.advance()
                        else:
                            raise Exception("Invalid syntax")
                    self.advance()
                    lines = []
                    if self.current_token.name == "LBRACE":
                        prev_line_pos = self.line_pos
                        self.advance()
                        while self.current_token.name != "RBRACE":
                            if prev_line_pos < self.line_pos:
                                lines.append(self.current_token)
                            self.advance()
                        self.advance()
                    else:
                        raise Exception("Invalid syntax")
                    temp_parser = Parser(lines)
                    lines = temp_parser.parse()
                    node = Node("DEF", name, (args, lines))
                else:
                    raise Exception("Invalid syntax")
            else:
                raise Exception("Invalid syntax")
        elif self.current_token.name == "RETURN":
            self.advance()
            node = Node("RETURN", self.expr())
        elif self.current_token.name == "BREAK":
            self.advance()
            node = Node("BREAK", None)
        elif self.current_token.name == "CONTINUE":
            self.advance()
            node = Node("CONTINUE", None)
        return node
    
    def term(self):
        node = self.factor()
        while self.current_token.name in ("ADD", "SUB"):
            if self.current_token.name == "ADD":
                self.advance()
                node = Node("ADD", node, self.factor())
            elif self.current_token.name == "SUB":
                self.advance()
                node = Node("SUB", node, self.factor())
        return node
        
    def factor(self):
        node = self.atom()
        while self.current_token.name in ("MUL", "DIV"):
            if self.current_token.name == "MUL":
                self.advance()
                node = Node("MUL", node, self.atom())
            elif self.current_token.name == "DIV":
                self.advance()
                node = Node("DIV", node, self.atom())
        return node
        
    def atom(self):
        if self.current_token.name == "INT":
            node = Node("INT", self.current_token.value)
            self.advance()
        elif self.current_token.name == "FLOAT":
            node = Node("FLOAT", self.current_token.value)
            self.advance()
        elif self.current_token.name == "SUB":
            self.advance()
            if self.current_token.name == "INT":
                node = Node("INT", -self.current_token.value)
                self.advance()
            elif self.current_token.name == "FLOAT":
                node = Node("FLOAT", -self.current_token.value)
                self.advance()
            else:
                raise Exception("Invalid syntax")
        elif self.current_token.name == "STRING":
            node = Node("STRING", self.current_token.value)
            self.advance()
        elif self.current_token.name == "IDENTIFIER":
            node = Node("IDENTIFIER", self.current_token.value)
            self.advance()
        elif self.current_token.name == "TRUE":
            node = Node("BOOL", True)
            self.advance()
        elif self.current_token.name == "FALSE":
            node = Node("BOOL", False)
            self.advance()
        elif self.current_token.name == "NONE":
            node = Node("NONE", None)
            self.advance()
        elif self.current_token.name == "LPAREN":
            self.advance()
            exprs = []
            while self.current_token.name != "RPAREN":
                exprs.append(self.expr())
                if not self.current_token.name in ("COMMA", "RPAREN"):
                    raise Exception("Invalid syntax")
                if self.current_token.name == "COMMA":
                    self.advance()
            node = Node("TUPLE", tuple(exprs))
            self.advance()
        elif self.current_token.name == "LBRACKET":
            self.advance()
            exprs = []
            while self.current_token.name != "RBRACKET":
                exprs.append(self.expr())
                if not self.current_token.name in ("COMMA", "RBRACKET"):
                    raise Exception("Invalid syntax")
                if self.current_token.name == "COMMA":
                    self.advance()
            node = Node("LIST", exprs)
            self.advance()
        elif self.current_token.name == "LBRACE":
            self.advance()
            exprs = []
            while self.current_token.name != "RBRACE":
                if self.current_token.name == "IDENTIFIER":
                    key = self.current_token.value
                    self.advance()
                    if self.current_token.name == "COLON":
                        self.advance()
                        exprs.append((key, self.expr()))
                    else:
                        raise Exception("Invalid syntax")
                else:
                    raise Exception("Invalid syntax")
                if not self.current_token.name in ("COMMA", "RBRACE"):
                    raise Exception("Invalid syntax")
                if self.current_token.name == "COMMA":
                    self.advance()
            node = Node("DICT", exprs)
            self.advance()
        elif self.current_token.name in [i.upper() for i in KEYWORDS]:
            node = Node("NONE", None)
        elif self.current_token.name == "EOF":
            return Node("EOF", None)
        elif self.current_token.name == "NEWLINE":
            self.advance()
            return Node("EOL", None)
        else:
            print(self.lines)
            raise Exception("Invalid syntax")
        return node