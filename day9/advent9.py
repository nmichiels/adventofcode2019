import numpy as np

from intcode import runProgram



def run():
    instructions = np.loadtxt('input_9.txt', delimiter=',', dtype='int64')
    code = instructions.copy()

    from multiprocessing import Process, Queue

    inputs = Queue()
    outputs = Queue()

    process = Process(target = runProgram, args=(code, inputs, outputs))
    process.start()

    # part 1
    inputs.put(1)

    # part 2
    #inputs.put(2)


    process.join()
    
    while not outputs.empty():
        print("Output: ", outputs.get())


if __name__ == '__main__':
    #freeze_support()
    run()
