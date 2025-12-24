# interpreter.py

from errors import HinglishError


class Interpreter:
    def __init__(self):
        self.variables = {}

    def eval_condition(self, cond):
        if cond[0] == "REL_COND":
            _, left, op, right = cond
            if left not in self.variables:
                raise HinglishError(f"{left} defined hi nahi hai")

            if op == ">":
                return self.variables[left] > right
            if op == "<":
                return self.variables[left] < right
            if op == "==":
                return self.variables[left] == right

        if cond[0] == "LOGIC_COND":
            return self.eval_logic_cond(cond)

        raise HinglishError("condition samajh nahi aayi")

    def eval_logic_cond(self, cond):
        # Unary NOT
        if len(cond) == 3:
            _, op, var = cond
            if var not in self.variables:
                raise HinglishError(f"{var} defined hi nahi hai")
            val = self.variables[var]

            if op == "NOT":
                return not val

        # Binary logical ops
        _, op, left, right = cond

        if left not in self.variables:
            raise HinglishError(f"{left} defined hi nahi hai")
        if right not in self.variables:
            raise HinglishError(f"{right} defined hi nahi hai")

        a = self.variables[left]
        b = self.variables[right]

        if op == "AND":
            return a and b
        if op == "OR":
            return a or b
        if op == "NAND":
            return not (a and b)
        if op == "NOR":
            return not (a or b)
        if op == "XOR":
            return a != b

        raise HinglishError("unknown logical operator")


    def execute(self, ast):
        for stmt in ast:
            self.exec_stmt(stmt)

    def exec_stmt(self, stmt):
        kind = stmt[0]

        if kind == "LET":
            _, var, value = stmt
            self.variables[var] = value

        elif kind == "PRINT":
            value = stmt[1]
            if value in self.variables:
                print(self.variables[value])
            else:
                print(value)

        elif kind == "INPUT":
            _, msg, var = stmt
            self.variables[var] = int(input(msg))

        elif kind == "FOR":
            _, var, iterable, body = stmt
            if iterable not in self.variables:
                raise HinglishError(f"{iterable} defined hi nahi hai")
            for v in self.variables[iterable]:
                self.variables[var] = v
                self.execute(body)

        elif kind == "IMPORT":
            _, module = stmt
            raise HinglishError(
                f"module '{module}' load nahi hua — interpreter ko loader chahiye"
            )

        elif kind == "DEBUG":
            print("🧠 VARIABLES:", self.variables)

        elif kind == "PAUSE":
            input("⏸ ruk gaya… Enter dabao")

        elif kind == "IF":
            _, cond, then_block, else_block = stmt
            if self.eval_condition(cond):
                self.execute(then_block)
            else:
                self.execute(else_block)

        elif kind == "WHILE":
            _, cond, body = stmt
            while self.eval_condition(cond):
                self.execute(body)

        elif kind == "DO_WHILE":
            _, cond, body = stmt
            while True:
                self.execute(body)
                if not self.eval_condition(cond):
                    break

        elif kind == "ASSIGN_OP":
            _, target, source, op, value = stmt

            if source not in self.variables:
                raise HinglishError(f"{source} defined hi nahi hai")

            src_val = self.variables[source]

            if isinstance(value, str):
                if value not in self.variables:
                    raise HinglishError(f"{value} defined hi nahi hai")
                val = self.variables[value]
            else:
                val = value

            if op == "-":
                self.variables[target] = src_val - val
            elif op == "+":
                self.variables[target] = src_val + val
            elif op == "*":
                self.variables[target] = src_val * val
            elif op == "/":
                self.variables[target] = src_val // val
