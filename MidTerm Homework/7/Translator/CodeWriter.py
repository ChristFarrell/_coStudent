class CodeWriter:
    def __init__(self, filename):
        self.file = open(filename, "w")
        self.label_counter = 0
        self.filename = filename.split("/")[-1].split("\\")[-1].replace(".asm", "")

    def writeArithmetic(self, command):
        if command in ["add", "sub", "and", "or"]:
            self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\n")
            if command == "add":
                self.file.write("M=M+D\n")
            elif command == "sub":
                self.file.write("M=M-D\n")
            elif command == "and":
                self.file.write("M=M&D\n")
            elif command == "or":
                self.file.write("M=M|D\n")
        elif command in ["neg", "not"]:
            self.file.write("@SP\nA=M-1\n")
            if command == "neg":
                self.file.write("M=-M\n")
            else:
                self.file.write("M=!M\n")
        elif command in ["eq", "gt", "lt"]:
            self.label_counter += 1
            label_true = f"TRUE{self.label_counter}"
            label_end = f"END{self.label_counter}"
            jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}[command]
            self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n")
            self.file.write(f"@{label_true}\nD;{jump}\n")
            self.file.write("@SP\nA=M-1\nM=0\n")
            self.file.write(f"@{label_end}\n0;JMP\n")
            self.file.write(f"({label_true})\n@SP\nA=M-1\nM=-1\n({label_end})\n")

    def writePushPop(self, ctype, segment, index):
        if ctype == "C_PUSH":
            if segment == "constant":
                self.file.write(f"@{index}\nD=A\n")
            elif segment in ["local", "argument", "this", "that"]:
                base = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}[segment]
                self.file.write(f"@{base}\nD=M\n@{index}\nA=D+A\nD=M\n")
            elif segment == "temp":
                self.file.write(f"@{5+index}\nD=M\n")
            elif segment == "pointer":
                self.file.write(f"@{'THIS' if index == 0 else 'THAT'}\nD=M\n")
            elif segment == "static":
                self.file.write(f"@{self.filename}.{index}\nD=M\n")
            self.file.write("@SP\nA=M\nM=D\n@SP\nM=M+1\n")

        elif ctype == "C_POP":
            if segment in ["local", "argument", "this", "that"]:
                base = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}[segment]
                self.file.write(f"@{base}\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n")
                self.file.write("@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == "temp":
                self.file.write("@SP\nAM=M-1\nD=M\n")
                self.file.write(f"@{5+index}\nM=D\n")
            elif segment == "pointer":
                self.file.write("@SP\nAM=M-1\nD=M\n")
                self.file.write(f"@{'THIS' if index == 0 else 'THAT'}\nM=D\n")
            elif segment == "static":
                self.file.write("@SP\nAM=M-1\nD=M\n")
                self.file.write(f"@{self.filename}.{index}\nM=D\n")

    def close(self):
        self.file.close()
