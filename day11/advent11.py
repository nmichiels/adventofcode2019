import numpy as np

from intcode import runProgram
from multiprocessing import Process, Queue


def showMap(map):
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            print(map[i,j], end='')
        print('')



def run():
    instructions = np.loadtxt('input_11.txt', delimiter=',', dtype='int64')
    code = instructions.copy()

    map = np.zeros((101, 151) ,dtype=int)
    map[:] = 0

    robotPos = (int(map.shape[0] / 2.0),int(map.shape[1] / 2.0))


    part2 = True
    if part2:
        map[robotPos] = 1 # set starting position to white
    else:
        map[robotPos] = 0 # set starting position to black



    directions = [(-1,0),(0,1),(1,0),(0,-1)]
    currentDir = 0

    # use mask to see where a color has been changed
    paintedMask = np.copy(map)


    
    inputs = Queue()
    outputs = Queue()
    notify = Queue() #used for notification of output or end of program

    process = Process(target = runProgram, args=(code, inputs, outputs, notify))
    process.start()


    while True:
        if map[robotPos] == 0: # black pixel
            inputs.put(0)
        else:
            inputs.put(1)

        out = notify.get()
        if out == -1:
            break
        else:
            out = notify.get()
            color = outputs.get()
            if color == 0:
                map[robotPos] = 0
            elif color == 1:
                map[robotPos] = 1
            else:
                print("error color")
            paintedMask[robotPos] = 2

            dir = outputs.get()
            if dir == 0:
                currentDir -= 1
                if currentDir < 0:
                    currentDir += len(directions)
            elif dir == 1:
                currentDir += 1
                currentDir = currentDir % len(directions)
            else:
                print("error dir")

            # move robot into current direction
            robotPos = (robotPos[0] + directions[currentDir][0], robotPos[1] + directions[currentDir][1])

          
            
    if part2:
        import matplotlib.pyplot as plt
        imgplot = plt.imshow(map.astype(dtype='float'))
        plt.show()
    else:
        unique, counts = np.unique(paintedMask, return_counts=True)
        occ = dict(zip(unique, counts))
        print("Result Part 1:", occ[2])  
    

    
    




  


        

    process.join()
    
    while not outputs.empty():
        print("Output: ", outputs.get())


if __name__ == '__main__':
    #freeze_support()
    run()
