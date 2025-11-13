// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
(LOOP)
    @KBD
    D=M
    @BLACK
    D;JNE        // if key pressed → go fill black
    @WHITE
    0;JMP        // else → go fill white

(BLACK)
    @color
    M=-1         // black = all 1s
    @DRAW
    0;JMP

(WHITE)
    @color
    M=0          // white = all 0s
    @DRAW
    0;JMP

(DRAW)
    @SCREEN
    D=A
    @addr
    M=D          // addr = SCREEN base

(LOOPDRAW)
    @color
    D=M
    @addr
    A=M
    M=D          // set pixel = color
    @addr
    M=M+1        // addr++
    @KBD
    D=A
    @addr
    D=M-D
    @LOOPDRAW
    D;JLT        // loop until addr reaches KBD

    @LOOP
    0;JMP        // repeat forever