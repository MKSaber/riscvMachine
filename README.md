# riscv Machine
Implementing a small RISC machine in python. The machine supports several instructions and can run simple programs.
It supports encoding and storing an assembly code in memory and then decoding and executing it.

Supported Instructions:
- NOP, HALT, CMP, JMP, LW, SW, ADD, ADDi, SUB, XOR, AND, OR, BEQ, BNE, Li, BGE, BLT, JAL, MUL, Li, JALR

This risc-Machine contains:
- some of the RISC instruction set
- decoder
- encoder
- memory

# Folder Structure:
```bash
risc_emu
  |______ Docs
  |        |____ reference-card.pdf
  |         |____ riscv-spec-v2.2.pdf
  |
  |______ machine.py                          # Risc emulator
  |______ Instruction_test.py                 # unit testing the risc instructions
  |______ factorial_simple_test.py            # storing an assembly code into memory + decoding and executing it ( Factorial )
```

# How to use the emulator
- Run commands directly using the commands defined ADD(), CMP(), LW() ... etc
- use excAssembly to run 1 line of assembly instruction at a time.
- Store an assembly program in memory using addLabel(),  storeAssembly() and run the code using execute()
