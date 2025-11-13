# NOTES

## [Homework 1]()

On the project 1, we asked to build the basic logic gates (NOT, AND, OR, XOR, MUX, DMUX, etc.) using only NAND gates. This project split for some of part.<br>

1. Logic gates output of NOT = NOT A.
2. Logic gates output of AND = A and B.
3. Logic gates law of OR = a OR b = NOT(NOTa AND NOTb).
4. Logic gates law of XOR = (a AND NOT b) OR (NOT a AND b).
5. Logic gates of Mux (Multiplexer) = choose between a and b based on selector sel, where out = (a AND NOT sel) OR (b AND sel).
6. Logic gates of DMux (Demultiplexer) = send input in to one of two outputs depending on sel.

For the (NOT16, AND16, OR16, XOR16, MUX16, DMUX16), the concept itself still same but instead of single bits, this part using of 16-bit buses.<br>

For the Mux4Way16 and Mux8Way16, use multiple Mux16 chips to choose among 4 or 8 16-bit inputs. Last for DMux4Way, DMux8Way: expand DMux logic to 4 or 8 outputs using two or three levels.<br>

## [Homework 2]()

On the project 2, we asked to build circuits that can perform binary addition and basic arithmetic operations. There are 5 projects inside (A 16-bit Adder, A Full Adder, A Half Adder, A 16-bit Incrementer, ALU).<br>

For A 16-bit Adder, the purpose of this was to adds 2 single bits. The output will be sum and carry. If both bits are 1 → carry = 1. If only one bit is 1 → sum = 1. If both 0 → sum = 0, carry = 0<br>

For A Full Adder, the purpose of this was to adds 2 single bits + carry input. The output will be Outputs: sum, carry (carry-out). The building was combine of two HalfAdders with one OR gate.<br>

For A Half Adder, the purpose of this was to adds two 16-bit numbers. The output will be out[16].<br>

For A 16-bit Inclementer, the purpose of this was to increments a 16-bit number by 1. Since we already have Add16, we only adds 1 to the input. At the end, the output will be out[16].<br>

For ALU, since we already build logic gates and adders, now both of them will be combine to make a real working control/circuit that performs logic and math operations. The ALU can clear x or y (zero inputs), negate x or y (invert inputs), either AND or ADD them, possibly negate the final result. Here the process of ALU.<br>

At first, preprocess inputs, where Mux16 selects between original input(a=x or a=y) and zero(false). If zx=1, then x1=0. If zx=0, then x1=x. It's same with zy and y1. Another part is selecting between x1 and nx1. If nx=1, then x2=NOT(x1). If nx=0, then x2=1.<br>

Second, we compute the main operation (AND or ADD). The Mux16 chooses if f=0, then (aAndB). If f=1, then (aPlusB)<br>

Third, we have optional choosing between output negation. The Mux16 chooses if no=0, then it's original. If no=1, then it's negated output.<br> 

The last one is zero flag, where it split for some part checking. o1 = 1 if any bit 0–7 is 1, o2 = 1 if any bit 8–15 is 1, o3 = 1 if any bit in the 16-bit output is nonzero, If none of the bits were 1 → zr=1 (output is zero).<br>

## [Homework 3]()

On the project 3, we already build the combinational logic and now we will let adding of memory — circuits that store data between clock cycles. There are 8 projects inside (Bit, Register, RAM8, RAM64, RAM512, RAM4K, RAM16K, PC).<br>

For Bit, we stores 1 bit of data (0 or 1). If load=0, Mux passes out back into itself (old value). If load=1, Mux passes new in (new value).<br>

For Register, we stores a 16-bit value. Each Bit is independent but shares the same load.<br>

For RAM8, it contains 8 registers (Each 16 bits), that needs a 3-bit address to select the register. Let DMux8Way to select which register gets loaded, and Mux8Way16 to read one output.<br>

For RAM64, it contains 64 registers (8 groups of RAM8), that needs a 6-bit address. Same like before, let DMux8Way to select which register gets loaded, and Mux8Way16 to read one output.<br>

For RAM512, it contains 512 registers (8 x RAM64), that needs a 9-bit address. We also let DMux8Way to select which register gets loaded, and Mux8Way16 to read one output.<br>

For RAM4K, it contains 4096 registers (8 x RAM512), that needs a 12-bit address. Still same, let DMux8Way to select which register gets loaded, and Mux8Way16 to read one output.<br>

