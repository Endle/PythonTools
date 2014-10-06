#!/usr/bin/env python3

def get_data():
    data = []
    for i in range(4):
        s = input()
        s = s.split()
        data.append([float(a) for a in s])
    return data

def compute(d):
    import math
    ret = {}
    ret['T'] = 273.16 + d[0]
    ret['p'] = 96.744 + d[1]
    ret['k'] = 4 / 27 * (ret['p'] / 100) ** 3
    ret['k*10000'] = ret['k'] * 10000
    ret['lnK'] = math.log(ret['k'])
    ret['1:T'] = 1 / ret['T']

    ret['G'] = -8.315 * ret['T'] * ret['lnK']

    return ret

def draw(points):
    import matplotlib.pyplot
    #for p in points:
        #matplotlib.pyplot.plot(p[0], p[1])
    x_list = [p[0] for p in points]
    y_list = [p[1] for p in points]
    matplotlib.pyplot.scatter(x_list, y_list)
    matplotlib.pyplot.xlim(0.00317, 0.0033)
    matplotlib.pyplot.ylim(-8.5, -4)
    matplotlib.pyplot.xlabel('1/T')
    matplotlib.pyplot.ylabel('lnK')

    from scipy.optimize import leastsq
    from numpy import array
    def fun(p, x):
        return p[0] * x + p[1]
    def err(p, x, y):
        return fun(p, x) - y

    line = leastsq(err, (-0.01,-1), args=(array(x_list), array(y_list)))
    print(line)

    x1_list = [0.003171] + x_list + [0.003298]
    matplotlib.pyplot.plot(x1_list, [fun(line[0], x) for x in x1_list])
    #matplotlib.pyplot.show()
    return line[0]

def compute2(d, h, r0):
    r = {}
    r['G'] = -8.315 * r0['T'] * r0['lnK'] / 1000
    r['S'] = (h - r['G']) / r0['T']
    return r


if __name__ == '__main__':
    data = get_data()
    ret_list = []
    for d in data:
        ret = compute(d)
        print(ret)
        print("")
        ret_list.append(ret)

    p_list = [(r['1:T'], r['lnK']) for r in ret_list]
    line_data = draw(p_list)
    h = 268.09

    ret_list2 = []
    for d in data:
        ret0 = compute(d)
        ret = compute2(d, h, ret0)
        print(ret)
        print("")
        ret_list2.append(ret)

    import BesselFormula
    s_list = [r['S'] for r in ret_list2]
    s = BesselFormula.compute(s_list)
    print(s)

