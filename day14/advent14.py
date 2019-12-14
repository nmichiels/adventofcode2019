import numpy as np




def parseReaction(line): 
    parts = line.split(" => ")

    reactions = []
    for part in parts:
        reactions = reactions + part.split(', ')


    chemicals = []
    for reaction in reactions:

        c = reaction.split(' ')
        count = int(c[0])
        chemical = c[1]
        chemicals.append((chemical, count))

    outputChem = chemicals[-1]
    inputChems = chemicals[:-1]


    #print(outputChem)
    
    return inputChems, outputChem


def produce(outputChemical, amount, reactions, counts):
    (inputs, outputAmount) = reactions[outputChemical]

    for (requiredChem, requiredAmount) in inputs:
        if requiredChem == 'ORE':
            counts['ORE'] += requiredAmount
            continue

        while counts[requiredChem] < requiredAmount:
            produce(requiredChem, requiredAmount, reactions, counts)

        # use input chemical
        counts[requiredChem] -= requiredAmount


    # at this point all input chemicals have been used an the output chemical is produced
    counts[outputChemical] += outputAmount
    #print("Produced %d of %s"%(outputAmount,outputChemical))

          
  

def run():
    file = open('input_14.txt', 'r')


    reactions = {}
    counts = {}
    counts['ORE'] = 0
    for line in file:
        inputs, output = parseReaction(line[:-1])
        reactions[output[0]] = (inputs, output[1])
        counts[output[0]] = 0

    
    part1 = False
    
    if part1:
        produce('FUEL', 1, reactions, counts)
        print("Result Part 1: Number of ORE's required: ", counts['ORE'])

    else:
        while counts['ORE'] < 1000000000000:
            produce('FUEL', 1, reactions, counts)
            if counts['FUEL'] % 1000 == 0:
                print(counts['FUEL'] , "==>", counts['ORE'] )
        print("Num ORE's used:", counts['ORE'])
        print("Result Part2: Num FUELs produced:", counts['FUEL'])
    
    





if __name__ == '__main__':
    run()
