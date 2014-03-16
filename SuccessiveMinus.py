#!/usr/bin/python3
#逐差法计算平均距离

def get_input():
    ret = dict()
    print ("N = ?", end="     ")
    n = int(input())
    ret['n'] = n

    if n % 2 == 1:
        raise TypeError("N should be even")

    for i in range(n):
        print(str(i+1)+":  ", end="")
        x = float(input())
        ret[i] = x

    return ret


def compute(data):
    n = data['n'] // 2
    aver = sum([data[i+n] - data[i] for i in range(n)]) / (n * n)
    print ("average = " + str(aver))

data = get_input()
aver = compute(data)
