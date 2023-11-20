"""
This is a small risc machine that supports multiple instruction sets: NOP, HALT, CMP, JMP, LOAD, STORE, ADD, SUB
The current implementation does not support encoding / decoding instructionself.
"""

import numpy as np  #not necessarily needed, but it will make things easier
import fnmatch
import time

class machine:
    def __init__(self, mem_size):
        """
        Create a CPU state with memory = mem_size, and initialize all registerself.
        """
        
        # create a memory block of mem_size of datatype uint8 and fill it with zeroself.
        self.memory         = np.zeros(mem_size, dtype=np.uint8)
        self.memory_size    = mem_size

        # set registers to 0 ( 32 registers of type: int32)
        # x0        zero        hard-wired zero
        # x1        ra          return address
        # x2        sp          stack pointer
        # x3        gp          global pointer
        # x4        tp          thread pointer
        # x5        temp        temp/alternate link register
        # x6-7      temp
        # x8        s0          saved register / frame pointer
        # x9        s1          saved register
        # x10-11    a0..a1      function args/return values
        # x12-17    a2..a7      function args
        # x18-27    s2..s11     saved registers
        # x28-31    t3..t6      temp
        self.registers      = np.zeros(32, dtype=np.int32)

        # set program counter to 0
        self.pc             = np.zeros(1, dtype=np.int32)

        #set dictionary with supported instructions
        self.instruciton_dictionary = {'NOP': self.NOP, 'HALT': self.HALT, 'CMP': self.CMP, 'JMP': self.JMP, 'LW': self.LW, 'SW': self.SW, 'ADD': self.ADD, 'ADDi': self.ADDi, 'SUB': self.SUB, 'XOR': self.XOR, 'AND': self.AND, 'OR': self.OR, 'BEQ': self.BEQ, 'BNE': self.BNE, 'Li': self.Li, 'BGE': self.BGE, 'BLT': self.BLT, 'JAL': self.JAL, 'MUL': self.MUL, 'Li': self.Li, 'JALR': self.JALR}

        #set flag for comparisons to false
        self.flag           = False

        #create label dictionary empty till a program is loaded
        self.label_dictionary = {}

        #create instruction encoding for assembly
        self.decoder_dictionary = {
            '0000000_?????_000_0110011': ['R',  'ADD'      ],
            '0100000_?????_000_0110011': ['R',  'SUB'      ],
            '0000000_?????_100_0110011': ['R',  'XOR'      ],
            '0000000_?????_110_0110011': ['R',  'OR'       ],
            '0000000_?????_111_0110011': ['R',  'AND'      ],
            '0000001_?????_000_0110011': ['R',  'MUL'      ],
            '???????_?????_010_0100011': ['S',  'SW'       ],
            '???????_?????_000_0010011': ['I',  'ADDi'     ],
            '???????_?????_010_0000011': ['I',  'LW'       ],
            '???????_?????_000_1100011': ['B',  'BEQ'      ],
            '???????_?????_001_1100011': ['B',  'BNE'      ],
            '???????_?????_101_1100011': ['B',  'BGE'      ],
            '???????_?????_100_1100011': ['B',  'BLT'      ],
            '???????_?????_???_1101111': ['J',  'JAL'      ],
            '???????_?????_000_1100111': ['I',  'JALR'     ]
        }

        # generate assembler dictionary by inverting the decoder dictionary
        # so that key = 'instruction' and value = ['opcode-bits', 'format-type']
        self.asm_dict = {self.decoder_dictionary[k][1]: [k, self.decoder_dictionary[k][0]] for k in self.decoder_dictionary}

        #------------------------------------------------------------------------------------------------------------------------------------------------
        # Register Names ( RiscV )
        #------------------------------------------------------------------------------------------------------------------------------------------------
        self.zero = 0
        self.ra = 1
        self.sp = 2
        self.gp = 3
        self.tp = 4
        self.t0 = 5
        self.t1 = 6
        self.t2 = 7
        self.s0 = 8
        self.s1 = 9
        self.a0 = 10
        self.a1 = 11
        self.a2 = 12
        self.a3 = 13
        self.a4 = 14
        self.a5 = 15
        self.a6 = 16
        self.a7 = 17
        self.s2 = 18
        self.s3 = 19
        self.s4 = 20
        self.s5 = 21
        self.s6 = 22
        self.s7 = 23
        self.s8 = 24
        self.s9 = 25
        self.s10 = 26
        self.s11 = 27
        self.t3 = 28
        self.t4 = 29
        self.t5 = 30
        self.t6 = 31

        #------------------------------------------------------------------------------------------------------------------------------------------------
        # Program execution metric
        #------------------------------------------------------------------------------------------------------------------------------------------------

        self.debug = False
        self.memory_used = 0
        self.total_number_of_instructions = 0
        self.number_of_branches = 0
        self.number_of_arithmatic = 0
        self.number_of_load_store = 0


    #------------------------------------------------------------------------------------------------------------------------------------------------

    # Program Counter
    def incrementPC(self, inc=4):
        """
        Increments program counter by 4 to point to the next instruction
        Make sure that register0 is always zero
        """
        self.registers[0] = 0
        self.pc += inc
    
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------

    def NOP(self):
        """
        No operation instruction, does nothing / should consume 1 clock cyle
        """
        self.ADDi(self.registers[0], self.registers[0], 0)
        self.incrementPC()
    
    def HALT(self):
        """
        This instruction halts the CPU and stops further instructions until the next external interrupt is fired.
        External interrupts are not supported yet. 
        """
        while True:
            #Do Nothing
            pass

            #TODO: future improvement
            #if(EXTERNAL_INTERRUPT):
            #   break

    def JMP(self, rd, offset):
        """ 
        save next instruction offset in rd
        increment program counter by offset
        """
        self.registers[rd] = self.pc + 4
        self.incrementPC(offset)

    def JAL(self, rd, offset):
        """
        Calls JMP which saves the next instruction in rd and increments program counter by offset
        """
        self.JMP(rd, offset)

    def JALR(self, rd, rs1, imm): 
        temp = self.pc + 4
        self.pc = (self.registers[rs1] + imm) & ~1
        self.registers[rd] = temp
        self.registers[0] = 0

    def CMP(self, rs1, rs2):
        if self.registers[rs1] == self.registers[rs2]:
            self.flag = True;
        else:
            self.flag = False;
        
        self.incrementPC()

    def LW(self, rd, offset, rs1):
        """
        Loads a word (32bits) from a memory offset into a general purpose register
        """
        self.registers[rd] = ((self.memory[self.registers[rs1] + offset + 3] << 24) + (self.memory[self.registers[rs1] + offset + 2] << 16) + (self.memory[self.registers[rs1] + offset + 1] << 8) + (self.memory[self.registers[rs1] + offset]))
        self.incrementPC()

    def SW(self, rs2, offset, rs1):
        """
        Stores a word (32bits) into memory
        """
        self.memory[self.registers[rs1] + offset]       = self.registers[rs2]
        self.memory[self.registers[rs1] + offset + 1]   = self.registers[rs2] >> 8
        self.memory[self.registers[rs1] + offset + 2]   = self.registers[rs2] >> 16
        self.memory[self.registers[rs1] + offset + 3]   = self.registers[rs2] >> 24
        self.incrementPC()

    def Li(self, rd, imm):
        """
        Load immidiate value into register
        """
        self.ADDi(self.registers[rd], self.registers[0], imm)   #ADDi will increment pc
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Arithmetic Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------

    def ADD(self, rd, rs1, rs2):
        """
        Add rs1 and rs2 and store the result in rd
        """
        self.registers[rd] = self.registers[rs1] + self.registers[rs2]
        self.incrementPC()

    def SUB(self, rd, rs1, rs2):
        """
        Subtract rs2 from rs1 and store the result in rd
        """
        self.registers[rd] = self.registers[rs1] - self.registers[rs2]
        self.incrementPC()

    def ADDi(self, rd, rs1, val):
        """
        Add an immediate value (val) to rs1 and store the result in rd
        """
        self.registers[rd] = self.registers[rs1] + val;
        self.incrementPC()
    
    def MUL(self, rd, rs1, rs2):
        """"
        Performs multiplication between rs1 and rs2 and stores the value in rd
        """
        self.registers[rd] = self.registers[rs1] * self.registers[rs2]
        self.incrementPC()

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Logical Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------

    def XOR(self, rd, rs1, rs2):
        """
        XOR rs1 and rs2 and store the value in rd
        """
        self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]
        self.incrementPC()

    def OR(self, rd, rs1, rs2):
        """
        OR rs1 and rs2 and store value in rd
        """
        self.registers[rd] = self.registers[rs1] | self.registers[rs2]
        self.incrementPC()

    def AND(self, rd, rs1, rs2):
        """
        AND rs1 and rs2 and store value in rd
        """
        self.registers[rd] = self.registers[rs1] & self.registers[rs2]
        self.incrementPC()

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Branch Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------

    def BEQ(self, rs1, rs2, val):
        """
        branch if rs1 == rs2, otherwise continue
        """
        if(self.registers[rs1] == self.registers[rs2]):
            self.incrementPC(val)
        else:
            self.incrementPC()

    def BNE(self, rs1, rs2, val):
        """
        branch if rs1 != rs2, otherwise continue
        """
        if(self.registers[rs1] != self.registers[rs2]):
            self.incrementPC(val)
        else:
            self.incrementPC()

    def BGE(self, rs, rt, offset):
        """
        Branch if >=
        """
        if(self.registers[rs] >= self.registers[rt]):
            self.incrementPC(offset)
        else:
            self.incrementPC()
    
    def BLT(self, rs1, rs2, offset):
        """
        Branch if <
        """
        if(self.registers[rs1] < self.registers[rs2]):
            self.incrementPC(offset)
        else:
            self.incrementPC()
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Program Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------

    def addLabel(self, label):
        """
        add new label to label dictionary with current pc value
        """
        self.label_dictionary.update({label: self.pc})

    def getLabel(self, label):
        """
        lookup label in label dictionary
        """
        if(isinstance(label, str)):
            label = self.label_dictionary[label]
        return label
    
    # function to return key for any value
    def get_key(self, val):
   
        for key, value in self.instruciton_dict_encoding.items():
            if val == value:
                return key
 
        return 0
        
    def excAssembly(self, instruction, arg1, arg2, arg3=0, arg4 =0):
        """
        captures the assembly instructions and store it into memory for future operation
        """

        instr = self.instruciton_dictionary.get(instruction)
        rd = arg1
        rs1 = arg2
        rs2 = arg3
        rs3 = arg4
        
        if (instr):
            if      instr == self.ADD       : self.ADD(arg1, arg2, arg3)
            elif    instr == self.SUB       : self.SUB(arg1, arg2, arg3)
            elif    instr == self.NOP       : self.NOP()
            elif    instr == self.ADDi      : self.ADDi(arg1, arg2, arg3)
            elif    instr == self.BNE       : self.BNE(arg1, arg2, arg3)
            elif    instr == self.BEQ       : self.BEQ(arg1, arg2, arg3)
            elif    instr == self.HALT      : self.HALT()
            elif    instr == self.AND       : self.AND(arg1, arg2, arg3)
            elif    instr == self.OR        : self.OR(arg1, arg2, arg3)
            elif    instr == self.XOR       : self.XOR(arg1, arg2, arg3)
            elif    instr == self.SW        : self.SW(arg1, arg2, arg3)
            elif    instr == self.LW        : self.LW(arg1, arg2, arg3)
            elif    instr == self.CMP       : self.CMP(arg1, arg2)
            elif    instr == self.JMP       : self.JMP(arg1, arg2)
            elif    instr == self.BGE       : self.BGE(arg1, arg2, arg3)
            elif    instr == self.BLT       : self.BLT(arg1, arg2, arg3)
            elif    instr == self.JAL       : self.JAL(arg1, arg2)
            elif    instr == self.MUL       : self.MUL(arg1, arg2, arg3)
            elif    instr == self.JALR      : self.JALR(arg1, arg2, arg3)
            else                            : self.NOP()

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Helper functions
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def field(self, bits, hi, lo):
        """
        extract bitfields from a bit-array using Verilog bit-indexing order,
        so [0] is the right-most bit (which is opposite order than bitstring),
        and [1:0] are the 2 least significant bits, etc.
        """
        return bits[len(bits) - 1 - hi : len(bits) - lo]
    
    def write_i32(self, x, addr):
        """
        write 32-bit int to memory (takes 4 byte-addresses)
        """
        self.memory[addr]     = (x     )  & 0xFF
        self.memory[addr + 1] = (x >> 8)  & 0xFF
        self.memory[addr + 2] = (x >> 16) & 0xFF
        self.memory[addr + 3] = (x >> 24) & 0xFF

    def bits_2_uint(self, bits):
        """
        convert bit-string to unsigned int
        """
        return int(bits, 2)
    
    def bits2i(self, bits):
        """
        convert bit-string to signed int (subtract constant if msb is 1)
        """
        return self.bits_2_uint(bits) - (1 << len(bits) if bits[0] == '1' else 0)
    
    def read_i32(self, addr):
        """"read 32-bit int from memory"""
        ret = np.int8(self.memory[addr + 3]) << 3*8
        for i in range(3): ret += self.memory[addr + i] << i*8
        return ret

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Encoding functions
    #------------------------------------------------------------------------------------------------------------------------------------------------

    # Volume I: RISC-V User-Level ISA V2.2
    # 31 27 | 26 25     | 24 20 | 19 15 | 14 12 | 11 7              | 6  0
    #    funct7         |  rs2  |  rs1  | funct3| rd                |opcode          R-type
    # rs3 | funct2      |  rs2  |  rs1  | funct3| rd                |opcode          R4-type
    # imm[11:0]         |       |  rs1  | funct3| rd                |opcode          I-type
    # imm[11:5]         | rs2   |  rs1  | funct3| imm[4:0]          |opcode          S-type
    # imm[12]|imm[10:5] | rs2   |  rs1  | funct3| imm[4:1] imm[11]  |opcode          B-type
    # imm[20]|imm[10:1] imm[11] | imm[19:12]    | rd                |opcode          J-type
    def storeAssembly(self, instruction, arg1, arg2, arg3=0, arg4 =0):
        """
        stores instruction and arguments into memory after encoding using RiscV user level ISA.
        Using: Volume I: RISC-V User-Level ISA V2.2
        """
        instr = self.instruciton_dictionary.get(instruction)
        if(instr):
            # Use CS 61C Reference Card
            [opcode_bits, typ] = self.asm_dict[instruction]
            
            funct7 = opcode_bits[0:7]
            funct3 = opcode_bits[14:17]
            opcode = opcode_bits[18:25]
     
            # swap arg2 and arg3 if instruction is LW 
            if instruction == 'LW':
                temp2 = arg2
                temp3 = arg3

                arg2 = temp3
                arg3 = temp2
            
            if typ == 'B':
                arg3 = self.getLabel(arg3)
                arg3 -= self.pc
    
            if instruction == 'JAL':
                arg2 = self.getLabel(arg2)
                arg2 -= self.pc

            # TODO: loop throughout the code, find labels and store their offset first, then loop and encode+store into memory
            #       this will allow the code to be written in a non-linear matter

            rd    = np.binary_repr(arg1, 5)
            rs1   = np.binary_repr(arg2, 5)
            rs2   = np.binary_repr(arg3, 5)
            imm_i = np.binary_repr(arg3, 12)
            imm_s = np.binary_repr(arg2, 12)
            imm_j = np.binary_repr(arg2, 21)
            imm_b = np.binary_repr(arg3, 13)

            if   typ == 'R' : bits = funct7 + rs2  + rs1 + funct3 + rd + opcode
            elif typ == 'I' : bits = imm_i + rs1 + funct3 + rd + opcode 
            elif typ == 'S' : bits = self.field(imm_s,11,5) + rd + rs2 + funct3 + \
                                     self.field(imm_s,4,0) + opcode
            
            elif typ == 'J' : bits = self.field(imm_j,20,20) + self.field(imm_j,10,1) + \
                             self.field(imm_j,11,11) + self.field(imm_j,19,12) + rd + opcode
            
            elif typ == 'B' : bits = self.field(imm_b,12,12) + self.field(imm_b,10,5) + rs1 + rd + \
                        funct3 + self.field(imm_b,4,1)   + self.field(imm_b,11,11) + opcode
                
            # write instruction into memory at address 'self.pc'
            self.write_i32(self.bits_2_uint(bits), self.pc)
            self.incrementPC()

            if self.debug == True:
                self.memory_used += 1
        else:
            print("ERROR: instruction not supported")
            if self.debug == True:
                self.dump()
            self.HALT()
        

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Decoding functions
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def decode(self, bits):
        """decode instruction based on Volume I: RISC-V User-Level ISA V2.2"""
        opcode = self.field(bits,  6,  0)
        funct3 = self.field(bits, 14, 12)
        rs2c   = self.field(bits, 24, 20)  # rs2 code
        funct7 = self.field(bits, 31, 25)

        rd     = self.bits_2_uint(self.field(bits, 11,  7))
        rs1    = self.bits_2_uint(self.field(bits, 19, 15))
        rs2    = self.bits_2_uint(self.field(bits, 24, 20))

        imm_i  = self.bits2i(self.field(bits, 31, 20))                                      # I-type
        
        imm_s  = self.bits2i(self.field(bits, 31, 25) + self.field(bits, 11,  7))           # S-type
        imm_b  = self.bits2i(self.field(bits, 31, 31) + self.field(bits,  7,  7) +
                        self.field(bits, 30, 25) + self.field(bits, 11,  8) + '0')          # B-type
        
        imm_j  = self.bits2i(self.field(bits, 31, 31) + self.field(bits, 19, 12) +
                        self.field(bits, 20, 20) + self.field(bits, 30, 21) + '0')          # J-type
        opcode_bits = funct7 + '_' + rs2c + '_' + funct3 + '_' + opcode

        # decode instruction (opcode_bits -> inst)
        inst = 0
        for k in self.decoder_dictionary:
            if fnmatch.fnmatch(opcode_bits, k):
                inst = self.decoder_dictionary[k][1]
                break  # to speed up run-time
        if inst == 0:
            
            print('ERROR: this instruction is not supported: ' + bits)
            if self.debug == True:
                self.dump()
            self.HALT()

        if inst   == 'JAL'      : self.JAL      (rd,  imm_j)
        elif inst == 'JALR'     : self.JALR     (rd,  rs1,   imm_i)
        elif inst == 'BEQ'      : self.BEQ      (rs1, rs2,   imm_b)
        elif inst == 'BNE'      : self.BNE      (rs1, rs2,   imm_b)
        elif inst == 'BLT'      : self.BLT      (rs1, rs2,   imm_b)
        elif inst == 'SW'       : self.SW       (rs2, imm_s, rs1)
        elif inst == 'ADDi'     : self.ADDi     (rd,  rs1,   imm_i)
        elif inst == 'ADD'      : self.ADD      (rd,  rs1,   rs2)
        elif inst == 'SUB'      : self.SUB      (rd,  rs1,   rs2)
        elif inst == 'XOR'      : self.XOR      (rd,  rs1,   rs2)
        elif inst == 'OR'       : self.OR       (rd,  rs1,   rs2)
        elif inst == 'AND'      : self.AND      (rd,  rs1,   rs2)
        elif inst == 'MUL'      : self.MUL      (rd,  rs1,   rs2)
        elif inst == 'LW'       : self.LW       (rd,  imm_i, rs1)
        
        #print(inst)
        if self.debug == True:
            self.total_number_of_instructions += 1
            if inst == 'LW':
                self.number_of_load_store += 1
            elif inst in ['ADD', 'ADDi', 'MUL', 'SUB']:
                self.number_of_arithmatic += 1
            elif inst in ['BLT', 'BNE', 'BEQ']:
                self.number_of_branches += 1

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # excute from memory functions
    #------------------------------------------------------------------------------------------------------------------------------------------------

    def execute(self, start, end=None, instructionCount=0):
        """
        Executes code from start label to end label or for instructionCount number of instructions
        """
        if self.debug == True:
            self.excution_time = time.perf_counter()

        self.pc = self.getLabel('start')
        if end is None:
            for i in range(instructionCount):
                inst = self.read_i32(self.pc)  # fetch instruction from memory
                self.decode(np.binary_repr(np.uint32(inst), 32))
        else:  # this is for the case where argument 'end' is used
            while self.pc != self.getLabel(end):
                inst = self.read_i32(self.pc)  # fetch instruction from memory
                self.decode(np.binary_repr(np.uint32(inst), 32))

        if self.debug == True:
            self.excution_time = time.perf_counter() - self.excution_time
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Reset Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def reset_machine(self):
        self.registers  = np.zeros(32, dtype=np.int32)
        self.pc         = 0
        self.flag       = False

        self.debug = False
        self.memory_used = 0
        self.total_number_of_instructions = 0
        self.number_of_branches = 0
        self.number_of_arithmatic = 0
        self.number_of_load_store = 0

    
    def clear_memory(self):
        self.memory     = np.zeros(self.memory_size, dtype=np.uint8)

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Dump Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------
    
    def dump(self):
        print("Registers:")
        print("---------")
        for i in range(32):
            print(self.registers[i])
        print("---------")
        print("")
        print("Program Counter: ")
        print(self.pc)
        print("---------")
        print("")
        