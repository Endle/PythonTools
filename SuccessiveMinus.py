#!/usr/bin/python3
#逐差法计算

def t95sn(n):
    '''返回 T0.95 / sqrt(n) 的值
    '''
    if n == 3:
        return 2.48
    elif n == 4:
        return 1.59
    else:
        #FIXME: better exception handler needed
        return 0

def get_input():
    ret = dict()
    print ("N = ?", end="     ")
    n = int(input())
    #ret['n'] = n

    if n % 2 == 1:
        raise TypeError("N should be even")

    for i in range(n):
        print(str(i+1)+":  ", end="")
        x = float(input())
        ret[i] = x

    return ret


def default_callback(a, b, ia, ib):
    return (b - a) / (ib - ia)

def compute(data, callback=default_callback):
    '''
    data: A list with 2n elems
    Return a list generated with callback function
    '''
    n = len(data) // 2
    return [callback(data[i], data[i+n], i, i+n) \
            for i in range(n)]


if __name__ == '__main__':
    data = get_input()
    result = compute(data,angular_acceleration)
    print(result)
    import BesselFormula
    S = BesselFormula.compute(result)
    print("S = ", S)
    da = S * t95sn(len(result))
    print("DeltaA = ", da)
