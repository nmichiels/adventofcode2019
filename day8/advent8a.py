import numpy as np

file = open('input_8.txt', 'r')

def split(word): 
    return [char for char in word]  

line = split(file.readline())

#remove \n
line = line[:-1]


width = 25
height = 6

layers = int(len(line) / (width*height))


print('layers', layers)
image = np.reshape(line, (width, height, layers), order='F') # Fortran-like index ordering)
print(image.shape)
image = np.transpose(image, axes=(1,0,2))


maxNumber = 99999999999
minLayer = -1
for i in range(image.shape[2]):

    unique, counts = np.unique(image[:,:,i], return_counts=True)
    occ = dict(zip(unique, counts))
    if occ['0'] < maxNumber:
        maxNumber = occ['0']
        minLayer = i


# calc result
unique, counts = np.unique(image[:,:,minLayer], return_counts=True)
occ = dict(zip(unique, counts))

print("result:", occ['1']*occ['2'])


#part 2 decode image

result = np.zeros((height,width), dtype='int')

for row in range(height):
    for col in range(width):

        i = 0
        while image[row,col,i] == '2': # as long as transparant, continue to next layer
            i += 1
        #print(image[row,col,i])
        if image[row,col,i] == '1':
            result[row,col] = 1

        print(result[row,col], end='')

    print('')

import cv2

import matplotlib.pyplot as plt
imgplot = plt.imshow(result)
plt.show()

