# parser.py

from errors import HinglishError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type=None):
        token = self.current()
        if token is None:
            return None

        if token_type and token[0] != token_type:
            raise HinglishError(
                f"line {token[2]}: expected {token_type}, mila {token[0]}"
            )

        self.pos += 1
        return token


    def block(self):
        stmts = []
        self.eat("INDENT")

        while self.current() and self.current()[0] != "DEDENT":
            stmt = self.statement()
            if stmt is not None:
                stmts.append(stmt)

        self.eat("DEDENT")
        return stmts


    # -------- STATEMENTS -------- #

    def parse(self):
        statements = []

        while self.current():
            if self.current()[0] == "NEWLINE":
                self.eat("NEWLINE")
                continue

            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)

        return statements


    def statement(self):
        token = self.current()

        # ignore blank lines
        if token[0] == "NEWLINE":
            self.eat("NEWLINE")
            return None

        # Hinglish math assignment
        if (
            token[0] == "IDENTIFIER" and
            self.tokens[self.pos + 1][0] == "CONNECTOR"
        ):
            return self.hinglish_assignment_expr()
        
        if token[0] == "LET":
            return self.let_statement()

        if token[0] == "PRINT":
            return self.print_statement()

        if token[0] == "INPUT":
            return self.input_statement()

        if token[0] == "FOR":
            return self.for_statement()

        if token[0] == "IMPORT":
            return self.import_statement()

        if token[0] == "DEBUG":
            self.eat("DEBUG")
            # optional identifier after debug (e.g. "dikhao variables"); consume if present
            if self.current() and self.current()[0] == "IDENTIFIER":
                self.eat("IDENTIFIER")
            return ("DEBUG",)

        if token[0] == "PAUSE":
            self.eat("PAUSE")
            return ("PAUSE",)

        if token[0] == "IF":
            return self.if_statement()

        if token[0] == "WHILE":
            # lookahead for DO-WHILE
            if any(t[0] == "DO" for t in self.tokens[self.pos:]):
                return self.do_while_statement()
            return self.while_statement()

        if token[0] == "DO":
            raise HinglishError("tab tak akela mat use kar bhaii, pehle 'jab tak' aata hai")

        raise HinglishError(f"ye statement samajh nahi aaya: {token}")



    # -------- INDIVIDUAL STATEMENTS -------- #
    def let_statement(self):
        self.eat("LET")
        var = self.eat("IDENTIFIER")[1]
        self.eat("CONNECTOR")      # hai

        # simple value OR expression
        if self.current()[0] == "NUMBER":
            value = self.eat("NUMBER")[1]
            return ("LET", var, value)

        elif self.current()[0] == "LIST":
            value = self.eat("LIST")[1]
            return ("LET", var, value)

        elif self.current()[0] == "IDENTIFIER":
            expr = self.expression()
            return ("LET_EXPR", var, expr)

        else:
            raise HinglishError("assignment ke baad kuchh gadbad hai bhaii")


    def print_statement(self):
        self.eat("PRINT")
        value = self.eat()[1]
        return ("PRINT", value)

    def input_statement(self):
        self.eat("INPUT")                  # bta
        msg = self.eat("STRING")[1]
        self.eat("IDENTIFIER")              # integer
        var = self.eat("IDENTIFIER")[1]
        return ("INPUT", msg, var)


    def for_statement(self):
        self.eat("FOR")                     # har ek
        var = self.eat("IDENTIFIER")[1]
        iterable = self.eat("IDENTIFIER")[1]
        self.eat("CONNECTOR")               # me
        self.eat("NEWLINE")
        body = self.block()
        return ("FOR", var, iterable, body)


    def import_statement(self):
        self.eat("IMPORT")
        token = self.eat("STRING")
        return ("IMPORT", token[1])

    def condition(self):
        token = self.current()

        # Unary NOT
        if token[0] == "LOGIC_OP" and token[1] == "NOT":
            op = self.eat("LOGIC_OP")[1]
            var = self.eat("IDENTIFIER")[1]
            return ("LOGIC_COND", op, var)

        # Binary logical condition
        left = self.eat("IDENTIFIER")[1]

        op_token = self.eat()
        if op_token[0] == "LOGIC_OP":
            op = op_token[1]
            right = self.eat("IDENTIFIER")[1]
            return ("LOGIC_COND", op, left, right)

        # Fallback to relational condition
        op = op_token[1]   # >, <, ==
        right = self.eat("NUMBER")[1]
        return ("REL_COND", left, op, right)


    def if_statement(self):
        self.eat("IF")
        cond = self.condition()
        self.eat("THEN")
        self.eat("NEWLINE")

        then_block = self.block()

        else_block = []
        if self.current() and self.current()[0] == "ELSE":
            self.eat("ELSE")
            self.eat("NEWLINE")
            else_block = self.block()

        return ("IF", cond, then_block, else_block)

    def while_statement(self):
        self.eat("WHILE")
        self.eat("NEWLINE")
        body = self.block()
        return ("WHILE", None, body)

    def do_while_statement(self):
        self.eat("WHILE")   # jab tak

        body = []
        while self.current() and self.current()[0] != "DO":
            body.append(self.statement())

        self.eat("DO")      # tab tak
        cond = self.condition()

        return ("DO_WHILE", cond, body)

    def hinglish_assignment_expr(self):
        target = self.eat("IDENTIFIER")[1]
        self.eat("CONNECTOR")          # hai

        source = self.eat("IDENTIFIER")[1]
        self.eat("CONNECTOR")          # me

        val_token = self.eat()         # NUMBER or IDENTIFIER

        if val_token[0] not in ("NUMBER", "IDENTIFIER"):
            raise HinglishError(
                f"line {val_token[2]}: yahan number ya variable expected tha"
            )

        value = val_token[1]
        op = self.eat("HING_OP")[1]

        return ("ASSIGN_OP", target, source, op, value)
