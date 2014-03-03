#!/usr/bin/python3
#Use python3!

def get_input():
    ret = dict()
    print ("N = ?", end="     ")
    n = int(input())
    ret['n'] = n

    for i in range(n):
        print(str(i)+":  ", end="")
        x = float(input())
        ret[i] = x
    
    return ret
    

def compute(data):
    n = data['n']
    aver = sum([data[i] for i in range(n)]) / n
    print ("average = " + str(aver))

    a = sum([ (data[i]-aver) **2 for i in range(n)])
    b = n - 1
    import math
    return math.sqrt(a / b)



data = get_input()
S = compute(data)
print ("S = " + str(S))
