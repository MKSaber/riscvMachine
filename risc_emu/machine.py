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
        self.memory         = np.zeros(mem_size, dtype=np.uint8)
        self.memory_size    = mem_size

        # set registers to 0 ( 32 registers of type: int32)
        # x0        hard-wired zero
        # x1        return address
        # x2        stack pointer
        # x3        global pointer
        # x4        thread pointer
        # x5        temp/alternate link register
        # x6-7      temp
        # x8        saved register / frame pointer
        # x9        saved register
        # x10-11    function args/return values
        # x12-17    function args
        # x18-27    saved registers
        # x28-31    temp
        self.registers      = np.zeros(32, dtype=np.int32)

        # set program counter to 0
        self.pc             = np.zeros(1, dtype=np.int32)

        #set dictionary with supported instructions
        self.instruciton_dictionary = {'NOP': self.NOP, 'HALT': self.HALT, 'CMP': self.CMP, 'JMP': self.JMP, 'LW': self.LW, 'SW': self.SW, 'ADD': self.ADD, 'ADDi': self.ADDi, 'SUB': self.SUB, 'XOR': self.XOR, 'AND': self.AND, 'OR': self.OR, 'BEQ': self.BEQ, 'BNE': self.BNE}

        #set flag for comparisons to false
        self.flag           = False

        #create label dictionary empty till a program is loaded
        self.label_dictionary = {}

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

    def SW(self, rs1, offset, rs2):
        """
        Stores a word (32bits) into memory
        """
        self.memory[self.registers[rs1] + offset]       = self.registers[rs2]
        self.memory[self.registers[rs1] + offset + 1]   = self.registers[rs2] >> 8
        self.memory[self.registers[rs1] + offset + 2]   = self.registers[rs2] >> 16
        self.memory[self.registers[rs1] + offset + 3]   = self.registers[rs2] >> 24
        self.incrementPC()

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
            
        
    def execute(self, start, end=None, instructionCount=0):
        """
        Executes code from start label to end label or for instructionCount number of instructions
        """
        self.pc = start
        if end is None:
            for i in range(instructionCount):
                inst = self.read(self.pc)


    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Reset Instructions
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def reset_machine(self):
        self.registers  = np.zeros(32, dtype=np.int32)
        self.pc         = 0
        self.flag       = False
    
    def clear_memory(self):
        self.memory     = np.zeros(self.memory_size, dtype=np.uint8)