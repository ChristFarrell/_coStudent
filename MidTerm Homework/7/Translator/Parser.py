class Parser:
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.current = None
        self.index = 0

    def hasMoreCommands(self):
        while self.index < len(self.lines):
            line = self.lines[self.index]
            if line and not line.startswith("//"):
                return True
            self.index += 1
        return False

    def advance(self):
        self.current = self.lines[self.index].split("//")[0].strip()
        self.index += 1

    def commandType(self):
        if self.current.startswith("push"):
            return "C_PUSH"
        elif self.current.startswith("pop"):
            return "C_POP"
        else:
            return "C_ARITHMETIC"

    def arg1(self):
        parts = self.current.split()
        if self.commandType() == "C_ARITHMETIC":
            return parts[0]
        return parts[1]

    def arg2(self):
        parts = self.current.split()
        return int(parts[2]) if len(parts) > 2 else None
