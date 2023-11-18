"""
This is a unit test to ensure that the risc machine instruction sets (NOP, HALT, CMP, JMP, LOAD, STORE, ADD, SUB) work as expected
"""

import numpy as np
from machine import machine

#-------------------------------------------------------------------------------
# Test 1: ADD two numbers
#-------------------------------------------------------------------------------
m = machine(mem_size=1000)      # initialize the risc machine with memory of 1000 bytes

m.registers[5] = 5              # manully set register rs5 to 5
m.registers[6] = 10             # manully set register rs6 to 10
m.ADD(7, 6, 5)                  # add resigter 5 and register 6 and store the summation in register 7
print (m.registers[7])

#-------------------------------------------------------------------------------
# Test 2: SUB two numbers
#-------------------------------------------------------------------------------
m.registers[5] = 50             # manully set register rs5 to 50
m.registers[6] = 10             # manully set register rs6 to 10
m.SUB(7, 5, 6)                  # subtract resigter 5 and register 6 and store the summation in register 7
print (m.registers[7])

#-------------------------------------------------------------------------------
# Test 3: CMP two numbers
#-------------------------------------------------------------------------------
m.registers[5] = 50             # manully set register rs5 to 50
m.registers[6] = 10             # manully set register rs6 to 10
m.CMP(5, 6)                     # compare registers 5 and 6
print (m.flag)

m.registers[6] = 50             # manully set register rs6 to 50
m.CMP(5, 6)                     # compare registers 5 and 6
print (m.flag)

#-------------------------------------------------------------------------------
# Test 4: LOAD word
#-------------------------------------------------------------------------------

m.memory[0] = 1
m.memory[1] = 1
m.memory[2] = 1
m.memory[3] = 1

m.registers[2] = 0
m.LW(2, 0, 1)
print(m.registers[2])           # 0x1010101 = 16843009

#-------------------------------------------------------------------------------
# Test 5: STORE word
#-------------------------------------------------------------------------------

m.registers[3] = 16843009
m.registers[4] = 500
m.SW(4, 0, 3)                   # storing the value 0x1010101 from register 3 into memory[500]

print(m.memory[500])
print(m.memory[501])
print(m.memory[502])
print(m.memory[503])


#-------------------------------------------------------------------------------
# Test 6: Excute instruction
#-------------------------------------------------------------------------------
m.registers[1] = 1
m.registers[2] = 2
m.excAssembly('ADD', 1, 1, 2)
print("Excuting Assembly Instructions: " + str(m.registers[1]))


#-------------------------------------------------------------------------------
# Test 7: Excute program ( Fibo )
#-------------------------------------------------------------------------------
# m.excAssembly('Li', a0, 0)   # clear accumilator
# m.excAssembly('Li', s0, 0)   # clear loop counter
# m.excAssembly('Li', s1, 10)  # loop limit = 10 (Max Fibo)

# m.addLabel('Loop')

# m.excAssembly('BGE', , 0)


