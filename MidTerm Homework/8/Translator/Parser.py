class Parser:
    """
    Parses a single .vm file, providing access to its components.
    """

    def __init__(self, input_file):
        self.lines = []
        with open(input_file, 'r') as f:
            for line in f:
                line = line.split('//')[0].strip()
                if line:
                    self.lines.append(line)
        self.current_command_index = -1
        self.current_command = None

    def has_more_commands(self):
        return self.current_command_index < len(self.lines) - 1

    def advance(self):
        self.current_command_index += 1
        self.current_command = self.lines[self.current_command_index]

    def command_type(self):
        command = self.current_command.split()[0]
        if command in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return "C_ARITHMETIC"
        elif command == "push": return "C_PUSH"
        elif command == "pop": return "C_POP"
        elif command == "label": return "C_LABEL"
        elif command == "goto": return "C_GOTO"
        elif command == "if-goto": return "C_IF"
        elif command == "function": return "C_FUNCTION"
        elif command == "return": return "C_RETURN"
        elif command == "call": return "C_CALL"

    def arg1(self):
        parts = self.current_command.split()
        if self.command_type() == "C_ARITHMETIC":
            return parts[0]
        else:
            return parts[1]

    def arg2(self):
        parts = self.current_command.split()
        return int(parts[2])