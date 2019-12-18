import numpy as np
import time
from intcode import runProgram
from multiprocessing import Process, Queue
import os

def showMap(map, droidPos, steps = 0):

    #os.system('clear')  # For Linux/OS X
    os.system('cls')  # For Windows
    print('')
    print("STEPS:", steps)

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i,j] == 'W':
                print(' ', end='')
            else:
                print(map[i,j], end='')
        print('')
    print('')
    print(" ", flush=True)
    print("Position Droid:", droidPos)



def unitTestTrajectoryAndMainMovementRoutine(mainMovementRoutine, functions, trajectory):
    test = []
    for functionName in mainMovementRoutine:
        functionRoutine = functions[functionName]
        for step in functionRoutine:
            test.append(step)

    print(test)


    theSame = True
    for i in range(len(test)):
        if test[i][0] != trajectory[i][0] or test[i][1] != trajectory[i][1]:
            theSame = False
            break

    return theSame

def run():
    instructions = np.loadtxt('input_17.txt', delimiter=',', dtype='int64')
    code = instructions.copy()

    code[0] = 2
    map = np.chararray((51, 51))
    map[:] = 'W'
    map = map.astype('unicode')

    #droidPos = [int(map.shape[0] / 2.0),int(map.shape[0] / 2.0)]
    #map[droidPos[0],droidPos[1]] = 'D'


    #showMap(map, droidPos)

    inputs = Queue()
    outputs = Queue()
    notify = Queue() #used for notification of output or end of program
    notifyOnInput = Queue()

    process = Process(target = runProgram, args=(code, inputs, outputs, notify,notifyOnInput))
    process.start()


    currentRow = 0
    currentCol = 0
    while True:

        # get feedback from intcode
        out = notify.get()

        if out == -1 or out == "done":
            break

        out = outputs.get()
        #print(out)

        if out == 10:
            #print("newline", currentCol, currentRow)
            currentRow += 1
            currentCol = 0
        else:
            map[currentRow,currentCol] = chr(out)
            currentCol+=1


    #showMap(map, droidPos =[0,0])

    numCrossings = 0
    for row in range(1, map.shape[0]-1):
        for col in range(1, map.shape[1]-1):
            if map[row,col] == '#' and map[row+1,col] == '#' and map[row-1,col] == '#' and map[row,col+1] == '#' and map[row,col-1] == '#':
                #map[row,col] = 'O'
                numCrossings += row*col
    showMap(map, droidPos =[0,0])
    print("Result Part 1:", numCrossings)



    #process.join()

    currentPos = np.where(map == '^')
    currentRow = currentPos[0][0]
    currentCol = currentPos[1][0]
    print("startPos: ", currentRow, currentCol)


    def findDir(row, col, dirName, map):

            
        if dirName == 'U' and col+1 < map.shape[1] and map[row,col+1] == '#':
            return [0,+1], 'R', 'R'
        elif dirName == 'U' and col-1 >= 0 and map[row,col-1] == '#':
            return [0,-1], 'L', 'L'
        elif dirName == 'D' and col+1 < map.shape[1] and map[row,col+1] == '#':
            return [0,+1], 'R', 'L'
        elif dirName == 'D' and col-1 >= 0 and map[row,col-1] == '#':
            return [0,-1], 'L', 'R'
        elif dirName == 'R' and row+1 < map.shape[0] and map[row+1,col] == '#':
            return [1,0], 'D', 'R'
        elif dirName == 'R' and row-1 >= 0 and map[row-1,col] == '#':
            return [-1,0], 'U', 'L'
        elif dirName == 'L' and row+1 < map.shape[0] and map[row+1,col] == '#':
            return [1,0], 'D', 'L'
        elif dirName == 'L' and row-1 >= 0 and map[row-1,col] == '#':
            return [-1,0], 'U', 'R'
        else:
            print("no dir found")
            return None, None, None


    dirName = 'U'
    currentDir, dirName, turn = findDir(currentRow, currentCol,dirName,  map)

    trajectory = []

    


    while currentDir is not None:
        steps = 0
        while True:

            newRow = currentRow +  currentDir[0]
            newCol = currentCol + currentDir[1]

        
            if newRow < map.shape[0] and newRow >= 0 and newCol <  map.shape[1] and newCol >= 0 and map[newRow, newCol] == '#':
                currentRow = newRow
                currentCol = newCol
                
                steps += 1
            else:
                break
        trajectory.append((turn, steps))

        currentDir, dirName, turn = findDir(currentRow, currentCol,dirName,  map)
        #print("dir:", currentDir, dirName, turn)

    showMap(map, droidPos =[0,0])
    print(trajectory)


    def findLongestSubPath(trajectory):
        #print(subPath[i][0])

        subTrajectories = [trajectory]



        def findSubPaths(startPos, maxLen):
            subPaths = []
            maxSubPathLen = 0
            for i in range(1, maxLen+1):
                subPath = trajectory[startPos:startPos+i]
                for j in range(i, len(trajectory)-len(subPath)+1):
                    found = True
                    for t in range(len(subPath)):
                        if (type(trajectory[j+t]) is not tuple) or subPath[t][0] != trajectory[j+t][0] or subPath[t][1] != trajectory[j+t][1]:
                            found = False
                            break

                    if found:
                        if len(subPath) > maxSubPathLen:
                            maxSubPathLen = len(subPath)
                        subPaths.append((len(subPath), j))
                        #print("Found subpath ", subPath , "at index", j)
           
            return subPaths, maxSubPathLen


        def findAndAlterLongestSubPath(trajectory, startPos, maxLen, functions, functionName):
            subPaths, maxSubPathLen = findSubPaths(startPos, maxLen)
            subPaths = sorted(subPaths, key=lambda x: x[1], reverse=True)


            for subPath in subPaths:
                if subPath[0] == maxSubPathLen:
                    del trajectory[subPath[1]:subPath[1]+maxSubPathLen]
                    trajectory.insert(subPath[1], functionName)


            #print(functionName, "  ", maxSubPathLen)
            functions[functionName] = trajectory[startPos:startPos+maxSubPathLen]
            del trajectory[startPos:startPos+maxSubPathLen]
            trajectory.insert(startPos, functionName)
            

        def findStartIndexAndLength(trajectory):
            #find start index and stopindex ==> first range without function names
            startIdx = -1
            length = -1
            for i in range(len(trajectory)):

                if startIdx == -1 and type(trajectory[i]) is tuple:
                    startIdx = i

                if startIdx != -1:
                    if i == len(trajectory)-1:
                        length = i - startIdx + 1
                        break
                       
                    if type(trajectory[i]) is not tuple:
                        length = i - startIdx
                        break

            return startIdx, length




        functions = {}
        
  
        startIdx = 0
        length = len(trajectory)
        currentFunction =  ord('A')

        while startIdx >= 0 and length > 0:
            findAndAlterLongestSubPath(trajectory, startIdx, length, functions, chr(currentFunction))
            #print(trajectory)
            #print(functions)
            startIdx, length = findStartIndexAndLength(trajectory)
            print(startIdx, length)
            currentFunction += 1
        #print("functions",functions)
        return trajectory, functions
        #findAndAlterLongestSubPath(trajectory, 1, 4, functions, 'B')
        #print(trajectory)
        ##print("functions",functions)

        #findAndAlterLongestSubPath(trajectory, 3, 4, functions, 'C')
        #print(trajectory)

        #findAndAlterLongestSubPath(trajectory, 9, 4, functions, 'D')
        #print(trajectory)
        #print("functions",functions)

        #subPaths, maxSubPathLen = findSubPaths(1, 6)
        #del trajectory[0:maxSubPathLen]
        #trajectory.insert(0, 'A')

        #for subPath in subPaths:
        #    if subPath[0] == maxSubPathLen:
        #        del trajectory[subPath[1]:subPath[1]+maxSubPathLen]
        #        trajectory.insert(subPath[1], 'A')

        
        #print("subPaths", sorted(subPaths, key=lambda x: x[0], reverse=True))

    mainMovementRoutine = trajectory.copy()
    mainMovementRoutine, functions = findLongestSubPath(mainMovementRoutine)  
    
    assert unitTestTrajectoryAndMainMovementRoutine(mainMovementRoutine, functions, trajectory)

    print("mainMovementRoutine", mainMovementRoutine)
    print("functions", functions)

    



    #code = instructions.copy()
    #code[0] = 2
    #inputs = Queue()
    #outputs = Queue()
    #notify = Queue() #used for notification of output or end of program
    #notifyOnInput = Queue()
    #process = Process(target = runProgram, args=(code, inputs, outputs, notify,notifyOnInput))
    #process.start()

    test = []
    for i in range(len(mainMovementRoutine)-1):
        inputs.put(ord(mainMovementRoutine[i]))
        test.append(ord(mainMovementRoutine[i]))
        inputs.put(44)
        test.append(44)
    inputs.put(ord(mainMovementRoutine[len(mainMovementRoutine)-1]))
    test.append(ord(mainMovementRoutine[len(mainMovementRoutine)-1]))
    inputs.put(10)
    test.append(10)


    test2 = []
    #print("test", test)
    # pass the movement functions
    for functionName in functions:
        print(functionName)

        function = functions[functionName]
        print(function)
        for i in range(len(function)-1):
            inputs.put(ord(function[i][0]))
            test2.append(ord(function[i][0]))
            inputs.put(44)
            test2.append(44)
            steps = str(function[i][1])
            for char in steps:
                inputs.put(ord(char))
                test2.append(ord(char))
            inputs.put(44)
            test2.append(44)

        i = len(function)-1
        inputs.put(ord(function[i][0]))
        test2.append(ord(function[i][0]))
        inputs.put(44)
        test2.append(44)
        steps = str(function[i][1])
        for char in steps:
            inputs.put(ord(char))
            test2.append(ord(char))



        inputs.put(10)
        test2.append(10)

    print("test2", test2)

    inputs.put(ord('n'))
    inputs.put(10)
    # get feedback from intcode


    print("waiting for output")
    out = notify.get()
    while out == "done":
        out = notify.get()
        print(out)



    if out == -1:
        print("Program ended before output")

    while not outputs.empty():
        out = outputs.get()

        print("Result Part 5: " , chr(out), out)


    #while out == "done":
    #    out = notify.get()
    #    print(out)

    while True:
        out = outputs.get()

 
        print("Result Part 5: " , chr(out), out)


    print("number out:")
    process.join()










    
    
                

        #
    






  



if __name__ == '__main__':
    #freeze_support()
    run()
