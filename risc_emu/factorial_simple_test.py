"""
This is a simple factorial test
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


m.addLabel('return')                            #pc = 0
m.storeAssembly('ADDi', a0, 0, 1)
m.storeAssembly('JALR', ra, ra, 0)



m.addLabel('factorial')                         # pc = 8
m.storeAssembly('BEQ', a0, 0, 'return')
m.storeAssembly('ADDi', sp, sp, -8)
m.storeAssembly('SW', ra, 4, sp)
m.storeAssembly('SW', a0, 0, sp)
m.storeAssembly('ADDi', a0, a0, -1)
m.storeAssembly('JAL', ra, 'factorial')
m.storeAssembly('LW', a1, 0, sp)
m.storeAssembly('ADDi', sp, sp, 4)
m.storeAssembly('MUL', a0, a1, a0)
m.storeAssembly('LW', ra, 0, sp)
m.storeAssembly('ADDi', sp, sp, 4)
m.storeAssembly('JALR', ra, ra, 0)


m.addLabel('start')
m.storeAssembly('ADDi', a0, 0, 5)
m.storeAssembly('ADDi', t1, 0, 5)
m.storeAssembly('JAL', ra, 'factorial')

m.addLabel('end')
m.storeAssembly('ADDi', t2, 0, 1)

m.execute('start', 'end', 0)

print("Factorial of " + str(m.registers[t1]) + " = " + str(m.registers[a0]))