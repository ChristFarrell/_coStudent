import sys
from Parser import Parser
from CodeWriter import CodeWriter

def main():
    if len(sys.argv) != 2:
        print("Usage: python VMTranslator.py file.vm")
        return

    vm_file = sys.argv[1]
    asm_file = vm_file.replace(".vm", ".asm")

    parser = Parser(vm_file)
    code_writer = CodeWriter(asm_file)

    while parser.hasMoreCommands():
        parser.advance()
        ctype = parser.commandType()

        if ctype == "C_ARITHMETIC":
            code_writer.writeArithmetic(parser.arg1())
        elif ctype in ["C_PUSH", "C_POP"]:
            code_writer.writePushPop(ctype, parser.arg1(), parser.arg2())

    code_writer.close()

if __name__ == "__main__":
    main()
