"""
This is a simple fibonacci test
F(n) = F(n-1) + F(n-2)
"""

import numpy as np
from machine import machine

#-------------------------------------------------------------------------------
# Test 7: Excute program ( Factorial )
#-------------------------------------------------------------------------------
m = machine(mem_size=8000)      # initialize the risc machine with memory of 1000 bytes
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


m.pc = 4000
m.addLabel('BaseCase')              # Base case: n = 0 or n = 1  
m.storeAssembly('JALR', ra, ra, 0)

m.addLabel('fibonacci')
m.storeAssembly('BEQ', s0, a0, 'BaseCase')
m.storeAssembly('BLT', a0, s0, 'BaseCase') 
m.storeAssembly('ADDi', sp, sp, -12)
m.storeAssembly('SW', ra, 8, sp)
m.storeAssembly('SW', a0, 4, sp)
m.storeAssembly('ADDi', a0, a0, -1)
m.storeAssembly('JAL', ra, 'fibonacci')

m.storeAssembly('SW', a0, 0, sp)
m.storeAssembly('LW', a0, 4, sp)
m.storeAssembly('ADDi', a0, a0, -2)
m.storeAssembly('JAL', ra, 'fibonacci')

m.storeAssembly('LW', t0, 0, sp)
m.storeAssembly('ADD', a0, a0, t0)
m.storeAssembly('LW', ra, 8, sp)
m.storeAssembly('ADDi', sp, sp, 12)
m.storeAssembly('JALR', ra, ra, 0)


m.addLabel('start')
m.storeAssembly('ADDi', a0, 0, 10)           # the fib value is stored in a0
m.storeAssembly('ADDi', s0, 0, 1)
m.storeAssembly('ADD', t2, 0, a0)
m.storeAssembly('JAL', ra, 'fibonacci')

m.addLabel('end')
m.storeAssembly('ADD', t6, 0, a0)

m.execute('start', 'end', 0)

print("Fibonacci of " + str(m.registers[t2]) + " = " + str(m.registers[a0]))