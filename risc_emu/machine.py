"""
This is a small risc machine that supports multiple instruction sets: NOP, HALT, CMP, JMP, LOAD, STORE, ADD, SUB
The current implementation does not support encoding / decoding instructions.
"""

import numpy as np  #not necessarily needed, but it will make things easier

class machine:
    def __init__(self, mem_size):
        """
        Create a CPU state with memory = mem_size, and initialize all registers.
        """
        
        # create a memory block of mem_size of datatype uint8 and fill it with zeros.
        self.memory = np.zeros(mem_size, dtype=np.unit8)

        # set registers to 0 ( 32 registers of type: int32)
        self.registers      = np.zeros(32, dtype=np.int32)

        # set program counter to 0
        self.pc             = np.zeros(1, dtype=np.int32)

        #set dictionary with supported instructions
        self.instruciton_dictionary = {}

        #set flag for comparisons to false
        self.flag           = False



    # Program Counter
    def incrementPC(self, inc=4):
        """
        Increments program counter by 4 to point to the next instruction
        Make sure that register0 is always zero
        """
        self.registers[0] = 0
        self.pc += inc
    
    # Instructions
    def NOP(self):
        """
        No operation instruction, does nothing
        """
    
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

    def JMP(self, rd, offset):
        """ 
        save next instruction offset in rd
        increment program counter by offset
        """
        self.registers[rd] = self.pc + 4
        self.incrementPC(offset)

    def CMP(self, rs1, rs2):
        if self.registers[rs1] == self.registers[rs2]:
            self.flag = True;
        else:
            self.flag = False;

    def LW(self, rd, offset, rs1):
        """
        Loads a word (32bits) from a memory offset into a general purpose register
        """
        self.registers[rd] = ((self.memory[self.registers[rs1] + offset + 3] << 24) + (self.memory[self.registers[rs1] + offset + 2] << 16) + (self.memory[self.registers[rs1] + offset + 1] << 8) + (self.memory[self.registers[rs1] + offset]))
        self.incrementPC()

    def SW(self, rs1, offset, rs2):
        """
        Stores a word (32bits) into memory
        """
        self.memory[self.registers[rs1] + offset]       = self.registers[rs2]
        self.memory[self.registers[rs1] + offset + 1]   = self.registers[rs2] >> 8
        self.memory[self.registers[rs1] + offset + 2]   = self.registers[rs2] >> 16
        self.memory[self.registers[rs1] + offset + 3]   = self.registers[rs2] >> 24
        self.incrementPC()
