import numpy as np
import time
from intcode import runProgram
from multiprocessing import Process, Queue
import os

def showMap(map, score = 0, frame = 0):

    os.system('clear')  # For Linux/OS X
    print('')
    print("SCORE:", score)

    for j in range(41):
        if int(j / 10) != 0:
            map[23,j] = j / 10
    for j in range(41):
        map[24,j] = j % 10
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i,j] == 'W':
                print(' ', end='')
            else:
                print(map[i,j], end='')
        print('')
    print('')
    print('Frame', frame)
    print(" ", flush=True)





def runPart1():
    instructions = np.loadtxt('input_13.txt', delimiter=',', dtype='int64')
    code = instructions.copy()

    map = np.chararray((42, 42))
    map[:] = 'W'
    map = map.astype('unicode')

    
    inputs = Queue()
    outputs = Queue()
    notify = Queue() #used for notification of output or end of program
    notifyOnInput = Queue()

    process = Process(target = runProgram, args=(code, inputs, outputs, notify,notifyOnInput))
    process.start()


    while True:
        out = notify.get()
        if out == -1:
            break

        # out = notify.get()
        x = outputs.get()
        out = notify.get()
        y = outputs.get()
        out = notify.get()
        tileId = outputs.get()

        if x == -1 and y == 0:
            print("Score: ", tileId)

        if tileId == 0:
            map[y,x] = 'W'
        elif tileId == 1:
            map[y,x] = 'X'
        elif tileId == 2:
            map[y,x] = '.'
        elif tileId == 3:
            map[y,x] = '-'
        elif tileId == 4:
            map[y,x] = 'O'   
        else:
            print("Unknown Tile ID")

        # map[x,y] = tileId
        # print("drawing", tileId, "at", x, ",", y)
       
    print("end")
    showMap(map)  
    # part 1
    unique, counts = np.unique(map, return_counts=True)
    occ = dict(zip(unique, counts))
    # if 0 in occ:
    #     del occ[0]
    print(occ)
    print("Result Part 1:", occ['.'])  
    

# def showMap(map):
#     print('\n')
#     for row in range(map.shape[0]):
#         for col in range(map.shape[1]):
#             print(map[row,col], end='')
#         print('')

def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def distance(a,b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def is_between(a,c,b):
    return distance(a,c) + distance(c,b) == distance(a,b)

def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)

	

    num = np.dot( dap, dp )
    if (denom.astype(float) == 0.0):
        return False

    intersection = (num / denom.astype(float))*db + b1
    return intersection



def runPart2():
    instructions = np.loadtxt('input_13.txt', delimiter=',', dtype='int64')
    code = instructions.copy()

    # set memory address 0 to 2
    code[0] = 2

    map = np.chararray((42, 42))
    map[:] = 'W'
    map = map.astype('unicode')

    
    inputs = Queue()
    outputs = Queue()
    notify = Queue() #used for notification of output or end of program
    notifyOnInput = Queue()

    process = Process(target = runProgram, args=(code, inputs, outputs, notify,notifyOnInput))
    process.start()

    frame = 0
    score = 0
    running = True
    prevPosBall = None#np.array([0,0])
    prevPosPaddle = None
    countError = 0
    while True:
     
        
        
        # notifyOnInput.get()
        # inputs.put(1)

        # notifyOnInput.get()


        while True:
    
            # out = notify.get()
            # if out == -1:
            #     print("the end")
            #     running = False
            #     break

            x = outputs.get()

            # check if input is required
            if x == "done":
                break
            # out = notify.get()
            y = outputs.get()
            # out = notify.get()
            tileId = outputs.get()
            # print("drawing", tileId, "at", y, ",", x)
            if x == -1 and y == 0:
                score = tileId
                print("Score: ", score)

            if tileId == 0:
                map[y,x] = 'W'
            elif tileId == 1:
                map[y,x] = 'X'
            elif tileId == 2:
                map[y,x] = '.'
            elif tileId == 3:
                map[y,x] = '-'
            elif tileId == 4:
                map[y,x] = 'O'   
            else:
                print("Unknown Tile ID")
        
            # map[x,y] = tileId
            # 
        # notifyOnInput.get()
        if not running:
            print("STOP")
            break

        # time.sleep(0.1)
        showMap(map, score, frame)
       
        
        positionBall = np.where(map == 'O')
        positionPaddle = np.where(map == '-')
        dir = 0

        if not outputs.empty():
            print("ERROR outputs BALL")
            countError += 1
            return
        if len(positionBall[0]) == 0:
            # print("ERROR PREDICTING BALL")
            countError += 1
            positionBall = prevPosBall
            return
        else:
            positionBall = np.array([positionBall[0][0],positionBall[1][0]])
            
        if len(positionPaddle[0]) == 0:
            # print("ERROR PREDICTING PADDLER")
            countError += 1
            positionPaddle = prevPosPaddle
            return
        else:
            positionPaddle = np.array([positionPaddle[0][0],positionPaddle[1][0]])

        
        
        

        if prevPosBall is None:
            prevPosBall = positionBall

        if prevPosPaddle is None:
            prevPosPaddle = positionPaddle

        

        print("num errors: ", countError)
        # if prevPosBall[0] == positionBall[0] and prevPosBall[1] == positionBall[1]:
        #     pass
        # else:
        #     dir = positionBall - prevPosBall
        #     trackedPos = positionBall
        #     while trackedPos[0] != positionPaddle[0]:
        #         newPos = trackedPos + dir
        #         if map[newPos[0],newPos[1]] == 'X':
        #             print("hit a wall")
        #             dir = -dir
        #             newPos = trackedPos + dir

        # check if hit on paddle
        if positionBall[0] + 1 == positionPaddle[0] and positionBall[1] == positionPaddle[1]:
            intersectGround = False
            dir = 0
            # direction = positionBall - prevPosBall
            # if direction[1] > 0:
            #     dir = -1
            # elif direction[1] < 0:
            #     dir = 1
            # else:
            #     dir = 0

        else:
            if positionBall[1] < positionPaddle[1]:
                dir = -1
            elif positionBall[1] > positionPaddle[1]:
                dir = 1
            else:
                # dir = 0
                if positionBall[1] > prevPosBall[1]:
                    dir = 1  
                elif positionBall[1] < prevPosBall[1]:
                    dir = -1  
                else:
                    dir = 0


        # if intersectGround is not False:
        #     if intersectGround[1] < positionPaddle[1]:
        #         dir = -1
        #     elif intersectGround[1] > positionPaddle[1]:
        #         dir = 1  
        #     else:
        #         if positionBall[1] > prevPosBall[1]:
        #             dir = 1  
        #         elif positionBall[1] < prevPosBall[1]:
        #             dir = -1  
        #         else:
        #             dir = 0

        # else:
        #     if positionBall[1] < positionPaddle[1]:
        #         dir = -1
        #     elif positionBall[1] > positionPaddle[1]:
        #         dir = 1
        #     else:
        #         if positionBall[1] > prevPosBall[1]:
        #             dir = 1  
        #         elif positionBall[1] < prevPosBall[1]:
        #             dir = -1  
        #         else:
        #             dir = 0
        # else:
        #     # predict dir
        #     if positionBall[1] > prevPosBall[1]:
        #         dir = 1  
        #     if positionBall[1] < prevPosBall[1]:
        #         dir = -1


        # if down and intersect is not False:
        #     if intersect[1] < positionPaddle[1]:
        #         dir = -1
        #     if intersect[1] > positionPaddle[1]:
        #         dir = 1  
        # else:
        #     if positionBall[1] < positionPaddle[1]:
        #         dir = -1
        #     if positionBall[1] > positionPaddle[1]:
        #         dir = 1  

        prevPosBall = positionBall
        prevPosPaddle = positionPaddle
    
        # notifyOnInput.get()
        
        # time.sleep(1)
        inputs.put(dir)
        
        frame += 1
    
       
    print("end")
    # showMap(map, score, frame)  
    # part 1
    unique, counts = np.unique(map, return_counts=True)
    occ = dict(zip(unique, counts))
    # if 0 in occ:
    #     del occ[0]
    print(occ)
    print("Result Part 1:", occ['.'])  

