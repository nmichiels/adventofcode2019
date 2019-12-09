import numpy as np


def checkRuleDouble(digits):

    for i in range(0, len(digits)-1):
        if digits[i] == digits[i+1]:

            if i-1 >= 0 and digits[i] == digits[i-1]:
                continue
            elif i+2  < len(digits) and digits[i] == digits[i+2]:
                continue
            else:
                return True
    return False

def checkNumber(n):
    digits = [int(d) for d in str(n)]

    correct = False

    for i in range(0, len(digits)-1):



        correct = checkRuleDouble(digits)
           

        if digits[i] > digits[i+1]:
            return False


    return correct


print(checkNumber(112222))



count = 0
for i in range(147981,691424):
    if checkNumber(i):
        count += 1

print("Result: ", count)