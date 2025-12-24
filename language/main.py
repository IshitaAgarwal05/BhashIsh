# main.py

import sys
import os
from lexer import lexer
from parser import Parser
from interpreter import Interpreter
from errors import HinglishError


def run_code(code, interpreter=None, base_path="."):
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()

    if interpreter is None:
        interpreter = Interpreter()

    for stmt in ast:
        if stmt[0] == "IMPORT":
            _, module = stmt
            module_path = os.path.join(base_path, f"{module}.hl")
            try:
                with open(module_path) as f:
                    module_code = f.read()
                run_code(module_code, interpreter, base_path)
            except FileNotFoundError:
                raise HinglishError(f"module '{module}' nahi mila")
        else:
            interpreter.exec_stmt(stmt)

    return interpreter



def repl():
    print("🔥 HinglishLang REPL")
    print("💡 likhna shuru karo, blank line pe execute hoga")
    print("💀 exit ke liye Ctrl+C\n")

    buffer = ""
    interpreter = Interpreter()

    try:
        while True:
            prompt = ">>> " if not buffer else "... "
            line = input(prompt)

            if line.strip() == "":
                if buffer.strip():
                    try:
                        interpreter = run_code(buffer, interpreter)
                    except HinglishError as e:
                        print(e)
                    buffer = ""
                continue

            buffer += line + "\n"

    except KeyboardInterrupt:
        print("\n👋 bhaii REPL band ho gaya")


if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            repl()

        elif len(sys.argv) == 2:
            filename = sys.argv[1]

            if not filename.endswith(".hl"):
                raise HinglishError("sirf .hl file chalayegi bhaii")

            with open(filename, "r") as f:
                code = f.read()

            base_path = os.path.dirname(filename) or "."
            run_code(code, None, base_path)


        else:
            print("💡 Usage:")
            print("   python main.py        # REPL")
            print("   python main.py file.hl")

    except HinglishError as e:
        print(e)
