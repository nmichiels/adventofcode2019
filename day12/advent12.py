import numpy as np



def run():
   positions = []
   positions.append([-19,-4,2])
   positions.append([-9,8,-16])
   positions.append([-4,5,-11])
   positions.append([1,9,-13])
   
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


if __name__ == '__main__':
    #freeze_support()
    run()
