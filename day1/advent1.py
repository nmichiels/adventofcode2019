import numpy as np
data = np.loadtxt('input_1.txt')
print(data.shape)

def calcFuel(mass):
	if mass > 0:
		fuel = np.floor((mass/ 3.0)) - 2
		
		massFuel = calcFuel(fuel)
		
		if massFuel > 0:
			fuel += massFuel
		return fuel
	return 0
	

sum = 0

for mass in data:
	sum += calcFuel(mass)

print(sum)