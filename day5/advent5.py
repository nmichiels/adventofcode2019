import numpy as np

instructions = np.loadtxt('input_5.txt', delimiter=',', dtype='int')


print("Start Program")
pc = 0 # program counter
instruction = instructions[pc]
while instruction != 99:

    print("PC %d: %d"%(pc, instruction))
    opcode = instruction

    digits = [int(d) for d in str(opcode)]
    maxDigits = 5
    digits = np.pad(digits, (maxDigits-len(digits),0),  mode='constant', constant_values=(0, 0))
    opcode = digits[-2]*10 + digits[-1]

    digits = digits[:-2] #remove opcode from digits



    
    if opcode == 1 or opcode == 2:

        if digits[-1]:
            val1 = instructions[pc+1]
        else:
            val1 = instructions[instructions[pc+1]]

        if digits[-2]:
            val2 = instructions[pc+2]
        else:
            val2 = instructions[instructions[pc+2]]


        if digits[-3]:
            print("not sure what to do")
            outputPos = instructions[pc+3]
        else:
            outputPos = instructions[pc+3]

        if opcode == 1:
            instructions[outputPos] = val1 + val2
        if opcode == 2:
            instructions[outputPos] = val1 * val2
        pc += 4


    if opcode == 3:
        num = int(input())

        if digits[-1]:
            print("not sure what to do for opcode 3 position")
            instructions[instructions[pc+1]] = num
        else:
            instructions[instructions[pc+1]] = num
        
        pc += 2

    if opcode == 4:
        if digits[-1]:
            val = instructions[pc+1]
        else:
            val = instructions[instructions[pc+1]]


        inputPos = instructions[pc+1]
        print("out", val)
        pc += 2

    if opcode == 5:
        if digits[-1]:
            val = instructions[pc+1]
        else:
            val = instructions[instructions[pc+1]]
        
        if val != 0:
            if digits[-2]:
                pc = instructions[pc+2]
            else:
                pc = instructions[instructions[pc+2]]
        else:
            pc += 3

    if opcode == 6:
        if digits[-1]:
            val = instructions[pc+1]
        else:
            val = instructions[instructions[pc+1]]
        
        if val == 0:
            if digits[-2]:
                pc = instructions[pc+2]
            else:
                pc = instructions[instructions[pc+2]]
        else:
            pc += 3

    if opcode == 7:
        if digits[-1]:
            val1 = instructions[pc+1]
        else:
            val1 = instructions[instructions[pc+1]]

        if digits[-2]:
            val2 = instructions[pc+2]
        else:
            val2 = instructions[instructions[pc+2]]
        

        if digits[-3]:
            print("not sure what to do for opcode 7")
            outPos = instructions[pc+3]
        else:
            # print("not sure what to do for opcode 7")
            outPos = instructions[pc+3]
            #outPos = instructions[instructions[pc+3]]

        if val1 < val2:
            instructions[outPos] = 1
        else:
            instructions[outPos] = 0
        pc += 4   

    if opcode == 8:
        if digits[-1]:
            val1 = instructions[pc+1]
        else:
            val1 = instructions[instructions[pc+1]]

        if digits[-2]:
            val2 = instructions[pc+2]
        else:
            val2 = instructions[instructions[pc+2]]
        

        if digits[-3]:
            print("not sure what to do for opcode 8")
            outPos = instructions[pc+3]
        else:
            #print("not sure what to do for opcode 8")
            outPos = instructions[pc+3]
            #outPos = instructions[instructions[pc+3]]

        if val1 == val2:
            instructions[outPos] = 1
        else:
            instructions[outPos] = 0
            
        pc += 4

    instruction = instructions[pc]
    

print("\n\nResult: ", instructions[0])