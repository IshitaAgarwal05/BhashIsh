# lexer.py

import re
from errors import HinglishError
from keywords import KEYWORDS, MULTI_WORD_KEYWORDS, OPERATOR_PHRASES, LOGIC_OPS, CONNECTORS, CONSTANTS

INDENT_WIDTH = 4

def lexer(code):
    tokens = []
    indent_stack = [0]
    line_no = 0

    lines = code.split("\n")

    for line in lines:
        line_no += 1
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip(" "))
        content = line.lstrip(" ")

        if indent > indent_stack[-1]:
            tokens.append(("INDENT", None, line_no))
            indent_stack.append(indent)

        while indent < indent_stack[-1]:
            tokens.append(("DEDENT", None, line_no))
            indent_stack.pop()

        # ---- normal tokenization ----
        # collapse spaces inside quoted strings so they stay a single word during split
        content = re.sub(r'"[^\"]*"', lambda m: m.group(0).replace(' ', '<<<SPACE>>>'), content)

        for kw in MULTI_WORD_KEYWORDS:
            content = content.replace(kw, kw.replace(" ", "_"))

        # collapse spaces inside list literals so e.g. "[1, 2, 3]" becomes "[1,2,3]"
        content = re.sub(r'\[\s*([^\]]*?)\s*\]', lambda m: '[' + ','.join([p.strip() for p in m.group(1).split(',')]) + ']', content)

        words = content.split()

        for word in words:
            # string literal (restore spaces inside quoted strings replaced earlier)
            if word.startswith('"') and word.endswith('"'):
                tokens.append(("STRING", word.strip('"').replace('<<<SPACE>>>', ' '), line_no))
                continue

            # list literal
            elif word.startswith("[") and word.endswith("]"):
                items = word.strip("[]").split(",")
                values = [int(i.strip()) for i in items]
                tokens.append(("LIST", values, line_no))
                continue

            # restore underscores for multi-word keywords but not for strings
            word = word.replace("_", " ")

            if word in KEYWORDS:
                tokens.append((KEYWORDS[word], word, line_no))

            elif word in OPERATOR_PHRASES:
                tokens.append(("HING_OP", OPERATOR_PHRASES[word], line_no))

            # Logical operators
            elif word in LOGIC_OPS:
                tokens.append(("LOGIC_OP", LOGIC_OPS[word], line_no))

            elif word in CONSTANTS:
                tokens.append(("CONST", CONSTANTS[word], line_no))

            elif word.isdigit():
                tokens.append(("NUMBER", int(word), line_no))
            elif word in CONNECTORS:
                tokens.append(("CONNECTOR", word, line_no))            

            elif word in [">", "<", "=="]:
                tokens.append(("OPERATOR", word, line_no))
            elif word == "=":
                tokens.append(("OPERATOR", "=", line_no))

            # Identifiers (LAST OPTION)
            elif re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", word):
                tokens.append(("IDENTIFIER", word, line_no))
            else:
                raise HinglishError(f"line {line_no}: samajh nahi aaya '{word}'")

        tokens.append(("NEWLINE", None, line_no))

    while len(indent_stack) > 1:
        tokens.append(("DEDENT", None, line_no))
        indent_stack.pop()

    return tokens

