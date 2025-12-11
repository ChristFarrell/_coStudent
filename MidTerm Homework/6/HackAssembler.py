import sys
import re

# ========== SYMBOL TABLE ==========
symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}
for i in range(16):
    symbol_table[f"R{i}"] = i

next_var_addr = 16


# ========== HELPER FUNCTIONS ==========
def to_binary(n: int) -> str:
    """Convert integer to 15-bit binary string"""
    return format(n, "015b")


def trim(line: str) -> str:
    """Remove whitespace and comments"""
    line = re.sub(r"//.*", "", line)
    return line.strip()


# ========== COMP / DEST / JUMP TABLES ==========
comp_table = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101",
}

dest_table = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}

jump_table = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}


# ========== ASSEMBLER CORE ==========
def assemble(filename):
    global next_var_addr
    next_var_addr = 16
    symbol_table = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576,
        **{f"R{i}": i for i in range(16)}
    }

    # --- Load and clean lines ---
    with open(filename, "r") as f:
        raw_lines = [trim(line) for line in f]

    # --- First pass: remove labels, record addresses ---
    rom_addr = 0
    instructions = []

    for line in raw_lines:
        if not line:
            continue
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            symbol_table[label] = rom_addr
        else:
            instructions.append(line)
            rom_addr += 1

    # --- Second pass: translate instructions ---
    output = []
    for line in instructions:

        # A-instruction
        if line.startswith("@"):
            symbol = line[1:]
            if symbol.isdigit():
                addr = int(symbol)
            else:
                if symbol not in symbol_table:
                    symbol_table[symbol] = next_var_addr
                    next_var_addr += 1
                addr = symbol_table[symbol]
            output.append("0" + to_binary(addr))
            continue

        # C-instruction
        dest, comp, jump = "", line, ""
        if "=" in line:
            dest, comp = line.split("=")
        if ";" in comp:
            comp, jump = comp.split(";")

        output.append(
            "111" +
            comp_table[comp.strip()] +
            dest_table[dest.strip()] +
            jump_table[jump.strip()]
        )

    # --- Write file ---
    outname = filename.replace(".asm", ".hack")
    with open(outname, "w") as f:
        f.write("\n".join(output))

    print(f"Finish! Output written to {outname}")

# ========== ENTRY POINT ==========
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python HackAssembler.py file.asm")
        sys.exit(1)

    assemble(sys.argv[1])
