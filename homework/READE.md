# NOTES

## [Homework 1]()

Project 1 asked to build the basic logic gates (NOT, AND, OR, XOR, MUX, DMUX, etc.) using only NAND gates. This project split for some of part.<br>

1. Logic gates output of NOT = NOT A.<br>
2. Logic gates output of AND = A and B.<br>
3. Logic gates law of OR = a OR b = NOT(NOTa AND NOTb).<br>
4. Logic gates law of XOR = (a AND NOT b) OR (NOT a AND b).<br>
5. Logic gates of Mux (Multiplexer) = choose between a and b based on selector sel, where out = (a AND NOT sel) OR (b AND sel).<br>
6. Logic gates of DMux (Demultiplexer) = send input in to one of two outputs depending on sel.<br>

For the (NOT16, AND16, OR16, XOR16, MUX16, DMUX16), the concept itself still same but instead of single bits, this part using of 16-bit buses.<br>

For the Mux4Way16 and Mux8Way16, use multiple Mux16 chips to choose among 4 or 8 16-bit inputs. Last for DMux4Way, DMux8Way: expand DMux logic to 4 or 8 outputs using two or three levels.<br>

## [Homework 2]()