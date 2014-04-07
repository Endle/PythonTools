#!/usr/bin/python3
#转动惯量

gravity = 9.78
R = 25.0 / 1000 #实验台的半径
M = 22.1 / 1000 #砝码的质量

def get_input():
    ret = list()
    print ("N = ?", end="     ")
    n = int(input())

    if n % 2 == 1:
        raise TypeError("N should be even")

    for i in range(n):
        print(str(i+1)+":  ", end="")
        x = float(input())
        ret.append(x)

    return ret

def acceleration2rotationalInertia(acc1, acc2):
    return M * R * (gravity - R*acc2) / (acc2 - acc1)

def angular_acceleration(tm, tn, km, kn):
    km = km + 1
    kn = kn + 1
    import math
    return 2*math.pi * (kn*tm - km*tn) / \
            ((tm*tn) * (tn - tm))

if __name__ == '__main__':
    import SuccessiveMinus, BesselFormula
    data = get_input()
    result = SuccessiveMinus.compute(data,angular_acceleration)
    print(result)
    S = BesselFormula.compute(result)
    print("S = ", S)
    da = S * SuccessiveMinus.t95sn(len(result))
    print("DeltaA = ", da)
