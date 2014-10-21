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

#FIXME: range & label
def draw(points, x_range=None, y_range=None, xlabel=None, ylabel=None):
    import matplotlib.pyplot
    x_list = [p[0] for p in points]
    y_list = [p[1] for p in points]
    matplotlib.pyplot.scatter(x_list, y_list)
    matplotlib.pyplot.xlim(0, 2.5)
    matplotlib.pyplot.ylim(0, 0.6)
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
    draw(data, xlabel="c mg/mL", ylabel="A540")
