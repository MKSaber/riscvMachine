"""
This is a factorial test
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

m.addLabel('fact')                  # arg: n in a0, returns n! in a1
m.storeAssembly('ADDi', sp, sp, -8)
m.storeAssembly('SW', ra, 0, sp)
m.storeAssembly('Li', t0, 2)
m.storeAssembly('')


m.addLabel('start')
# print("-----")
# print(m.getLabel('start'))
# print("-----")


# m.addLabel('ret_one')
# m.excAssembly('Li', a1, 1)

# m.addLabel('done')
# m.excAssembly('LW', ra, 0, sp)
# m.excAssembly('ADDi', sp, sp, 8)



# m.addLabel('fact')                  # arg: n in a0, returns n! in a1
# m.excAssembly('ADDi', sp, sp, -8)   # reverse stack area
# m.excAssembly('SW', ra, 0, sp)
# m.excAssembly('Li', t0, 2)
# m.excAssembly('BLT', a0, t0, 'ret_one')         #TODO: check ret value location
# m.excAssembly('SW', a0, 4, sp)
# m.excAssembly('ADDi', a0, a0, -1)
# m.excAssembly('JAL', m.getLabel('fact'))
# m.excAssembly('LW', t0, 4, sp)
# m.excAssembly('MUL', a1, t0, a1)
# m.excAssembly('JUMP', m.getLabel('done'))       #TODO: check done location


