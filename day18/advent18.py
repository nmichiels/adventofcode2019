import numpy as np


def showMap(map):
    print('')
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            print(map[i,j], end='')
        print('')
    print('')






def findShortestPath(currentPos, targetLetter, map, visitedMask, directions, path):
    uniquePaths = []

    visitedMask[currentPos[0],currentPos[1]] = True

    for i in range(0,4):
        direction = directions[i]
        newPos = np.add(currentPos, direction)

        value = map[newPos[0],newPos[1]]

        # if blocked by wall or already been, stop path here and continue to other direction
        if visitedMask[newPos[0],newPos[1]] == True or value == '#':
            continue

        # if passing a door (between A and Z), stop path here and continue into other direction
        if ord(value) >= 65 and ord(value) < 65+26:
            continue

        if map[newPos[0],newPos[1]] == targetLetter:
            uniquePaths += [path + [newPos]]
            continue

        newPath = path + [newPos]
        uniquePaths += findShortestPath(newPos, targetLetter, map, visitedMask, directions, newPath)
        
        


    return uniquePaths



def gatherKeys(map, directions, currentPos, possiblekeys, keyPath, steps, depth, currentShortest):
    uniquePaths = []

    for key in possiblekeys:
        visitedMask = np.full(map.shape, False, dtype=bool)
        shortestPath = findShortestPath(currentPos, key, map, visitedMask, directions, [])
        shortestPath.sort(key = lambda x: len(x)) 

        if len(shortestPath) > 0:
            shortestPath = shortestPath[0]

            newKeys = np.delete(possiblekeys, np.argwhere(np.asarray(possiblekeys) == key))
            
            newPos = shortestPath[-1]
            if depth < 3:
                print("Handling key", key, " depth: ", depth, " new keys:", newKeys)

            newSteps = steps.copy()
            newSteps[0] += len(shortestPath)

            # prune path if it is already longer than current shortest path
            if len(currentShortest) > 0 and newSteps[0] >= currentShortest[0][1]:
                #print("SKIPPING")
                continue

            if len(newKeys) > 0:
                newKeyPath = keyPath +  [(key, len(shortestPath))]


                
             
                #remove door from map, because you have key at hand

                newMap = np.copy(map)
 

                doorPos = np.where(newMap == chr(ord(key)-32))
                if len(doorPos[0]) > 0:
                    newMap[doorPos[0][0],doorPos[1][0]] = '|'
               
                
                
           
               
                uniquePaths += gatherKeys(newMap, directions, newPos, newKeys, newKeyPath, newSteps, depth + 1, currentShortest)

        
            else:
               
                uniquePath = keyPath + [(key, len(shortestPath))]
            
                sum = 0
                for p in uniquePath:
                    sum += p[1]
                print("Found solution with length", sum, ": ", uniquePath)
                uniquePaths.append((uniquePath,sum))
                if len(currentShortest) == 0:
                    currentShortest.append((uniquePath,sum))
                elif sum < currentShortest[0][1]:
                    # found new shortest solution
                    currentShortest.pop(0)
                    currentShortest.append((uniquePath,sum, newSteps[0]))
                return uniquePaths

            
            #print("Path to", key, ":", shortestPath)
        #else:
            #print("Path ", key, ": blocked")


    return uniquePaths



def run():
    file = open('input_18.txt', 'r')

    def split(word): 
        return [char for char in word]  

    map = []
    for line in file:
        line = [char for char in line]  
        line = line[:-1]
        map.append(line)

    directions = [[-1,0],[1,0],[0,-1],[0,1]]

    map = np.asarray(map)
    showMap(map)

    # A starts from 65
    # a starts from 97
    startLetter = 97
    letterOffset = 32
    
    
    startPos = np.reshape(np.where(map == '@'), (2))
    #targetPos = np.reshape(np.where(map == 'b'), (2))
   
    keys = [chr(key) for key in range(ord('a'),ord('p')+1)]
    print("KEYS:", keys)

    currentShortest = []
    steps = [0]
    paths = gatherKeys(map.copy(), directions, startPos, keys.copy(), [], steps, 0,currentShortest)
    paths.sort(key = lambda x: x[1]) 
    print(currentShortest)
    print("Result part 1: ", paths[0][1])
    #for key in keys:
    #    visitedMask = np.full(map.shape, False, dtype=bool)
    #    shortestPath = findShortestPath(startPos, key, map, visitedMask, directions, [])
    #    shortestPath.sort(key = lambda x: len(x)) 

    #    if len(shortestPath) > 0:
    #        shortestPath = shortestPath[0]
    #        print("Path to", key, ":", shortestPath)
    #    else:
    #        print("Path ", key, ": blocked")


if __name__ == '__main__':
    #freeze_support()
    run()
