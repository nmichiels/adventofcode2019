import numpy as np


def runProgram(instructions, inputs, outputs, notify, notifyOnInput):
    
    #instructions = instructions.astype(dtype='int64')
    print(instructions.dtype)
  
    relativeBase = 0
 
    pc = 0 # program counter
    instruction = instructions[pc]


    # pad instructions to increase program memory
    maxSize = 4000000
    instructions = np.pad(instructions, (0, maxSize-len(instructions)), mode='constant', constant_values=(0, 0))
    #print("instructions.size",instructions.shape)

    while instruction != 99:
        #print("PC %d: %d"%(pc, instruction))
        opcode = instruction


        digits = [int(d) for d in str(opcode)]
        maxDigits = 5
        digits = np.pad(digits, (maxDigits-len(digits),0),  mode='constant', constant_values=(0, 0))
    

        opcode = digits[-2]*10 + digits[-1]

        digits = digits[:-2] #remove opcode from digits



    
        if opcode == 1 or opcode == 2:
            if digits[-1] == 1:  #intermediate mode
                val1 = instructions[pc+1]
            elif digits[-1] == 2: #relative mode
                val1 = instructions[relativeBase+instructions[pc+1]]
            else: #position mode
                val1 = instructions[instructions[pc+1]]

            if digits[-2] == 1:
                val2 = instructions[pc+2]
            elif digits[-2] == 2: #relative mode
                val2 = instructions[relativeBase+instructions[pc+2]]
            else: #position mode
                val2 = instructions[instructions[pc+2]]


            if digits[-3] == 1:
                print("Error not implemented opcode 1 and 2")
                outputPos = instructions[pc+3]
            elif digits[-3] == 2:
                outputPos = relativeBase + instructions[pc+3]
            else:

                outputPos = instructions[pc+3]

            if opcode == 1:
                instructions[outputPos] = val1 + val2
            if opcode == 2:
                instructions[outputPos] = val1 * val2
            pc += 4


        if opcode == 3:
            print("waiting for input")
            notifyOnInput.put(1)
            num =  inputs.get()
            print("done waiting for input")
            if digits[-1] == 1:
                print("not sure what to do for opcode 3 position")
                instructions[instructions[pc+1]] = num
            elif digits[-1] == 2: #relative mode
                instructions[relativeBase+instructions[pc+1]] = num
            else:
                instructions[instructions[pc+1]] = num
        
            pc += 2

        if opcode == 4:
            if digits[-1] == 1:
                val = instructions[pc+1]
            elif digits[-1] == 2:
                val = instructions[relativeBase+instructions[pc+1]]
            else:
                val = instructions[instructions[pc+1]]


            inputPos = instructions[pc+1]
            #print(val)
            outputs.put(val)
            notify.put(1) # notify output
            pc += 2

        if opcode == 5:
            if digits[-1] == 1:
                val = instructions[pc+1]
            elif digits[-1] == 2:
                val = instructions[relativeBase+instructions[pc+1]]
            else:
                val = instructions[instructions[pc+1]]
        
            if val != 0:
                if digits[-2] == 1:
                    pc = instructions[pc+2]
                elif digits[-2] == 2:
                    pc = instructions[relativeBase+instructions[pc+2]]
                else:
                    pc = instructions[instructions[pc+2]]
            else:
                pc += 3

        if opcode == 6:
            if digits[-1] == 1:
                val = instructions[pc+1]
            elif digits[-1] == 2:
                val = instructions[relativeBase+instructions[pc+1]]
            else:
                val = instructions[instructions[pc+1]]
        
            if val == 0:
                if digits[-2] == 1:
                    pc = instructions[pc+2]
                elif digits[-2] == 2:
                    pc = instructions[relativeBase+instructions[pc+2]]
                else:
                    pc = instructions[instructions[pc+2]]
            else:
                pc += 3

        if opcode == 7:
            if digits[-1] == 1:
                val1 = instructions[pc+1]
            elif digits[-1] == 2:
                 val1 = instructions[relativeBase+instructions[pc+1]]
            else:
                val1 = instructions[instructions[pc+1]]

            if digits[-2] == 1:
                val2 = instructions[pc+2]
            elif digits[-2] == 2:
                val2 = instructions[relativeBase+instructions[pc+2]]
            else:
                val2 = instructions[instructions[pc+2]]
            

            if digits[-3] == 1:
                print("not sure what to do for opcode 7")
                outPos = instructions[pc+3]
            elif digits[-3] == 2:
                outPos = relativeBase + instructions[pc+3]
            else:
                outPos = instructions[pc+3]
                #outPos = instructions[instructions[pc+3]]

            if val1 < val2:
                instructions[outPos] = 1
            else:
                instructions[outPos] = 0
            pc += 4   

        if opcode == 8:
            if digits[-1] == 1:
                val1 = instructions[pc+1]
            elif digits[-1] == 2:
                val1 = instructions[relativeBase+instructions[pc+1]]
            else:
                val1 = instructions[instructions[pc+1]]

            if digits[-2] == 1:
                val2 = instructions[pc+2]
            elif digits[-2] == 2:
                val2 = instructions[relativeBase+instructions[pc+2]]
            else:
                val2 = instructions[instructions[pc+2]]
        

            if digits[-3] == 1:
                print("not sure what to do for opcode 8")
                outPos = instructions[pc+3]
            elif digits[-3] == 2:
                outPos = relativeBase + instructions[pc+3]
            else:
                outPos = instructions[pc+3]
                #outPos = instructions[instructions[pc+3]]

            if val1 == val2:
                instructions[outPos] = 1
            else:
                instructions[outPos] = 0
            
            pc += 4

        if opcode == 9:
            #print('9')
            if digits[-1] == 1:
                val = instructions[pc+1]
            elif digits[-1] == 2:
                #print("not sure what to do for opcode 9")
                val = instructions[relativeBase+instructions[pc+1]]
            else:
                val = instructions[instructions[pc+1]]

            relativeBase += val

            pc += 2

        instruction = instructions[pc]

    notify.put(-1) # notify end of program
    return outputs