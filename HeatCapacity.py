#!/usr/bin/env python3


def Cp_T(t):
    def in_range(x, a, b):
        return a < x and x < b
    if in_range(t, 70, 80):
        return 171.5
    elif in_range(t, 80, 90):
        return 202.7
    elif in_range(t, 90, 100):
        return 229.5
    elif in_range(t, 100, 110):
        return 252.2
    elif in_range(t, 110, 120):
        return 271.2
    elif in_range(t, 120, 130):
        return 287.2
    elif in_range(t, 130, 140):
        return 300.7
    elif in_range(t, 140, 150):
        return 312.2
    elif in_range(t, 150, 160):
        return 322.0
    elif in_range(t, 160, 170):
        return 330.6
    elif in_range(t, 170, 180):
        return 338.0
    elif in_range(t, 180, 190):
        return 344.5
    elif in_range(t, 190, 200):
        return 350.0
    elif in_range(t, 200, 210):
        return 355.0
    elif in_range(t, 210, 220):
        return 359.4
    elif in_range(t, 220, 230):
        return 363.5
    elif in_range(t, 230, 240):
        return 367.1
    elif in_range(t, 240, 250):
        return 370.2
    elif in_range(t, 250, 260):
        return 373.1
    elif in_range(t, 260, 270):
        return 375.8
    elif in_range(t, 270, 280):
        return 378.3
    elif in_range(t, 280, 290):
        return 380.7
    elif in_range(t, 290, 300):
        return 382.9
    else:
        return 384.8


def integrate_Cp(t1, t2):
    from scipy import integrate
    return integrate.quad(Cp_T, t1, t2, limit=10000)

def Debye(T, Td):
    from scipy import integrate
    from math import exp
    a = 9 * 6.02 * 1.38 * T**4 / (Td**3)
    b, e = integrate.quad(lambda x: x**3 / (exp(x) - 1), 0, Td/T)
    return a * b


def main():
    print("比热容法：")
    result, err = integrate_Cp(298.15, 77.3)
    print(result)
    print(err)
    print("德拜温度法：")
    result2 = Debye(77, 428) - Debye(300, 428)
    print(result2)

main()
