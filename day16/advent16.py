import numpy as np



def runPart1():
    signal = '59772698208671263608240764571860866740121164692713197043172876418614411671204569068438371694198033241854293277505547521082227127768000396875825588514931816469636073669086528579846568167984238468847424310692809356588283194938312247006770713872391449523616600709476337381408155057994717671310487116607321731472193054148383351831456193884046899113727301389297433553956552888308567897333657138353770191097676986516493304731239036959591922009371079393026332649558536888902303554797360691183681625604439250088062481052510016157472847289467410561025668637527408406615316940050060474260802000437356279910335624476330375485351373298491579364732029523664108987'
    signal = [x for x in signal ]
    signal = [int(x) for x in signal ]
    pattern = [0, 1, 0, -1]


    def preprocessPatterns(signal, pattern):
        patterns = []
        for digit in range(len(signal)):
            currentPattern = np.repeat(pattern, digit+1)
            currentPattern = np.tile(currentPattern, int(np.ceil(len(signal)/(len(currentPattern)-1))))
            currentPattern = currentPattern[1:len(signal)+1] # skip first element in patter
            patterns.append([currentPattern])
    
        return patterns

    def applyPhase(signal, pattern):
        newSignal = signal.copy()
        for digit in range(len(signal)):
            sum = np.sum(np.multiply(signal,  digitPatterns[digit]))
            #select ones digit of sum
            newSignal[digit] = int(str(sum)[-1])
    
        return newSignal

    digitPatterns = preprocessPatterns(signal, pattern)

    for i in range(1):
        signal = applyPhase(signal, pattern)
        outputAsStr = [str(x) for x in signal ]
        print("End of phase", i, ": First 8 digits", ''.join(outputAsStr[:8]))
    
    outputAsStr = [str(x) for x in signal ]
    print("Result part 1: First 8 digits", ''.join(outputAsStr[:8]))


def runPart2():
    signal = '59772698208671263608240764571860866740121164692713197043172876418614411671204569068438371694198033241854293277505547521082227127768000396875825588514931816469636073669086528579846568167984238468847424310692809356588283194938312247006770713872391449523616600709476337381408155057994717671310487116607321731472193054148383351831456193884046899113727301389297433553956552888308567897333657138353770191097676986516493304731239036959591922009371079393026332649558536888902303554797360691183681625604439250088062481052510016157472847289467410561025668637527408406615316940050060474260802000437356279910335624476330375485351373298491579364732029523664108987'
    signal = [x for x in signal ]
    signal = [int(x) for x in signal ]
    signal = np.tile(signal, 10000)
    pattern = [0, 1, 0, -1]

   
    def applyPhase(signal, pattern):
        # pattern is always 1, so result is sum of all values after that digit
        # we calculate sum on the go by staring at the last digit
        sum = 0
        for digit in reversed(range(0, len(signal))):
            sum += signal[digit]
            signal[digit] = int(str(sum)[-1])            #select ones digit of sum


    # get offset and covert to int
    offset = signal[0:7]
    offset = [str(x) for x in offset ]
    offset = int(''.join(offset))


    # Because offset > len(signal)/2 --> all values in pattern before offset digit are zero and all after are 1
    # As a result we can simplify input length and phase calculations
    print("Reduce input from", len(signal), "to", len(signal)-offset)
    signal = signal[offset:]

  
    for i in range(100):
        applyPhase(signal, pattern)
        outputAsStr = [str(x) for x in signal[0:8] ]
        print("End of phase", i+1, ": First 8 digits", ''.join(outputAsStr))
    
    outputAsStr = [str(x) for x in signal[0:8] ]
    print("Result part 2: resulting 8 digits at offset", offset, ": ",''.join(outputAsStr))


runPart1()
runPart2()