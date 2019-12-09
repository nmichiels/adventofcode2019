import numpy as np

instructions = np.loadtxt('input_2.txt', delimiter=',', dtype='int')
print(instructions.shape)

#init
instructions[1] = 12
instructions[2] = 2

pc = 0 # program counter
opcode = instructions[pc]
while opcode != 99:
    inputPos1 = instructions[pc+1]
    inputPos2 = instructions[pc+2]
    outputPos = instructions[pc+3]


    if opcode == 1:
        instructions[outputPos] = instructions[inputPos1] + instructions[inputPos2]

    if opcode == 2:
        instructions[outputPos] = instructions[inputPos1] * instructions[inputPos2]


    pc += 4
    opcode = instructions[pc]

print("Result: ", instructions[0])