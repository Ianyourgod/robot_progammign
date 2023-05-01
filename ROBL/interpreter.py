class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.custom_functions = {}
        self.classes = {}
        self.prev_if = False

    def custom_function(self, function, call_args: dict, call_name: str):
        self.custom_functions[call_name] = (function, call_args)
        return function
    
    def interpret(self, ast):
        
        ## VALUES ##
        
        if ast.type == "INT":
            return int(ast.left)
        elif ast.type == "FLOAT":
            return float(ast.left)
        elif ast.type == "STRING":
            return ast.left
        elif ast.type == "BOOL":
            return ast.left
        elif ast.type == "IDENTIFIER":
            if ast.left in self.variables:
                return self.variables[ast.left]
            elif ast.left in self.functions:
                return self.functions[ast.left][1]
            else:
                raise Exception(f"Variable {ast.left} not defined")
        elif ast.type == "NONE":
            return None
        elif ast.type == "TUPLE":
            return tuple([self.interpret(i) for i in ast.left])
        elif ast.type == "LIST":
            return [self.interpret(i) for i in ast.left]
        elif ast.type == "DICT":
            return {self.interpret(i): self.interpret(j) for i, j in ast.left}

        ## MATH ##

        elif ast.type == "ADD":
            return self.interpret(ast.left) + self.interpret(ast.right)
        elif ast.type == "SUB":
            return self.interpret(ast.left) - self.interpret(ast.right)
        elif ast.type == "MUL":
            return self.interpret(ast.left) * self.interpret(ast.right)
        elif ast.type == "DIV":
            return self.interpret(ast.left) / self.interpret(ast.right)
        elif ast.type == "MOD":
            return self.interpret(ast.left) % self.interpret(ast.right)
        elif ast.type == "EXP":
            return self.interpret(ast.left) ** self.interpret(ast.right)
        elif ast.type == "FLOORDIV":
            return self.interpret(ast.left) // self.interpret(ast.right)

        ## COMPARISONS ##

        elif ast.type == "EQ":
            return self.interpret(ast.left) == self.interpret(ast.right)
        elif ast.type == "NEQ":
            return self.interpret(ast.left) != self.interpret(ast.right)
        elif ast.type == "LT":
            return self.interpret(ast.left) < self.interpret(ast.right)
        elif ast.type == "GT":
            return self.interpret(ast.left) > self.interpret(ast.right)
        elif ast.type == "LTE":
            return self.interpret(ast.left) <= self.interpret(ast.right)
        elif ast.type == "GTE":
            return self.interpret(ast.left) >= self.interpret(ast.right)
        elif ast.type == "AND":
            return self.interpret(ast.left) and self.interpret(ast.right)
        elif ast.type == "OR":
            return self.interpret(ast.left) or self.interpret(ast.right)
        elif ast.type == "NOT":
            return not self.interpret(ast.right)
        
        ## STATEMENTS ##

        elif ast.type == "ASSIGN":
            self.variables[ast.left.left] = self.interpret(ast.right)
        elif ast.type == "ADD_ASSIGN":
            self.variables[ast.left.left] += self.interpret(ast.right)
        elif ast.type == "SUB_ASSIGN":
            self.variables[ast.left.left] -= self.interpret(ast.right)
        elif ast.type == "MUL_ASSIGN":
            self.variables[ast.left.left] *= self.interpret(ast.right)
        elif ast.type == "DIV_ASSIGN":
            self.variables[ast.left.left] /= self.interpret(ast.right)
        elif ast.type == "MOD_ASSIGN":
            self.variables[ast.left.left] %= self.interpret(ast.right)
        elif ast.type == "EXP_ASSIGN":
            self.variables[ast.left.left] **= self.interpret(ast.right)
        elif ast.type == "INT_DIV_ASSIGN":
            self.variables[ast.left.left] //= self.interpret(ast.right)
        elif ast.type == "IF":
            cond = bool(self.interpret(ast.left))
            self.prev_if = cond
            if cond:
                for line in ast.right:
                    self.interpret(line)
        elif ast.type == "ELIF":
            cond = bool(self.interpret(ast.left))
            if cond and not self.prev_if:
                for line in ast.right:
                    self.interpret(line)
            self.prev_if = cond
        elif ast.type == "ELSE":
            if not self.prev_if:
                for line in ast.left:
                    self.interpret(line)

        ## FUNCTIONS ##

        elif ast.type == "CALL":
            if ast.left.left in self.functions:
                args, lines = self.functions[ast.left.left]
                if len(args) != len(ast.right):
                    raise Exception(f"Function {ast.left.left} takes {len(args)} arguments, {len(ast.right)} given")
                temp_interpreter = Interpreter()
                for i, j in zip(args, ast.right):
                    temp_interpreter.variables[i] = self.interpret(j)
                for line in lines:
                    ret = temp_interpreter.interpret(line)
                    if type(ret) == tuple and ret[0] == "RETURN":
                        return ret[1]
            else:
                raise Exception(f"Function {ast.left} not defined")
        elif ast.type == "DEF":
            name = ast.left
            lines = ast.right[1]
            args = ast.right[0]
            self.functions[name] = (args, lines)
        elif ast.type == "RETURN":
            return ("RETURN", self.interpret(ast.left))
