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


# Available tests and examples:
- instruction_test.py: includes some unit tests to run some instructions and validates the outcome
- factorial_simple_test.py: stores a recursive factorial assembly code into memory, then excutes it.
- fib_test.py: stores a recursive factorial assembly code into memory, then excutes it.

# Limitations:
- This emulator does not yet support linking - which means that the assembly code needs to be stored in a sequential order. The code cannot store a branch instruction to a label that has not yet been added.

# Future Work:
- Support linker/label tables where the code could be written non sequentially and the linker would find and link instructions accordingly.



# Questions and Answers:
**1. Define and implement the machine model and the instruction set. State very clearly any assumptions you make.**  
Each needed instruction was defined and implemented with a comment that could be read out via --help()
Extra instructions were needed to be able to perform more complex tasks.

**2. Write a RISC machine for executing the instruction set.**   
RISC emulator can execute instructions directly based on an assembly format.
Write some tests and a test harness that checks that these tests pass.   
3 test files were written to unit test the instructions + do a full validation test that goes through multiple APIs at the same time   

**3. Write some programs (fib, factorial, sum) for the RISC machine.**   
factorial program works as expected
fib program works as expected   

**4. How would you implement linked lists here?**  
This means I'll need to create types and use the *next to dereference the memory. Not sure how can that be achieved but my assumption would be as follows: once a node is created: 3 integer values will be stored: a. pointer (has the address of the node(using the self.pc when storing it) b. value (contans the value stored in that node) c. *next ( initially will contain 0 ( NULL)) and every time that pointer is assigned to a node: its value will contain the address of the next node's pointer.   

**5. Design a binary encoding for the instruction set. Get your RISC machine to decode and then execute the program.**  
Done to solve the factorial assembly code as I was unable to find a non-recursive code online   

**6. Extend the instruction set with other arithmetic and logical instructions.**  
Done to be able to execute a full program (AND, OR, XOR, MUL, ...)   

**7. Extend the memory system by a cache. Explain how you've implemented a cache replacement policy.**  
The only way that I could think of a cache replacement policy would be as follows: have a small array acting as cashe the first few instruction reads are copied into the cache, every new fetch would check cache first, and if a cache hit -> read from cache, if a cashe miss -> read from memory.   

**8. Come up with a metric to cost program execution in terms of compute + memory. Explain your idea and implement it.**  
Created a much of metric counters that would count the number of instructions, the number of arithmetic operations, the number of branches, and the time that the code took to execute.this is protected by a machine flag "debug"
