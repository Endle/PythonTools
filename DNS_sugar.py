#!/usr/bin/env python3

def get_data():
    import basic_tools
    return basic_tools.get_input(lambda s: [float(i) for i in s.split()])


def linear_fit(x_list, y_list):
    from scipy.optimize import leastsq
    from numpy import array
    def fun(p, x):
        return p[0] * x + p[1]
    def err(p, x, y):
        return fun(p, x) - y
#FIXME: initial value
    line = leastsq(err, (-0.01,-1), args=(array(x_list), array(y_list)))
    print(line)
    return line

#FIXME: label
def draw(points, x_range=None, y_range=None, xlabel=None, ylabel=None):
    import matplotlib.pyplot
    x_list = [p[0] for p in points]
    y_list = [p[1] for p in points]
    matplotlib.pyplot.scatter(x_list, y_list)

    def get_range(l0):
        l = sorted(l0)
        diff = l[-1] - l[0]
        va = max(0, l[0] - diff / 10)
        vb = l[-1] + diff/10
        print(l)
        print(va, vb)
        return (va, vb)

    if not x_range:
        x_range = get_range(x_list)
    if not y_range:
        y_range = get_range(y_list)
    if not xlabel:
        xlabel = ""
    if not ylabel:
        ylabel = ""

    matplotlib.pyplot.xlim(x_range[0], x_range[1])
    matplotlib.pyplot.ylim(y_range[0], y_range[1])

    matplotlib.pyplot.xlabel(xlabel)
    matplotlib.pyplot.ylabel(ylabel)

#FIXME
    def fun(p, x):
        return p[0] * x + p[1]
    line = linear_fit(x_list, y_list)
    matplotlib.pyplot.plot(x_list, [fun(line[0], x) for x in x_list])
    matplotlib.pyplot.show()
    #return line[0]



if __name__ == '__main__':
    data = get_data()
    draw(data)
