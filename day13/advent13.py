import numpy as np
import time
from intcode import runProgram
from multiprocessing import Process, Queue
import os

def showMap(map, score = 0, frame = 0):

    os.system('clear')  # For Linux/OS X
    print('')
    print("SCORE:", score)
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i,j] == 'W':
                print(' ', end='')
            else:
                print(map[i,j], end='')
        print('')
    print('')
    print('Frame', frame)





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
    prevPosBall = (0,0)
    while True:
        while notifyOnInput.empty():
            while not notify.empty():

                out = notify.get()
                if out == -1:
                    print("the end")
                    running = False
                    break

                x = outputs.get()
                out = notify.get()
                y = outputs.get()
                out = notify.get()
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
            if not running:
                break
        if not running:
                break
        showMap(map, score, frame)
        # if not running:
        #     break
        if not notifyOnInput.empty():
            # print("joystick", frame)


            positionBall = np.where(map == 'O')
            positionPaddle = np.where(map == '-')
            dir = 0
            if len(positionBall[0]) > 0 and len(positionPaddle[0]) > 0:
                
                positionBall = (positionBall[0][0],positionBall[1][0])
                positionPaddle = (positionPaddle[0][0],positionPaddle[1][0])

                # print(positionBall, "vs", positionPaddle)
                
                if positionBall[1] < positionPaddle[1]:
                    dir = -1
                if positionBall[1] > positionPaddle[1]:
                    dir = 1  

                prevPosBall = positionBall
      
            notifyOnInput.get()
            time.sleep(0.0)
            inputs.put(dir)
            
            frame += 1
    
       
    print("end")
    showMap(map, score, frame)  
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
