# SAGA16 a 16-bits CPU using Logisim

First, this project is part of a curricular component of my course. The project is for learning purposes and doesn't challenge itself too much to do anything other than what is written here.

For future purposes, I intend to create an assembler code interpreter in python that will transform instructions into hexadecimal blocks.

# Download Logisim

## Simulator used to build the CPU.

[Loagisim Evolution](https://github.com/logisim-evolution/logisim-evolution)

# Video of the process

[Projetei a minha propria CPU no Logisim]()

## ARCHITECTURE OF THE SAGA16 CPU
The SAGA CPU consists of the following functional
units:

- Register array and address logic.

- Arithmetic and logic unit (ALU).

- Instruction register and control section
### Registers:

The register section consists of a static RAM array
organized into six 16-bit registers:

- Program counter (PC)

- Stack pointer (SP)

- Six 8-bit general purpose registers arranged in pairs,
referred to as B,C; D,E; and H,L

- A temporary register pair called W,Z, who loads the address to the SP

The program counter maintains the memory address of the current program instruction and is incremented automatically during every instruction fetch. The stack pointer maintains the address of the next available stack location in memory. The stack pointer can be initialized to use any portion of read-write memory as a stack.

## INSTRUCTION SET

### Summary of processor instructions
Notes: This CPU allows the creation of chars and strings, which are only for visualization and determined via code.

|All registers|Register pairs| |
|-------|-------|------|
|Teemporary registers|110 - W|111 - Z|
|Main registers|000 - B|001 - C|
|Main registers|010 - D|011 - E|
|Main registers|100 - H|101 - L|
|Stack pointer registers|W&Z||
|16-bit direct storage|**Null** - F|**Null** - G|

|Meaning|Acronym|Description|
|-------|-------|-----------|
|From   |SSS|3 Bits responsible for selecting where some information will come from|
|To     |DDD    |3 Bits responsible for selecting the destination of some data|
|Memory |M|Ram memory |
|Register|r|Any register|
|Register Pair|r&r|Matches any of the 4 pairs of registers|
|Accumulator|A|Almost all manipulated data in ALU will be stored in this register and replaced by another one, as it is a temporary register|
|16 bits|WORD|All instruction with "WORD" works with 16 bits data, that means it will do a direct operation with 16 bits using whatever is in the F and G registers|
|8 bits|BYTE|All instruction with "BYTE" works with 8 bits data, that means it will do a direct operation with 8 bits|


| Mnemonic | Description |HexCode| D <sub>7</sub> | D <sub>6</sub> | D <sub>5</sub> | D <sub>4</sub> | D <sub>3</sub> | D <sub>2</sub> | D <sub>1</sub> | D <sub>0</sub> |
|----------|-------------|----|---|---|---|---|---|---|---|---|
|NOP| No operation |00| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|MOV **<sub>r1, r2</sub>** | <sub>r2</sub> is copied to <sub>r1</sub> |--| 0 | 1 | D | D | D | S | S | S |
|MOV M, **<sub>r</sub>**| The value of <sub>r</sub> is written to M (memory) |7-| 0 | 1 | 1 | 1 | 0 | S | S | S |
|MOV **<sub>r</sub>**, M | The value read from M is copied to <sub>r</sub> |--| 0 | 1 | D | D | D | 1 | 1 | 0 |
|MVI **<sub>r</sub>** | The value read from r is copied to Accumulator |7-| 0 | 1 | 1 | 1 | 1 | S | S | S |
|MVI M | The value read from Memory is copied to Accumulator |7e| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
|MOV **<sub>r</sub>**, A| The value of Accumulator is copied to <sub>r</sub> |0-| 0 | 0 | 0 | 0 | 1 | D | D | D |
|MOV **M**, A| The value of **M** is copied to Accumulator |0e| 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 |
|LXI **B**| Load imediate from memory (only 1 byte at a time) register pair **B & C** |06| 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
|LXI **D**| Load imediate from memory (only 1 byte at a time) register pair **D & E** |16| 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 |
|LXI **H**| Load imediate from memory (only 1 byte at a time) register pair **H & L** |26| 0 | 0 | 1 | 0 | 0 | 1 | 1 | 0 |
|LXI **W** | Load imediate from memory (only 1 byte at a time) temporary register pair **W & A** |36| 0 | 0 | 1 | 1 | 0 | 1 | 1 | 0 |
|LOAD PAIR at F| Load data from register pair temporary to F register |18+| 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
|LOAD PAIR at G| Load data from register pair temporary to G register |1d+| 0 | 0 | 0 | 1 | 1 | 1 | 0 | 1 |
|ADD BYTE r| Add ACC plus register |8-| 1 | 0 | 0 | 0 | 0 | S | S | S |
|MULT BYTE r| Multiplies ACC with register |8-| 1 | 0 | 0 | 0 | 1 | S | S | S |
|OPA BYTE| Returns A ignoring B. It can be used to generate flags, without performing an arithmetic operation |9-| 1 | 0 | 0 | 1 | 0 | S | S | S |
|DIV BYTE r| Divide ACC with register|9-| 1 | 0 | 0 | 1 | 1 | S | S | S |
|ANA BYTE r| And operation ACC with register |a-| 1 | 0 | 1 | 0 | 0 | S | S | S |
|XRA BYTE r| Xor operation ACC with register |a-| 1 | 0 | 1 | 0 | 1 | S | S | S |
|ORA BYTE r| Or operation ACC with register |b-| 1 | 0 | 1 | 1 | 0 | S | S | S |
|MOD BYTE r| Give the remainder of dividing ACC with register |b-| 1 | 0 | 1 | 1 | 1 | S | S | S |
|ADD WORD| Add F <sub>(16)</sub> plus G <sub>(16)</sub> |28+| 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
|MULT WORD| Multiplies F <sub>(16)</sub> by G <sub>(16)</sub> |29| 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
|OPA WORD| Returns A ignoring B. It can be used to generate flags, without performing an arithmetic operation |2a| 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
|DIV WORD| Divide F <sub>(16)</sub> by G <sub>(16)</sub> |2b| 0 | 0 | 1 | 0 | 1 | 0 | 1 | 1 |
|ANA WORD| And operation with F <sub>(16)</sub> and G <sub>(16)</sub> |2c| 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 |
|XRA WORD| Xor operation with F <sub>(16)</sub> and G <sub>(16)</sub> |2d| 0 | 0 | 1 | 0 | 1 | 1 | 0 | 1 |
|ORA WORD| Or operation with F <sub>(16)</sub> and G <sub>(16)</sub> |2e| 0 | 0 | 1 | 0 | 1 | 1 | 1 | 0 |
|MOD WORD| Give the remainder of dividing F <sub>(16)</sub> and G <sub>(16)</sub>|2f| 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |
|STW F| Store 16 bits F register direct on memory |3e| 0 | 0 | 1 | 1 | 1 | 1 | 1 | 0 |
|JMP | Jump unconditional |c3| 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
|JZ | Jump on zero |c0| 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
|JNZ | Jump on no zero |c8| 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
|JM | Jump on minus |d0| 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
|JP | Jump on positive |d8| 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
|JG | Jump on grater, if A > B |e0| 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
|JL | Jump on less, if A < B |e8| 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
|JC | Jump on carry |f0| 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
|JNC | Jump on not carry |f8| 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
|LDW var | Load value from memory block to HL register pair |c1| 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
|OUT | Print number or char elements |02+| 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

# How does the instruction work?

In the instruction set above, some instructions have a hexadecimal number with a + sign.

I'll explain so you don't have any doubts.

Instructions like **OUT**, I thought I could write them like this:

- out -%d to print signed numbers
- out %d to print unsigned numbers
- out %s string print characters

In hexadecimal the instructions would be: 

- 02 + 13 => 0213 out -%d
- 02 + 03 => 0203 out %d
- 02 + 00 => 0200 out %s

**Obs: Remember that I'm not adding, just concatenating**

That is, 02 is the output instruction, and the rest are instruction complements.

Let's see another example that happens:
**Load lsb pair at f**
this instruction loads in register F, a value, and who says which pair to load is the complement of the instruction, so:
**Load lsb pair at f**, can be written in the following ways.
- 1800 -> Loads the pair BC.
- 1801 -> Loads the DE pair.
- 1802 -> Loads of HL pair.
- 1803 -> Loads of the WZ pair.

**Load lsb pair at G**, can be written in the following ways.
- 1d00 -> Loads the BC pair.
- 1d01 -> Loads the DE pair.
- 1d02 -> Loads the HL pair.
- 1d03 -> Loads the WZ pair.

**Add** Instruction:
- 2800 -> Addition x+y
- 2801 -> Addition x+(-y)

# images

## How is the cpu seen from a further angle?

You can see that the cpu communicates with the ram memory and with a terminal, it doesn't have an input system that is present in that circuit, not yet.

![CPU Design](./images/cpu_Design.png)

Logisim allows you to customize the appearance of your integrated circuits. This is the final appearance of my cpu in the simulator.

![CPU Appearence](./images/cpu_Appearance.png)

## Registers of SAGA16

This is the cpu main registers scheme.

![Registers](./images/registers.png)

## How "strings" works?

Word storage consists of two characters in 1 block of memory, if there is a row of blocks containing characters, we will have a string, and who will mark the end of this string is 0x0000.

![word storage](./images/strings.png)

# Char table



|ASCII Character|Hexadecimal|Binary|
|-----------|--|------------|
|NUL	    |00|	00000000|
|SOH	    |01|	00000001|
|STX	    |02|	00000010|
|ETX	    |03|	00000011|
|EOT	    |04|	00000100|
|ENQ	    |05|	00000101|
|ACK	    |06|	00000110|
|BEL	    |07|	00000111|
|BS	        |08|	00001000|
|HT	        |09|	00001001|
|LF	        |0A|	00001010|
|VT	        |0B|	00001011|
|FF	        |0C|	00001100|
|CR	        |0D|	00001101|
|SO	        |0E|	00001110|
|SI	        |0F|	00001111|
|DLE	    |10|	00010000|
|DC1	    |11|	00010001|
|DC2	    |12|	00010010|
|DC3	    |13|	00010011|
|DC4	    |14|	00010100|
|NAK	    |15|	00010101|
|SYN	    |16|	00010110|
|ETB	    |17|	00010111|
|CAN	    |18|	00011000|
|EM	    |19|	00011001|
|SUB	|1A|	00011010|
|ESC	|1B|	00011011|
|FS	    |1C|	00011100|
|GS	    |1D|	00011101|
|RS	    |1E|	00011110|
|US	    |1F|	00011111|
|Space	|20|	00100000|
|!	    |21|	00100001|
|"	    |22|	00100010|
|#	    |23|	00100011|
|$	    |24|	00100100|
|%	    |25|	00100101|
|&	    |26|	00100110|
|'	    |27|	00100111|
|(	    |28|	00101000|
|)	    |29|	00101001|
|*	    |2A|	00101010|
|+	    |2B|	00101011|
|,	    |2C|	00101100|
|-	    |2D|	00101101|
|.	    |2E|	00101110|
|/	    |2F|	00101111|
|0	    |30|	00110000|
|1	    |31|	00110001|
|2	    |32|	00110010|
|3	    |33|	00110011|
|4	    |34|	00110100|
|5	    |35|	00110101|
|6	    |36|	00110110|
|7	    |37|	00110111|
|8	    |38|	00111000|
|9	    |39|	00111001|
|:	    |3A|	00111010|
|;	    |3B|	00111011|
|<	    |3C|	00111100|
|=	    |3D|	00111101|
|>	    |3E|	00111110|
|?	    |3F|	00111111|
|@	    |40|	01000000|
|A	    |41|	01000001|
|B	    |42|	01000010|
|C	    |43|	01000011|
|D	    |44|	01000100|
|E	    |45|	01000101|
|F	    |46|	01000110|
|G	    |47|	01000111|
|H	    |48|	01001000|
|I	    |49|	01001001|
|J	    |4A|	01001010|
|K	    |4B|	01001011|
|L	    |4C|	01001100|
|M	    |4D|	01001101|
|N	    |4E|	01001110|
|O	    |4F|	01001111|
|P	    |50|	01010000|
|Q	    |51|	01010001|
|R	    |52|	01010010|
|S	    |53|	01010011|
|T	    |54|	01010100|
|U	    |55|	01010101|
|V	    |56|	01010110|
|W	    |57|	01010111|
|X	    |58|	01011000|
|Y	    |59|	01011001|
|Z	    |5A|	01011010|
|[	    |5B|	01011011|
|\	    |5C|	01011100|
|]	    |5D|	01011101|
|^	    |5E|	01011110|
|_	    |5F|	01011111|
|`	    |60|	01100000|
|a	    |61|	01100001|
|b	    |62|	01100010|
|c	    |63|	01100011|
|d	    |64|	01100100|
|e	    |65|	01100101|
|f	    |66|	01100110|
|g	    |67|	01100111|
|h	    |68|	01101000|
|i	    |69|	01101001|
|j	    |6A|	01101010|
|k	    |6B|	01101011|
|l	    |6C|	01101100|
|m	    |6D|	01101101|
|n	    |6E|	01101110|
|o	    |6F|	01101111|
|p	    |70|	01110000|
|q	    |71|	01110001|
|r	    |72|	01110010|
|s	    |73|	01110011|
|t	    |74|	01110100|
|u	    |75|	01110101|
|v	    |76|	01110110|
|w	    |77|	01110111|
|x	    |78|	01111000|
|y	    |79|	01111001|
|z	    |7A|	01111010|
|{	    |7B|	01111011|
|Barra	|7C|	01111100|
|}	    |7D|	01111101|
|~	    |7E|	01111110|
|DEL	|7F|	01111111|