For RAM16K, it contains 64 registers (8 x RAM4K), that needs a 14-bit address. Also, let DMux8Way to select which register gets loaded, and Mux8Way16 to read one output.<br>

For PC(Program Counter), It first increments if inc=1, or loads a new address if load=1, or resets to 0 if reset=1. Otherwise keeps current value<br>

## [Homework 4]()

On the project 4, we starting moving from hardware to the software. On this project, we will learn the Hack Machine Language, by writing .asm programs.<br>

For Fill.asm, we continously check if a key is pressed. If pressed, fill the entire screen black. Else, fill the screen white and all of this process will be repeat forever.<br>

At first we make main loop that checking the keyboard. @KBD is memory address 24576 — this special address stores the keyboard state. After that, we make system that if key pressed, it fill black. If no key, it fill white. After the system, we make the drawing loop. At the end once finished filling the screen, go back to (LOOP) to check keyboard again.<br>

For mult.asm, we multiplies two numbers stored in RAM[0] and RAM[1], and puts the product in RAM[2]. At first, we set RAM[2] = RAM[2] + RAM[0]. Next, we check if RAM[0] and RAM[1] is zero, then it's skip to END. After that there are setup loop counter. So, RAM[0] = first number (x) and RAM[3] = counter = x. Each loop iteration will add RAM[1] to the product (RAM[2]) and decrease the counter (RAM[3]). Let it repeat until the counter hits 0.<br>

For example: RAM[0] = 3 ; RAM[1] = 4 ; RAM[2] = 12 (result) ; RAM[3] = Loop counter (decrements each time). This project works only for non-negative integers and work slow on big number.<br>

## [Homework 5]()

On the project 5, after built from logic gates → ALU → registers → memory, we can connects to form the Hack Computer.<br>

For CPU project, it's executes instructions, processes data, and control the system. The CPU takes instruction[16] (from ROM), inM[16] (from Memory), and produces outM, writeM, addressM, and pc.<br>

At first, detect instruction type for ni=1 or ni=0. If ni=1 (A-instruction), then i = instruction. If ni=0 (C-instruction), then i = outtM (the result from ALU).<br>

Second, let control a register loading. If A-instruction (ni=1), always load A If C-instruction and destA=1, also load A, otherwise, don’t load A. After selection, we also selects ALU input Y. If a=0 → use A register. If a=1 → use Memory (inM).<br>

Third, the ALU performs computation. X = D and Y = A or M. The outpus will be outtM (ALU result), zr (zero flag), ng (negative flag). After thast, use the DRegister to update D if needed. Using writeM, write the memory if destM = 1 and the output will be a signal. Last, we using the jump logic and PC.<br>

In short, 
1. If it’s an A-instruction
   - Loads the A register with the specified value.

2. If it’s a C-instruction
   - Performs the ALU computation using D and A/M.
   - Updates A, D, or Memory if dest bits are set.
   - If the jump condition is true, loads A into PC (jumps).

3. Program Counter (PC) behavior
   - Automatically increments after each instruction.
   - Jumps when a valid jump condition is satisfied.

For Memory project, it's defines the entire addressable memory system of the Hack computer. It connects three physical devices — RAM, Screen, and Keyboard — into one unified interface that the CPU can use.<br>

At first, NOT creates the opposite signals N14 = NOT address[14] and N13 = NOT address[13] that will be used to detect whether we're in the RAM, Screen, or Keyboard range.<br>

Second, it goes to load signals and the components.From components, it result of outM from RAM16K, outS from Screen, and outK from Keyboard.<br>

Last, these multiplexers decide which component’s output should appear on the overall out bus.
1. Mux16(a=outS, b=outK, sel=address[13])
   - If address[13] = 0, output from Screen.
   - If address[13] = 1, output from Keyboard, result is outSK.

2. Mux16(a=outM, b=outSK, sel=address[14])
   - If address[14] = 0, output from RAM16K.
   - If address[14] = 1, output from either Screen or Keyboard (based on previous Mux), final result = out.

For Computer Project, the computer chip ties everything togeter, contain of CPU, Memory (RAM + Screen + Keyboard), and ROM. The execution will start like this:
1. CPU fetches instruction from ROM[PC].
2. CPU executes:
    - If A-instruction = updates A.
    - If C-instruction = performs computation, writes to RAM, or jumps.
3. Memory responds to load or address signals.
4. PC updates (either +1 or jump).
5. Repeat until reset or halt.