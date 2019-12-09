import numpy as np



def runProgram(instructions, inputs, outputs):
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
            num =  inputs.get()

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
            outputs.put(val)
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
    return outputs


def run():
    instructions = np.loadtxt('input_7.txt', delimiter=',', dtype='int')
    code = instructions.copy()

    import itertools
    combinations = list(itertools.permutations([5,6,7,8,9]))
    combination = [9,8,7,6,5]

    maxOutput = 0.0
    for combination in combinations:
        output = runOnce(instructions, combination)
        if output > maxOutput:
            maxOutput = output

    print("Max output: ", maxOutput)

def runOnce(instructions, combination):


    amplifiers = [instructions.copy() for i in range(5)]


    from multiprocessing import Process, Queue


    amplifierInputs = [Queue() for i in range(5)]

    endOutput = Queue()
    amplifierThreads = []
    for i in range(5):
        if i < 4:
            amplifierThreads.append(Process(target = runProgram, args=(amplifiers[i],amplifierInputs[i], amplifierInputs[i+1])))
        else:
            amplifierThreads.append(Process(target = runProgram, args=(amplifiers[i],amplifierInputs[i], amplifierInputs[0])))
        amplifierThreads[i].start()


    

    for i in range(5):
        amplifierInputs[i].put(combination[i])

    amplifierInputs[0].put(0)

    for i in range(5):
        amplifierThreads[i].join()
    

    return amplifierInputs[0].get()

    import sys
    sys.exit(0)
    maxOutput = 0.0
    for combination in combinations:

        phases  = combination
        inputs = [phases[0], 0]

        totalOutput = 0
        for i in range(1,6):
            #code = instructions.copy()  
            outputs = runProgram(amplifiers[i-1],inputs)
            print("outputs  ", outputs)
            if i < 5:
                inputs = [phases[i], outputs[-1]]
            totalOutput = outputs[-1]

        print("totalOutput", totalOutput)
        if totalOutput > maxOutput:
            maxOutput = totalOutput

    print("max output: ", maxOutput)



if __name__ == '__main__':
    #freeze_support()
    run()
