from __future__ import division 
import numpy as np

file = open('input_3.txt', 'r')

def readWire(file):
	wire = file.readline()
	wire = wire[:-1]
	wire = wire.split(',')
	return wire
	
wire1 = readWire(file)
wire2 = readWire(file)




def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 

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
    if is_between(a1, intersection, a2) and is_between(b1, intersection, b2):
        return intersection
    else:
        return False




# def getBoundingBox(startPos, currentPos, gridSize, direction, steps):
		
	# if direction == 'R':
		
		# if currentPos[1] + steps > gridSize[1]-1:
			# paddingRight = currentPos[1] + steps - (gridSize[1]-1)
			# gridSize[1] += paddingRight
			# currentPos[1] += steps
		

			
	# if direction == 'L':
			
		# if currentPos[1] - steps < 0:
			# paddingLeft = abs(currentPos[1] - steps)
			
			# gridSize[1] += paddingLeft
			# currentPos[1] += paddingLeft
			# startPos[1] += paddingLeft
			
			
			# # coordiniate system change because of padding
			# currentPos[1] -= steps

			
		
			
	# if direction == 'D':
	
	
		# if currentPos[0] + steps > gridSize[0]-1:
			# paddingDown = currentPos[0] + steps - (gridSize[0]-1)
			# gridSize[0] += paddingDown
			# currentPos[0] += steps
			
		
	# if direction == 'U':
		
		
		# if currentPos[0] - steps < 0:
			# paddingUp = abs(currentPos[0] - steps)
			# gridSize[0] += paddingUp
			# currentPos[0] += paddingUp
			# startPos[0] += paddingUp
			
			
			# # coordiniate system change because of padding
			
			# currentPos[0] -= steps
			

	
	
	# return gridSize, currentPos, startPos


# def getBoundingBoxWire(startPos, currentPos, gridSize, wire):
	# count = 0
	# for instruction in wire:
		# direction = instruction[0]
		# steps = int(instruction[1:])
		# print(count, "/", len(wire), ": ", steps, " in ", direction, "shape: ", gridSize)

		# gridSize, currentPos, startPos = getBoundingBox(startPos, currentPos, gridSize, direction, steps)
		
		# count += 1
		
		

	# return gridSize, startPos



		
	

def getLineSegments(currentPos, wire):
	count = 0
	segments = []
	sumSteps = 0
	for instruction in wire:
		direction = instruction[0]
		steps = int(instruction[1:])
		# print(count, "/", len(wire), ": ", steps, " in ", direction, "shape: ", grid.shape)
		
		
		
		if direction == 'R':
			
			segments.append((currentPos.copy(), [currentPos[0], currentPos[1]+steps], sumSteps))
			currentPos[1] += steps
			
			

			
		if direction == 'L':
			
			
			segments.append((currentPos.copy(), [currentPos[0], currentPos[1]-steps], sumSteps))
			currentPos[1] -= steps
			
			
		if direction == 'D':
		
		
			segments.append((currentPos.copy(), [currentPos[0]+steps, currentPos[1]], sumSteps))
			currentPos[0] += steps
			
			
			
		if direction == 'U':
			
			
			segments.append((currentPos.copy(), [currentPos[0]-steps, currentPos[1]], sumSteps))
			currentPos[0] -= steps
			
		sumSteps += steps
			
		count += 1
			
		
	return segments, currentPos
	
	
	

	
	
	
startPos = [0,0]
# grid = np.asarray([[ord('o')]])
# grid= draw(startPos, currentPos, grid, 'R', 5, '1')
# grid= draw(startPos, currentPos, grid, 'U', 6, '1')
# print(startPos)
# drawGrid(grid)
bb = [1, 1]


# currentPos = startPos.copy()

# bb, currentPos, startPos = getBoundingBox(startPos, currentPos, bb, 'U', 11)
# bb, currentPos, startPos = getBoundingBox(startPos, currentPos, bb, 'R', 4)


# print(bb, currentPos, startPos)
# import sys
# sys.exit(0)
# print("startpos:", startPos, " in grid of size ", bb)
# currentPos = startPos.copy()
# bb, startPos = getBoundingBoxWire(startPos, currentPos, bb, wire1)

# print("after wire 1 startpos:", startPos, " in grid of size ", bb)
# currentPos = startPos.copy()
# bb, startPos = getBoundingBoxWire(startPos, currentPos, bb, wire2)
# print("after wire 2 startpos:", startPos, " in grid of size ", bb)




startPos = [0, 0]


currentPos = startPos.copy()
segments1, pos = getLineSegments( currentPos, wire1)

currentPos = startPos.copy()
segments2, pos = getLineSegments(currentPos, wire2)



# Part 1
minDist = 999999999999
for segment1 in segments1:
	for segment2 in segments2:
		intersect = seg_intersect(np.array(segment1[0]), np.array(segment1[1]),np.array(segment2[0]), np.array(segment2[1]))
		if intersect is not False:
			dist = abs(intersect[0] - startPos[0]) + abs(intersect[1] - startPos[1])
			if dist < minDist and dist > 0:
				minDist = dist
				# print("min dist:", minDist)
				# print("inmtersect:", intersect)
				# print(np.array(segment1[0]), np.array(segment1[1]),np.array(segment2[0]), np.array(segment2[1]))
			# print("intersection:", intersect)
print("Part 1 Result:", minDist)


# min distance in steps
minDist = 999999999999
for segment1 in segments1:
	for segment2 in segments2:
		intersect = seg_intersect(np.array(segment1[0]), np.array(segment1[1]),np.array(segment2[0]), np.array(segment2[1]))


		if intersect is not False:
			d1 = distance(segment1[0], intersect)
			d2 = distance(segment2[0], intersect)
			dist = segment1[2] + segment2[2] + d1  + d2
			if dist < minDist and dist > 0:
				minDist = dist
				# print("min dist:", minDist)
				# print("inmtersect:", intersect)
				# print(np.array(segment1[0]), np.array(segment1[1]),np.array(segment2[0]), np.array(segment2[1]))
			# print("intersection:", intersect)
print("Result:", minDist)


