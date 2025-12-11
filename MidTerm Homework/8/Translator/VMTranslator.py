import os
import sys
from Parser import Parser
from CodeWriter import CodeWriter

def main():
    """
    Main function to drive the VM translation process.
    Handles file and directory input and orchestrates the parsing and code generation.
    """
    if len(sys.argv) != 2:
        print("Usage: python VMtranslator.py <file.vm or directory>")
        sys.exit(1)

    input_path = sys.argv[1]
    files_to_translate = []
    output_filename = ""

    if os.path.isdir(input_path):
        directory_path = os.path.abspath(input_path)
        directory_name = os.path.basename(directory_path)
        output_filename = os.path.join(directory_path, directory_name + ".asm")
        for file in os.listdir(input_path):
            if file.endswith(".vm"):
                files_to_translate.append(os.path.join(directory_path, file))
    elif os.path.isfile(input_path) and input_path.endswith(".vm"):
        file_path = os.path.abspath(input_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_filename = os.path.join(os.path.dirname(file_path), base_name + ".asm")
        files_to_translate.append(file_path)
    else:
        print("Invalid input: Please provide a .vm file or a directory containing .vm files.")
        sys.exit(1)

    with CodeWriter(output_filename) as code_writer:
        # Only write bootstrap code if Sys.vm exists
        has_sys = any("Sys.vm" in f for f in files_to_translate)
        if has_sys:
            code_writer.write_init()

        for file_path in files_to_translate:
            file_name = os.path.basename(file_path)
            code_writer.set_file_name(os.path.splitext(file_name)[0])
            parser = Parser(file_path)
            while parser.has_more_commands():
                parser.advance()
                command_type = parser.command_type()

                if command_type == "C_ARITHMETIC":
                    code_writer.write_arithmetic(parser.arg1())
                elif command_type in ["C_PUSH", "C_POP"]:
                    code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
                elif command_type == "C_LABEL":
                    code_writer.write_label(parser.arg1())
                elif command_type == "C_GOTO":
                    code_writer.write_goto(parser.arg1())
                elif command_type == "C_IF":
                    code_writer.write_if(parser.arg1())
                elif command_type == "C_FUNCTION":
                    code_writer.write_function(parser.arg1(), parser.arg2())
                elif command_type == "C_CALL":
                    code_writer.write_call(parser.arg1(), parser.arg2())
                elif command_type == "C_RETURN":
                    code_writer.write_return()

if __name__ == "__main__":
    main()