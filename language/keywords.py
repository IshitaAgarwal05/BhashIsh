KEYWORDS = {
    "chhaap": "PRINT",
    "agar": "IF",
    "toh": "THEN",
    "warna": "ELSE",
    "jab tak": "WHILE",
    "tab tak": "DO",
    "maan lo": "LET",
    "har ek": "FOR",
    "bta": "INPUT",
    "laao": "IMPORT",
    "dikhao": "DEBUG",
    "ruk jao": "PAUSE"
}

# since multi-word keywords ko pehle match karna hota hai
MULTI_WORD_KEYWORDS = [
    "jab tak", "tab tak",
    "maan lo",
    "har ek",
    "fuck bhaii",
    "kam kar", "badha kar", "guna kar", "bhaag kar",
    "ruk jao", "kchh nahi"
]

# operators
OPERATOR_PHRASES = {
    "kam kar": "-",
    "badha kar": "+",
    "guna kar": "*",
    "bhaag kar": "/"
}

LOGIC_OPS = {
    "aur": "AND",
    "ya": "OR",
    "nahi": "NOT",
    "nand": "NAND",
    "nor": "NOR",
    "xor": "XOR"
}


CONNECTORS = ["hai", "me"]

CONSTANTS = {
    "sachhi": True,
    "jhootha": False,
    "kchh nahi": None
}