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
print ("Test 1: Adding 5+10: " + str(m.registers[7]))
assert(m.registers[7] == 15)

#-------------------------------------------------------------------------------
# Test 2: SUB two numbers
#-------------------------------------------------------------------------------
m.registers[5] = 50             # manully set register rs5 to 50
m.registers[6] = 10             # manully set register rs6 to 10
m.SUB(7, 5, 6)                  # subtract resigter 5 and register 6 and store the summation in register 7
print("Test 2: 50-10: " + str(m.registers[7]))
assert(m.registers[7] == 40)

#-------------------------------------------------------------------------------
# Test 3: CMP two numbers
#-------------------------------------------------------------------------------
m.registers[5] = 50             # manully set register rs5 to 50
m.registers[6] = 10             # manully set register rs6 to 10
m.CMP(5, 6)                     # compare registers 5 and 6
print("Test 3: value1 != value2: " + str(m.flag))
assert(m.flag == False)

m.registers[6] = 50             # manully set register rs6 to 50
m.CMP(5, 6)                     # compare registers 5 and 6
print("Test 3: value1 == value2: " + str(m.flag))
assert(m.flag == True)

#-------------------------------------------------------------------------------
# Test 4: LOAD word
#-------------------------------------------------------------------------------

m.registers[2] = 0
m.LW(2, 0, 1)
print("Test 4: load word: " + str(m.registers[2]))           # 0x1010101 = 16843009

#-------------------------------------------------------------------------------
# Test 5: STORE word
#-------------------------------------------------------------------------------

m.registers[3] = 16843009
m.registers[4] = 500
m.SW(3, 0, 4)                   # storing the value 0x1010101 from register 3 into memory[500]
print("Test 5: Store word and reading it from memory")
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
print("Test 6: Excuting Assembly Instructions: " + str(m.registers[1]))


#-------------------------------------------------------------------------------
# Test 7: Excute program from memory
#-------------------------------------------------------------------------------

m.reset_machine()
m.write_i32(5, 0)  # manually write '6' into mem[0] (memory @ address 0)
m.write_i32(4, 4)  # manually write '7' into mem[4] (memory @ address 4)
m.LW (11, 0,  0)   # load register x[11] from mem[0 + 0]        -> should have the value 5
m.LW (12, 4,  0)   # load register x[12] from mem[4 + 0]        -> should have the value 4
m.MUL(10, 11, 12)  # x[10] := x[11] * x[12]
print("Excute from memory: " + str(m.registers[10]))            # should have the value 5*4 = 20
assert(m.registers[10] == 20)



