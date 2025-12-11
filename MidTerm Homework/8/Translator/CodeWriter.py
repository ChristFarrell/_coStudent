class CodeWriter:
    """
    Translates VM commands into Hack assembly code. This is the final, correct version.
    """

    def __init__(self, output_file):
        self.file = open(output_file, 'w')
        self.label_counter = 0
        self.current_file_name = ""
        self.current_function_name = "null"

    def set_file_name(self, file_name):
        self.current_file_name = file_name

    def write_arithmetic(self, command):
        if command == "add": self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n")
        elif command == "sub": self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n")
        elif command == "neg": self.file.write("@SP\nA=M-1\nM=-M\n")
        elif command == "eq": self.write_comparison("JEQ")
        elif command == "gt": self.write_comparison("JGT")
        elif command == "lt": self.write_comparison("JLT")
        elif command == "and": self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n")
        elif command == "or": self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n")
        elif command == "not": self.file.write("@SP\nA=M-1\nM=!M\n")

    def write_comparison(self, jump_type):
        true_label = f"COMP_TRUE_{self.label_counter}"
        end_label = f"COMP_END_{self.label_counter}"
        self.label_counter += 1
        self.file.write(f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@{true_label}\nD;{jump_type}\n@SP\nA=M-1\nM=0\n@{end_label}\n0;JMP\n({true_label})\n@SP\nA=M-1\nM=-1\n({end_label})\n")

    def write_push_pop(self, command, segment, index):
        self.resolve_address(segment, index)
        if command == "C_PUSH":
            if segment == "constant":
                self.file.write("D=A\n")
            else:
                self.file.write("D=M\n")
            self.file.write("@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif command == "C_POP":
            self.file.write("D=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def resolve_address(self, segment, index):
        if segment == "constant": self.file.write(f"@{index}\n")
        elif segment == "local": self.file.write(f"@{index}\nD=A\n@LCL\nA=M+D\n")
        elif segment == "argument": self.file.write(f"@{index}\nD=A\n@ARG\nA=M+D\n")
        elif segment == "this": self.file.write(f"@{index}\nD=A\n@THIS\nA=M+D\n")
        elif segment == "that": self.file.write(f"@{index}\nD=A\n@THAT\nA=M+D\n")
        elif segment == "pointer": self.file.write(f"@{3 + index}\n")
        elif segment == "temp": self.file.write(f"@{5 + index}\n")
        elif segment == "static": self.file.write(f"@{self.current_file_name}.{index}\n")

    def write_init(self):
        self.file.write("@256\nD=A\n@SP\nM=D\n")
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        self.file.write(f"({self.current_function_name}${label})\n")

    def write_goto(self, label):
        self.file.write(f"@{self.current_function_name}${label}\n0;JMP\n")

    def write_if(self, label):
        self.file.write("@SP\nAM=M-1\nD=M\n"f"@{self.current_function_name}${label}\nD;JNE\n")

    def write_function(self, function_name, num_locals):
        self.file.write(f"({function_name})\n")
        self.current_function_name = function_name
        for _ in range(num_locals):
            self.write_push_pop("C_PUSH", "constant", 0)

    def write_call(self, function_name, num_args):
        return_address = f"{function_name}$ret.{self.label_counter}"
        self.label_counter += 1
        self.file.write(f"@{return_address}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self.file.write(f"@{segment}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.file.write(f"@SP\nD=M\n@5\nD=D-A\n@{num_args}\nD=D-A\n@ARG\nM=D\n")
        self.file.write("@SP\nD=M\n@LCL\nM=D\n")
        self.file.write(f"@{function_name}\n0;JMP\n")
        self.file.write(f"({return_address})\n")

    def write_return(self):
        # FRAME = LCL (FRAME is a temp var, R13)
        self.file.write("@LCL\nD=M\n@R13\nM=D\n")
        # RET = *(FRAME - 5) (RET is a temp var, R14)
        self.file.write("@5\nA=D-A\nD=M\n@R14\nM=D\n")
        # *ARG = pop()
        self.file.write("@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n")
        # SP = ARG + 1
        self.file.write("@ARG\nD=M+1\n@SP\nM=D\n")
        # THAT = *(FRAME - 1)
        self.file.write("@R13\nAM=M-1\nD=M\n@THAT\nM=D\n")
        # THIS = *(FRAME - 2)
        self.file.write("@R13\nAM=M-1\nD=M\n@THIS\nM=D\n")
        # ARG = *(FRAME - 3)
        self.file.write("@R13\nAM=M-1\nD=M\n@ARG\nM=D\n")
        # LCL = *(FRAME - 4)
        self.file.write("@R13\nAM=M-1\nD=M\n@LCL\nM=D\n")
        # goto RET
        self.file.write("@R14\nA=M\n0;JMP\n")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()