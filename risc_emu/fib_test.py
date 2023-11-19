"""
This is a simple fibonacci test
"""

import numpy as np
from machine import machine

#-------------------------------------------------------------------------------
# Test 7: Excute program ( Factorial )
#-------------------------------------------------------------------------------
m = machine(mem_size=4000)      # initialize the risc machine with memory of 1000 bytes
m.reset_machine()
m.clear_memory()

zero = 0
ra = 1
sp = 2
gp = 3
tp = 4
t0 = 5
t1 = 6
t2 = 7
s0 = 8
s1 = 9
a0 = 10
a1 = 11
a2 = 12
a3 = 13
a4 = 14
a5 = 15
a6 = 16
a7 = 17
s2 = 18
s3 = 19
s4 = 20
s5 = 21
s6 = 22
s7 = 23
s8 = 24
s9 = 25
s10 = 26
s11 = 27
t3 = 28
t4 = 29
t5 = 30
t6 = 31


# addi t0, x0, 1
# add s0, x0, x0

# jal ra, Fibonacci
# j print


# Fibonacci:
# bge t0, a0, BaseCase
# addi sp, sp, -8
# sw ra, 0(sp)
# sw a0, 4(sp)
# addi a0, a0, -1
# jal ra, Fibonacci

# lw a1, 4(sp)
# sw a0, 4(sp)
# addi a0, a1, -2
# jal ra, Fibonacci
# lw a1, 4(sp)
# add a0, a0, a1
# lw ra, 0(sp)
# addi sp, sp, 8 

# BaseCase:
# jr ra
m.pc = 1200
m.addLabel('BaseCase')   
m.storeAssembly('JALR', ra, ra, 0)

m.addLabel('fibonacci')
m.storeAssembly('BEQ', t0, a0, 'BaseCase')  
m.storeAssembly('ADDi', sp, sp, -8)
m.storeAssembly('SW', ra, 0, sp)
m.storeAssembly('SW', a0, 4, sp)
m.storeAssembly('ADDi', a0, a0, -1)
m.storeAssembly('JAL', ra, 'fibonacci')

m.storeAssembly('LW', a1, 4, sp)
m.storeAssembly('SW', a0, 4, sp)
m.storeAssembly('ADDi', a0, a1, -2)
m.storeAssembly('JAL', ra, 'fibonacci')

m.storeAssembly('LW', a1, 4, sp)
m.storeAssembly('ADD', a0, a0, a1)
m.storeAssembly('LW', ra, 0, sp)
m.storeAssembly('ADDi', sp, sp, 8)
m.addLabel('end')
m.storeAssembly('ADDi', t2, 0, 1)

m.addLabel('start')
m.storeAssembly('ADDi', a0, 0, 2)
m.storeAssembly('ADDi', t0, 0, 1)
m.storeAssembly('ADDi', s0, 0, 0)
m.storeAssembly('ADDi', a7, 0, 4)
m.storeAssembly('JAL', ra, 'fibonacci')

m.addLabel('end')
m.storeAssembly('ADDi', t2, 0, 1)

m.execute('start', 'end', 0)

print("Fibonacci of " + str(m.registers[t0]) + " = " + str(m.registers[a0]))