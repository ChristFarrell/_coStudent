# NOTES

All of this project 6-12, I asked AI for 90% to help me write the homework for all of this project. Here is all of references: (Very sorry if this references might not full explain this project, since some of code already disappear/combined with other chat/not saved).
References
- Explanation program 11 & Understanding from chapter 6-12 : https://chatgpt.com/share/694360d4-7e50-8008-ad36-e38569825cac
- Explanation from chapter 1-8 : https://chatgpt.com/share/69436246-6d0c-8008-a129-1303e88a108e
- Explanation from chapter 8 and a bit 12 : https://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221jZp1vEJZl074_cbwJObYXvjrOwP_zMbe%22%5D%2C%22action%22%3A%22open%22%2C%22userId%22%3A%22100059528919497194278%22%2C%22resourceKeys%22%3A%7B%7D%7D&usp=drive_link
- More explanation from chapter 8 : https://drive.google.com/file/d/1RGPoIr9DHZUc98ulOMPv4Q_KV1TqDiRz/view?usp=sharing
- Chapter 12 : https://github.com/havivha/Nand2Tetris/tree/master/12

Presentation: https://www.canva.com/design/DAG5VdKRvfQ/Q2LYzbU7jgEPg035Ui2a1Q/edit

## [Homework 6](https://github.com/ChristFarrell/_coStudent/tree/main/MidTerm%20Homework/6)

On the project 6, this contain of 4 file, which is ADD, MAX, RECT, and PONG. Our main project is to test (.asm) in the CPU Emulator and the results will be loaded in the form of a file (.hack). On prorgram python, it will:<br>
1. Predefined symbols according to the Hack specification.
2. Converts number to binary.
3. Removing comment and spaces.
4. Make instruction for instruction A and instruction C (dest/comp/jump).

At the end, the result of (.hack) file is succeed.

## [Homework 7](https://github.com/ChristFarrell/_coStudent/tree/main/MidTerm%20Homework/7)

On the project 7, We asked to create a translator that converts VM code (.vm) to Hack Assembly (.asm). In Parser.py, it will read the VM command. Then in CodeWriter.py, it will translate VM to ASM. VMTranslator will manage the overall flow. This project will translate stact operations and memory. For the Parser.py, the program will:<br>
1. Looking for the next valid VM line.
2. Reads one VM instruction and stored it
3. Determines whether the instruction is: push, pop, or arithmetic
4. Collecting the command arguments.

For the codewriter.py, it will write Arithmetic and write PushPop. After that the VM Translator translates VM commands such as arithmetic, push/pop, branching, and function calls into Hack Assembly instructions. Each VM instruction is converted into a series of stack operations and pointer manipulations that can be executed by the Hack hardware. In the end, the VM Translator will generate an assembly (.asm) file based on all the Memory Access and Stack Arithmetic commands. <br>

## [Homework 8](https://github.com/ChristFarrell/_coStudent/tree/main/MidTerm%20Homework/8)

On the project 8, it using Same concept as homework 7, as example Parser.py, CodeWriter.py, and VMTranslator. But now it’s more advanced. The different on parser.py, it using new instructions for Program Flow and Function Handling. For codewriter.py, it contain:
1. write_init, that work to bootstrap Sys.init.
2. write_label, that create local labels on functions.
3. write_goto, that make unconditional jump
4. write_if, that make conditional jump.
5. write_function defines a new function.
6. write_call and write return.

In the end, the VM Translator will generate a complete assembly (.asm) file containing translations of all VM commands, including Memory Access, Stack Arithmetic, Program Flow, and Function Call. <br>

## [Homework 9](https://github.com/ChristFarrell/_coStudent/tree/main/MidTerm%20Homework/9)

On the project 9, we use code Jack. Jack is a high-level language similar to Java, which is object-oriented. Jack has formal syntax, classes, methods, functions, and constructors. Jack used to write game or OS programs because it supports classes, methods, variables, etc. Ultimately, we can build a path between Jack Code and VM to Hardware. For more explanation abouat how translate the jack to VM, take a look in project 11.<br>

## [Homework 10](https://github.com/ChristFarrell/_coStudent/tree/main/MidTerm%20Homework/10)

On the project 10, it explains how the compiler reads Jack's program line by line. Tokenizer generates XML that breaks down code into tokens (keywords, symbols, etc.). The parser generates XML that converts tokens into a grammar structure (parse tree).<br>

## [Homework 11](https://github.com/ChristFarrell/_coStudent/tree/main/MidTerm%20Homework/11)

On the project 11, we complete the Jack compiler by creating a code that converts the parse tree into VM instructions. JackCompiler.py will act to translate from the beginning to the .vm file. The code flow of python, contain:
1. Tokenizer, that will converts Jack's text into tokens. The code will be chunked into keywords, symbols, strings, etc.
2. CompilationEngine, that will read Jack's program structure and convert it into VM code.
3. SymbolTable, that will determine segment & index variables during compilation process.
4. VMWriter, that will write VM instructions such as push, pop, add, call, return, to a .vm file.

As the code will work from tokenizer until VMWriter, the Jack Compiler will generate a complete VM (.vm) file that contains translated instructions for every part of the Jack program including variable handling and instructions (pop, push, add, not, call, etc).<br>

## [Homework 12](https://github.com/ChristFarrell/_coStudent/tree/main/MidTerm%20Homework/12)

On the project 12, we were asked to explain the Operation System (OS) code that was provided via GitHub Havivha. Here it explanation all of the jack and the connection with other program jack..
1. Sys, initializes all components jack, including Start, Wait, Stop, Error.
2. Memory, acts as a basic foundation that runs without other OS components.
3. Array, a “box” for storing multiple values. Array.new borrows space from memory, Array.dispose returns that space.
4. Math, the computer's built-in calculator. It requires Arrays to perform calculations and indirectly calls memory to store the results.
5. String, represents text as an array of characters. Uses Memory for storage allocation. and Uses Math to convert numbers to text or text to numbers.
6. Screen, draws graphics (geometry) by manipulating bits in a Memory Map. It uses Math for geometric calculations and Arrays for bitwise operations (masking).
7. Keyboard, requires output to display what the user types. Strings are used to create buffers (reading letters/numbers). Also access memory directly (24576) and indirectly from Strings.
8. Output, it prints text to the screen (hardware) using String for text manipulation, Array for font maps, and Math to calculate pixel positions. It writes directly to Video Memory (RAM 16384) without using the Screen class.
