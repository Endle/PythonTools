#!/usr/bin/env python3
import basic_tools
from collections import namedtuple
from momap import momap

# ValueGroup 对应一个样品测量三次后得到的数值
ValueGroup = namedtuple("ValueGroup", ["average", "data_range"])
# SingleSample 对应一个样品测量三次后得到的结论
SingleSample = namedtuple("SingleSample",
        ["ingredient", "ratio", "value"])
# SingleRatio 包含的信息比 SingleSample 少
# SingleSample 按照 ingredient 分类后，每个 SingleRatio 对应一个配比
SingleRatio = namedtuple("SingleRatio",
        ["ratio", "value"])

class IndexOfSheet():
    Type = 1
    Name = 2
    Size = 5
    Zeta = 8

def get_ith(p):
    return lambda d: float( d.split(':')[p] )


def get_data_point(l):
    '''Get a list/tuple of strings
    Return a ValueGroup tuple (average, (range) )
    '''
    l = [float(i) for i in l]
    ave = sum(l) / len(l)
    ran = basic_tools.get_range(l)
    result = ValueGroup(ave, ran)
    return result

def find_portion(x):
    '''It is a HACK here!
    Should be more general
    '''
    return x[0].split('=')[0]

def load_data(filename="lip.csv"):
    '''读取一个 csv 文件，没有最上一行的标题，左侧有行号
    返回一个 tuple
    '''
    def get_size(csvdata):
        return ([l[IndexOfSheet.Name].split(' ')[0], l[IndexOfSheet.Size]]\
                for l in csvdata if l[IndexOfSheet.Type] == 'Size')
    def get_zeta(csvdata):
        return ([l[IndexOfSheet.Name].split(' ')[0], l[IndexOfSheet.Zeta]]\
                for l in csvdata if l[IndexOfSheet.Type] == 'Zeta')

    def split_by_name(data, wrapper=None):
        result = momap()
        for d in data:
            elem = d[1:]
            if wrapper:
                elem = wrapper(elem)
            result.extend(d[0], elem)
        return result

    def arrange_data(data):
        '''Expects a dict
        {sample_name : [data1, data2, data3]}
        sample_name & data_i are strings

        Return a list of SingleSample
        Each Element: [ingredient, amount, (average, (range)) ]
        Example: ['PGL3:P2:liposome:HA', '1:4:2:14.2', (5, (220.4, 222.9) )]
        '''
        group = split_by_name(data)
        result = list()
        for k,v in group.items():

            assert type(k) is str
            assert len(v) == 3
            assert type(v[0]) == type(v[1]) == type(v[2]) == str

            r = get_data_point(v)
            i = k.split('=')
            i.append(r)
            result.append(SingleSample._make(i))
        return result

# 把 size 和 data 对应的行和列抓取出来
    csvdata = basic_tools.load_csv(filename)
    size = get_size(csvdata)
    zeta = get_zeta(csvdata)

#Get Average & Range Here
    size = arrange_data(size)
    zeta = arrange_data(zeta)

    return(size, zeta)

import plotly.plotly as py
from plotly.graph_objs import *

def plotly_print(data, title="", x_axis="", y_axis=""):
    '''data 是一个 MultiMap
    '''

    def get_scatter(vals, fetchx, line_name=""):
        '''vals 是 [SingleRatio]
        返回一个 Scatter
        '''
        x_list = [fetchx(i.ratio) for i in vals]
        y_list = [i.value         for i in vals]
        data_list = list(zip(x_list, y_list))
        data_list.sort(key=lambda t:t[0])
        x_list = [i[0] for i in data_list]
        v_list = [i[1] for i in data_list]
        y_list = [i.average for i in v_list]

        return Scatter(
                x = x_list,
                y = y_list,
                error_y=ErrorY(
                    type='data',
                    symmetric=False,
                    array = [i.data_range[1] - i.average for i in v_list],
                    arrayminus = [i.average - i.data_range[0] for i in v_list],
                    ),
                name = line_name,
                )

    DataList = []


    for k, v in data.items():
        line = get_scatter(v, fetchx=get_ith(3), line_name=k)
        DataList.append(line)

    layout = Layout(
        title=title,
        xaxis=XAxis(title=x_axis),
        yaxis=YAxis(title=y_axis)
        )

    data = Data(DataList)
    fig = Figure(data=data, layout=layout,
            font=Font(family='Droid Sans, sans-serif'))
    unique_url = py.plot(fig, filename = 'temp')

def main():
    def split_by_peptide(data_list, wrapper=None):
        result = momap()
        for d in data_list:
            key = d.ingredient + "=" + ":".join(d.ratio.split(":")[:3]) + ":x"
            elem = d[1:]
            if wrapper:
                elem = wrapper(elem)
            result.add(key, elem)
        return result
    (size, zeta) = load_data()
    size = split_by_peptide(size, wrapper=SingleRatio._make)
    zeta = split_by_peptide(zeta, wrapper=SingleRatio._make)
# After that, size is a (multi)dict
# size[ingredient] = [SingleRatio]

    plotly_print(size,
            title="粒径与透明质酸含量的关系",
            x_axis="透明质酸与DNA质量比",
            y_axis="Z-Ave (d.nm)"
            )

    #plotly_print(zeta,
            #title="电势与透明质酸含量的关系",
            #x_axis="透明质酸与DNA质量比",
            #y_axis="ZP (mV)"
            #)

if __name__ == '__main__':
    main()
else:
    raise Exception("size_data.py shouldn't be used by other component")

