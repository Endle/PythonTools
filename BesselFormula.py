#!/usr/bin/python3
#贝赛尔公式

def get_input():
    import RotationalInertia
    return RotationalInertia.get_input()

def compute(data):
    n = len(data)
    aver = sum([data[i] for i in range(n)]) / n
    print ("average = " + str(aver))

    a = sum([ (data[i]-aver) **2 for i in range(n)])
    b = n - 1
    import math
    if b == 0:
        return None
    return math.sqrt(a / b)

if __name__ == '__main__':
    data = get_input()
    S = compute(data)
    print ("S = " + str(S))
