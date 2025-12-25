class HinglishError(Exception):
    def __init__(self, message, line=None, code_line=None, col=None):
        # output = "💀 fuck bhaii: " + message
        output = "💀 areee bhaii, error aagyaa: " + message
        if line and code_line and col is not None:
            output += f"\n    {code_line}\n    {' ' * col}^ yahin galti"
        super().__init__(output)
