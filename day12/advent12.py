import numpy as np




def addToHash(hashmap, positions, velocities):

   p = []
   for position in positions:
      p.append(position[0])
      p.append(position[1])
      p.append(position[2])
   for velocity in velocities:
      p.append(velocity[0])
      p.append(velocity[1])
      p.append(velocity[2])
   # print(tuple(p))
   
   key = hash(tuple(p))
   

   if key in hashmap:
      return True
   else:
      hashmap[key] = 1
      return False
   # print("hash:", hash(tuple(p)))
   
def runPart1():
   # positions = []
   # positions.append([-19,-4,2])
   # positions.append([-9,8,-16])
   # positions.append([-4,5,-11])
   # positions.append([1,9,-13])
   positions = []
   positions.append([-1,0,2])
   positions.append([2,-10,-7])
   positions.append([4,-8,8])
   positions.append([3,5,-1])
   
   
   velocities = []
   velocities.append([0,0,0])
   velocities.append([0,0,0])
   velocities.append([0,0,0])
   velocities.append([0,0,0])


   pairs = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
   
   def getTotalEnergy(positions, velocities):
       # potential energy
       total = 0

       for i in range(len(positions)):
           pot = 0
           kin = 0
           for c in range(3):
               pot += abs(positions[i][c])
               kin += abs(velocities[i][c])
           total += pot * kin
       return total


   def printPositions(t, positions, velocities):
       print("After %d steps:"%t)
       for i in range(len(positions)):
           print("pos=<x= %d, y= %d, z= %d>, vel=<x= %d, y= %d, z= %d>"%(positions[i][0],positions[i][1],positions[i][2],velocities[i][0],velocities[i][1],velocities[i][2]))
       print("")


   printPositions(0, positions, velocities)
   for t in range(1000):
       # calculate new velocities
       for pair in pairs:
           for c in range(3):
               if positions[pair[0]][c] < positions[pair[1]][c]:
                   velocities[pair[0]][c] += 1
                   velocities[pair[1]][c] -= 1
               elif positions[pair[0]][c] > positions[pair[1]][c]:
                   velocities[pair[0]][c] -= 1
                   velocities[pair[1]][c] += 1
               else:
                   pass
        
       # apply velocities
       for i in range(len(positions)):
           for c in range(3):
               positions[i][c] += velocities[i][c]

       if (t+1) %100 == 0:    
           printPositions(t+1, positions, velocities)

   print("Total energy:", getTotalEnergy(positions, velocities))
   
   
  
def runPart2():
   positions = []
   positions.append([-19,-4,2])
   positions.append([-9,8,-16])
   positions.append([-4,5,-11])
   positions.append([1,9,-13])
   # positions = []
   # positions.append([-1,0,2])
   # positions.append([2,-10,-7])
   # positions.append([4,-8,8])
   # positions.append([3,5,-1])
   
   velocities = []
   velocities.append([0,0,0])
   velocities.append([0,0,0])
   velocities.append([0,0,0])
   velocities.append([0,0,0])


   pairs = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
   hashmap = {}
   
   def getTotalEnergy(positions, velocities):
       # potential energy
       total = 0

       for i in range(len(positions)):
           pot = 0
           kin = 0
           for c in range(3):
               pot += abs(positions[i][c])
               kin += abs(velocities[i][c])
           total += pot * kin
       return total


   def printPositions(t, positions, velocities):
       print("After %d steps:"%t)
       for i in range(len(positions)):
           print("pos=<x= %d, y= %d, z= %d>, vel=<x= %d, y= %d, z= %d>"%(positions[i][0],positions[i][1],positions[i][2],velocities[i][0],velocities[i][1],velocities[i][2]))
       print("")


   printPositions(0, positions, velocities)
   addToHash(hashmap, positions, velocities)
   
   timeStamp = 0
   while True:
       # calculate new velocities
      for pair in pairs:
         for c in range(3):
            if positions[pair[0]][c] < positions[pair[1]][c]:
               velocities[pair[0]][c] += 1
               velocities[pair[1]][c] -= 1
            elif positions[pair[0]][c] > positions[pair[1]][c]:
               velocities[pair[0]][c] -= 1
               velocities[pair[1]][c] += 1
            else:
               pass
        
      # apply velocities
      for i in range(len(positions)):
         for c in range(3):
            positions[i][c] += velocities[i][c]
      if addToHash(hashmap, positions, velocities) == True:
         timeStamp += 1
         # found previous position with same state
         break
       	
      if (timeStamp+1) %100000 == 0:    
         printPositions(timeStamp+1, positions, velocities)
      timeStamp += 1


   print("Alignment after %d steps:"%timeStamp)

def test():
    from scipy.integrate import odeint
    y0 = []
    y0.append([-19,-4,2])
    y0.append([-9,8,-16])
    y0.append([-4,5,-11])
    y0.append([1,9,-13])
    # positions = []
    # positions.append([-1,0,2])
    # positions.append([2,-10,-7])
    # positions.append([4,-8,8])
    # positions.append([3,5,-1])
   

    y0.append([0,0,0])
    y0.append([0,0,0])
    y0.append([0,0,0])
    y0.append([0,0,0])

    y0 = np.asarray(y0)
    y0 = np.reshape(y0, (np.product(y0.shape)))


    pairs = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    # function that returns dy/dt
    def model(y,t):

      positions = []
      positions_dt = []
      velocities = []
      velocities_dt = []
      for i in range(4):
          positions.append([y[i*3+0],y[i*3+1],y[i*3+2]])
          positions_dt.append([0,0,0])
      for i in range(4, 8):
          velocities.append([y[i*3+0],y[i*3+1],y[i*3+2]])
          velocities_dt.append([0,0,0])

      
      # calculate new velocities
      for pair in pairs:
         for c in range(3):
            if positions[pair[0]][c] < positions[pair[1]][c]:
               velocities[pair[0]][c] += 1
               velocities[pair[1]][c] -= 1
               velocities[pair[0]][c] += 1
               velocities[pair[1]][c] -= 1
            elif positions[pair[0]][c] > positions[pair[1]][c]:
               velocities[pair[0]][c] -= 1
               velocities[pair[1]][c] += 1
            else:
               pass
        
      # apply velocities
      for i in range(len(positions)):
         for c in range(3):
            positions[i][c] += velocities[i][c]

      for i in range(4):
          positions.append([y[i*3+0],y[i*3+1],y[i*3+2]])

      return dydt

    y = odeint(model,y0,1000)
    print(y)

if __name__ == '__main__':
    #freeze_support()
    # runPart1()
	#runPart2()
    test()
