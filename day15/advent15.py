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



def tryToTakeStepIntoDirection(dir, inputs, outputs, notify):
   
    inputs.put(dir)

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
        map[targetPos[0],targetPos[1]] = 'O'
        map[droidPos[0],droidPos[1]] = '.'
    else:
        print("ERROR: unkown feedback", out)

    return
  


import time


def getInverseDir(dir):
    if dir == 1:
       return 2
    elif dir == 2:
        return 1
    elif dir == 3:
        return 4
    elif dir == 4:
        return 3


def backtrack(map, droidPos, directions, currentPath, inputs, outputs, notify):
    uniquePaths = []
    for i in range(1,5):
        #print(droidPos,  i)
        
        direction = directions[i]
        newDroidPos = np.add(droidPos, direction)

        if map[newDroidPos[0],newDroidPos[1]] != 'W':
            continue
        
        feedback = tryToTakeStepIntoDirection(i, inputs, outputs, notify)
        updateMap(feedback, droidPos, direction, map)
        
        #time.sleep(0.5)
        #showMap(map, droidPos)

        
        if feedback == 0:
            # droid hit a wall, position not changed
            continue

        if feedback == -1:
            print("Program ended with 99")
            return uniquePaths
        if feedback == 1:
            # droid moved in the requested direction
            newPath = currentPath + [newDroidPos]
            uniquePaths += backtrack(map, newDroidPos, directions,newPath, inputs, outputs, notify)
            
            # take one step back to backtrack previous pos
            feedback = tryToTakeStepIntoDirection(getInverseDir(i), inputs, outputs, notify)
            continue

        if feedback == 2:
            # droid moved in the requested direction, oxygen system found!
            uniquePaths += [currentPath + [newDroidPos]]
            print(uniquePaths)

           
            # take one step back to backtrack previous pos
            feedback = tryToTakeStepIntoDirection(getInverseDir(i), inputs, outputs, notify)
            continue

    return uniquePaths

def fillOxygen(map, directions):
    unique, counts = np.unique(map, return_counts=True)
    occ = dict(zip(unique, counts))

    oxygens = np.where(map == 'O')
    oxygens = [(oxygens[0][0],oxygens[1][0])]


    minutes = 0
    print(oxygens)
    while '.' in occ:
        newOxygens = oxygens.copy()
        for oxygen in oxygens:
            for i in range(1,5):
                direction = directions[i]
                newPos = np.add(oxygen, direction)

                if map[newPos[0],newPos[1]] == '.' or map[newPos[0],newPos[1]] == 'D':
                    map[newPos[0],newPos[1]] = 'O'
                    newOxygens.append(newPos)
        oxygens = newOxygens
        showMap(map, [0,0])

        minutes += 1
        unique, counts = np.unique(map, return_counts=True)
        occ = dict(zip(unique, counts))
    return minutes

def run():
    instructions = np.loadtxt('input_15.txt', delimiter=',', dtype='int64')
    code = instructions.copy()

    map = np.chararray((52, 52))
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


 
    directions = [[0,0],[-1,0],[1,0],[0,-1],[0,1]]

    currentpath = [np.array(droidPos)]
    uniquePaths = backtrack(map, droidPos, directions, currentpath, inputs, outputs, notify)
    
    
    # draw path on map
    #for pos in uniquePaths[0]:
    #    map[pos[0],pos[1]] = '*'
    #map[uniquePaths[0][0][0],uniquePaths[0][0][0]] = 'O'
    #map[uniquePaths[0][-1][0],uniquePaths[0][-1][0]] = 'O'
    showMap(map, droidPos)
    print("Result Part 1:", len(uniquePaths[0])-1)
    

    minutes = fillOxygen(map, directions)
    print("Result Part 2:", minutes + 1)
  



if __name__ == '__main__':
    #freeze_support()
    run()
