# BhashIsh 
*A Hinglish-based Programming Language*

BhashIsh is a small, educational, interpreter-based programming language written in Python, created for fun purposes.
It is designed to demonstrate **core compiler design concepts**—lexing, parsing, AST construction, and interpretation—using a **Hinglish-inspired syntax** that feels natural to Indian learners.

The language prioritizes:
- readability over symbols,
- beginner-friendly error messages,
- and a clean, layered compiler architecture.

---

## ✨ Key Features

- Hinglish keywords (`maan lo`, `jab tak`, `chhaap`)
- Natural language arithmetic (`kam kar`, `badha kar`, etc.)
- Indentation-based blocks (Python-style)
- REPL + `.hl` file execution
- Modular imports (`laao "module_name"`)
- Developer-friendly Hinglish errors (`💀 fuck bhaii`)
- Designed explicitly for **Compiler Design coursework**

---

## 📂 Project Structure
```
bhashish/
│
├── lexer.py         # Lexical analysis (tokenization)
├── parser.py        # Syntax analysis (AST generation)
├── interpreter.py   # Semantic execution
├── keywords.py      # Language vocabulary
├── errors.py        # Custom Hinglish errors
├── main.py          # CLI, REPL, module loader
│
└── examples/
├── test.hl
└── math_utils.hl
```

---

## ▶️ How to Run

### Run a file
```bash
cd language
python3 main.py examples/test.hl
```

### Start REPL
Blank line executes the buffered code.
```bash
cd language
python3 main.py
```

### Set it up for VSCode
- Press Ctrl + Shift + P
- Type → **Developer: Install Extension from Location**
- Select **bhashish-vscode/** folder
- Reload VS Code Window


## Language Syntax Examples

Variable assignment
```text
maan lo x hai 5
```

Arithmetic (no symbols!)
```text
x hai x me 1 kam kar
x hai x me 2 badha kar
```

Conditional
```text
agar x > 2 toh
    chhaap x
warna
    chhaap 0
```

Loop
```text
jab tak
    chhaap x
    x hai x me 1 kam kar
tab tak x > 0
```

Importing modules
```text
laao "math_utils"
```

# Debug Helpers
```text
dikhao variables
ruk jao
```

# Compiler Design Perspective (CFG)
BHASHISH is defined using a Context-Free Grammar (CFG).

Non-Terminals (V)
```
V = {
  Program, StmtList, Stmt,
  Assign, Expr, Condition,
  Loop, IfStmt, ImportStmt,
  ForStmt, Value, Identifier
}
```

Terminals (T)
```bash
T = {
  'maan lo', 'hai', 'me',
  'kam kar', 'badha kar', 'guna kar', 'bhaag kar',
  'agar', 'toh', 'warna',
  'jab tak', 'tab tak',
  'chhaap', 'laao',
  IDENTIFIER, NUMBER, STRING,
  INDENT, DEDENT, NEWLINE
}
```

Start Symbol (S)
```
S = Program
```

Production Rules (P)
```sql
Program → StmtList

StmtList → Stmt StmtList | ε

Stmt →
    Assign
  | IfStmt
  | Loop
  | ImportStmt
  | ForStmt
  | PrintStmt
  | DebugStmt

Assign →
    'maan lo' Identifier 'hai' Value
  | Identifier 'hai' Identifier 'me' Value OpPhrase

OpPhrase →
    'kam kar' | 'badha kar' | 'guna kar' | 'bhaag kar'

IfStmt →
    'agar' Condition 'toh' NEWLINE INDENT StmtList DEDENT
    'warna' NEWLINE INDENT StmtList DEDENT

Loop →
    'jab tak' NEWLINE INDENT StmtList DEDENT
    'tab tak' Condition

Condition →
    Identifier RelOp Value

RelOp →
    '>' | '<' | '==' | '!='

ImportStmt →
    'laao' STRING

Value →
    NUMBER | STRING | Identifier | Constant

```

## Architecture Notes
- Lexer converts Hinglish source into tokens.
- Parser builds a lightweight AST using tuples.
- Interpreter executes AST nodes using an in-memory environment.
- Module loading is handled strictly in main.py (not interpreter) to avoid circular dependencies.


## 📌 License
Feel free to fork, experiment, and extend.

BHASHISH is not just a toy language.
It is a learning tool with personality. 😌🔥


---