# def runPart2():
#     import os

#     instructions = np.loadtxt('input_13.txt', delimiter=',', dtype='int64')
#     code = instructions.copy()
    
#     # set memory address 0 to 2
#     # code[0] = 2
#     map = np.chararray((42, 42))
    
#     map[:] = ' '
#     map = map.astype('unicode')

    
#     inputs = Queue()
#     outputs = Queue()
#     notify = Queue() #used for notification of output or end of program
#     notifyOnInput = Queue()

#     process = Process(target = runProgram, args=(code, inputs, outputs, notify, notifyOnInput))
#     process.start()
    
#     minX = 999999
#     maxX = 0
#     minY = 999999
#     maxY = 0
#     showMap(map)
#     frame = 0
#     running = True
#     while True:
        
#         # out = notify.get()    
#         # if out == -1:
#         #     break            
#         while notifyOnInput.empty():
#             while not outputs.empty():
                
#                 out = notify.get()
#                 x = outputs.get()
#                 out = notify.get()
#                 y = outputs.get()
#                 out = notify.get()
#                 tileId = outputs.get()


#                 if x == -1 and y == 0:
#                     print("Score: ", tileId)

#                 if tileId == 0:
#                     map[y,x] = ' '
#                 elif tileId == 1:
#                     map[y,x] = 'X'
#                 elif tileId == 2:
#                     map[y,x] = '.'
#                 elif tileId == 3:
#                     map[y,x] = '-'
#                 elif tileId == 4:
#                     map[y,x] = 'O'   
#                 else:
#                     print("Unknown Tile ID")
#                 print("drawing", tileId, "at", x, ",", y)
#             print("done")
#             if not notify.empty():
#                 out = notify.get()    
#                 if out == -1:
#                     running = False
#                     print("break")
#                     break    
        
#         showMap(map)
#         if not running:
#             break

        

#         # map[x,y] = tileId
#         # print("drawing", tileId, "at", x, ",", y)
#         if not notifyOnInput.empty():
#             showMap(map)
#             print("joystick", frame)
#             notifyOnInput.get()
#             inputs.put(1)
            
#             frame += 1

            
           
#     print("end")
          
#     # part 1
#     unique, counts = np.unique(map, return_counts=True)
#     occ = dict(zip(unique, counts))
#     # if 0 in occ:
#     #     del occ[0]
#     print(occ)
#     print("Result Part 2:", occ['.'])  
    
    



  


        


    # process.join()
    
    # while not outputs.empty():
    #     print("Output: ", outputs.get())


if __name__ == '__main__':
    #freeze_support()
    # runPart1()
    runPart2()
