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



def getFeedback(dir, inputs, outputs, notify):
   
    inputs.put(dir)

    oxygenFound = False
    # get feedback from intcode
    out = notify.get()

    if out == -1:
        return -1

    out = outputs.get()

    return out
   
def updateMap(feedback, droidPos, direction, map):


      
    targetPos = np.add(droidPos, direction)

    if feedback == -1:
        pass
    elif feedback == 0:
        # droid hit a wall, position not changed
        map[targetPos[0],targetPos[1]] = '#'
    elif feedback == 1:
        # droid moved in the requested direction
        map[targetPos[0],targetPos[1]] = 'D'
        map[droidPos[0],droidPos[1]] = '.'
    elif feedback == 2:
        # droid moved in the requested direction
        map[targetPos[0],targetPos[1]] = 'D'
        map[droidPos[0],droidPos[1]] = '.'
    else:
        print("ERROR: unkown feedback", out)

    return
  




def backtrack(map, droidPos, currentPath):
    for i in range(1,5):
        pass



def run():
    instructions = np.loadtxt('input_15.txt', delimiter=',', dtype='int64')
    code = instructions.copy()

    map = np.chararray((42, 42))
    map[:] = 'W'
    map = map.astype('unicode')

    droidPos = [int(map.shape[0] / 2.0),int(map.shape[0] / 2.0)]
    map[droidPos[0],droidPos[1]] = 'D'


    showMap(map, droidPos)

    inputs = Queue()
    outputs = Queue()
    notify = Queue() #used for notification of output or end of program
    notifyOnInput = Queue()

    process = Process(target = runProgram, args=(code, inputs, outputs, notify,notifyOnInput))
    process.start()


    
    # generate random integer values
    from random import seed
    from random import randint
    import time
    # seed random number generator
    seed(1)

    directions = [[0,0],[-1,0],[1,0],[0,-1],[0,1]]


    backtrack(map, droidPos, [])


    while True:

        


        dir = randint(1, 4)
        direction = directions[dir]
        

        targetPos = np.add(droidPos, direction)



        # get feedback from intcode
        out = getFeedback(dir, inputs, outputs, notify)
        updateMap(out, droidPos, direction, map)


        if out == -1:
            break
        elif out == 0:
            # droid hit a wall, position not changed
            pass
        elif out == 1:
            # droid moved in the requested direction
            droidPos = targetPos
        elif out == 2:
            # droid moved in the requested direction
            droidPos = targetPos
            print("Found oxygen system at position", droidPos)
        else:
            print("ERROR: unkown feedback", out)

        showMap(map, droidPos)
        
        print(droidPos)
        print(direction)
        time.sleep(0.2)


    print("end")
    showMap(map)  
    # part 1
    unique, counts = np.unique(map, return_counts=True)
    occ = dict(zip(unique, counts))
    # if 0 in occ:
    #     del occ[0]
    print(occ)
    print("Result Part 1:", occ['.'])  
    



if __name__ == '__main__':
    #freeze_support()
    run()
