import numpy as np

file = open('input_10.txt', 'r')

def split(word): 
    return [char for char in word]  

map = []
for line in file:
    line = split(line)
    line = line[:-1]
    map.append(line)


map = np.asarray(map)


def showMap(map):
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            print(map[i,j], end='')
        print('')


showMap(map)



def findOccurences(map, value):
    occurences = []
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i,j] == value:
                occurences.append((i,j))
    return occurences





def distance(a,b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def is_between(a,c,b):
    #return distance(a,c) + distance(c,b) == distance(a,b)
    epsilon = 0.000001
    return -epsilon < (distance(a, c) + distance(c, b) - distance(a, b)) < epsilon




#def findOcclusions(baseStationPosition, asteroidsPositions):
#    occlusions = []
#    for possibleOccludedAsteroidPosition in asteroidsPositions:
#        if possibleOccludedAsteroidPosition == baseStationPosition:
#            continue


#        for astroidPosition in asteroidsPositions:
#            if astroidPosition == baseStationPosition or astroidPosition == possibleOccludedAsteroidPosition:
#                continue


#            if (is_between(baseStationPosition, astroidPosition, possibleOccludedAsteroidPosition)):
#                #print(astroidPosition, " is occluding ", possibleOccludedAsteroidPosition, " for ", baseStationPosition)
#                occlusions.append(possibleOccludedAsteroidPosition)
#    occlusions = list(dict.fromkeys(occlusions)) # remove duplicates
#    return occlusions


def getVisibleAsteroids(baseStationPosition, asteroidsPositions):
    visibleAstroids = []
    for possibleOccludedAsteroidPosition in asteroidsPositions:
        if possibleOccludedAsteroidPosition == baseStationPosition:
            continue


        unobstructed = True
        for astroidPosition in asteroidsPositions:
            if astroidPosition == baseStationPosition or astroidPosition == possibleOccludedAsteroidPosition:
                continue


            if (is_between(baseStationPosition, astroidPosition, possibleOccludedAsteroidPosition)):
                #print(astroidPosition, " is occluding ", possibleOccludedAsteroidPosition, " for ", baseStationPosition)
                unobstructed = False
                break

        if (unobstructed):
            visibleAstroids.append(possibleOccludedAsteroidPosition)

    return visibleAstroids
  




asteroidsPositions = findOccurences(map, '#')


runPart1 = True
if runPart1:
    occlusionsMap = map.copy()
    positionWithMaxDetectedAsteroids = None
    maxDetected = 0

    print("num", len(asteroidsPositions))
    for p in range(len(asteroidsPositions)):
        baseStationPosition = asteroidsPositions[p]
        #occlusions = findOcclusions(baseStationPosition, asteroidsPositions)
        #numDetectedAsteroids = len(asteroidsPositions)- 1 - len(occlusions) #ignore own position
        detectedAsteroids = getVisibleAsteroids(baseStationPosition, asteroidsPositions)
        numDetectedAsteroids = len(detectedAsteroids)
        occlusionsMap[baseStationPosition] = numDetectedAsteroids

        if numDetectedAsteroids > maxDetected:
            maxDetected = numDetectedAsteroids
            positionWithMaxDetectedAsteroids = baseStationPosition
    


    print('\n')
    showMap(occlusionsMap)
    print("Result: Position", tuple(reversed(positionWithMaxDetectedAsteroids)), "with", maxDetected, "detected asteroids")



# part 2
center = positionWithMaxDetectedAsteroids #(11,19)
print("Position of laser = ", center)
laserMap = map.copy()
laserMap[center] = 'X'
showMap(laserMap)



def getSortedAngles(detectedAsteroids):

    import math 

    def normalize(v):
        norm = np.linalg.norm(v)
        if norm == 0: 
           return v
        return v / norm

    angles = []
    for astroid in detectedAsteroids:

        dir = [center[0] - astroid[0], astroid[1]-center[1] ]
        dir = normalize(dir)

        angle = math.atan2(dir[1],dir[0]) 
        if (angle < 0.0):
            angle += 2.0*math.pi

        angles.append((astroid, angle))

    angles = sorted(angles, key=lambda x: x[1])

    return angles


numToVaporize = 200

numVaporized = 0
output = None
print("Lasermap before")
showMap(laserMap)
while numVaporized < numToVaporize:

    asteroidsPositions = findOccurences(laserMap, '#')
    detectedAsteroids = getVisibleAsteroids(center, asteroidsPositions)
    sortedAsteroidsBasedOnAngle = getSortedAngles(detectedAsteroids)


    while len(sortedAsteroidsBasedOnAngle) > 0:
        angle = sortedAsteroidsBasedOnAngle.pop(0)
        laserMap[angle[0]] = 'V'
        # vaporize this asteroid


        numVaporized += 1

        if numVaporized == numToVaporize:
            output = angle[0]
            break



print("Result positon: ", output, " --> ", output[1]*100 + output[0])

print("Resulting Map")
showMap(laserMap)
