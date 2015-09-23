#!/usr/bin/env python3
import basic_tools
from collections import namedtuple
import sys, os
import numpy
#from PySide.QtGui import *
import PySide.QtGui
import PySide.QtCore

_MAIN_WINDOW = None

def handle_xls(file_path:str) -> numpy.matrix :
    import xlrd
    book = xlrd.open_workbook(file_path, encoding_override="gbk")
    table = book.sheet_by_name("Result Data")
# 96 孔板
    tmp_list = []
    for r in range(2, 10):
        row_data = table.row_values(r)[1:]
        tmp_list.append(row_data)

    ret = numpy.matrix(tmp_list)
    assert ret.shape == (8, 12)
    return ret

def handle_xlsx(file_path:str, cell_name:str) -> numpy.matrix :
    import openpyxl
    book = openpyxl.load_workbook(file_path)
    sheet = book.get_sheet_by_name(cell_name)
    cols = len(sheet.columns)
    if cols == 1:
        col = 0
    elif cols == 2:
        col = 1
    else:
        #FIXME: 给更多的提示
        #import PySide.QtGui
        #dialog = PySide.QtGui.QInputDialog()
        #text = dialog.getText(dialog, "", "Choose right column: ")[0]
        #col = int(text)
        col = 0

    data = [cell.value for cell in sheet.columns[col]]
    print(data)
    return data

def _standart_curve(a:float=1, b:float=0):
    return lambda x : a * x + b

def funm(dat:numpy.matrix, f) -> numpy.matrix:
    '''Dirty copycat for scipy.linalg.funm'''
    ret = dat.copy()
    for x in numpy.nditer(ret, op_flags=['readwrite']):
        x[...] = f(x)

    return ret


def absorb_to_protein(absorb:numpy.matrix) -> numpy.matrix:
    f = _standart_curve()
    #FIXME: 调试中先不调用
    #ret = funm(absorb, f)
    ret = absorb.copy()
    return ret

def get_cell_name() -> str:
    import PySide.QtGui
    dialog = PySide.QtGui.QInputDialog()
    return dialog.getText(dialog, "", "Cell name: ")[0]

def get_chosen_range(grid:numpy.matrix, app:PySide.QtGui.QApplication) -> list:
# http://segmentfault.com/q/1010000003028975
    size = grid.shape
    twid = PySide.QtGui.QTableWidget(size[0], size[1])
# 为了设置宽度方便
    for col in range(size[1]):
        twid.setColumnWidth(col, 80)
        for row in range(size[0]):
            value = grid.item(row, col)
            item = PySide.QtGui.QTableWidgetItem(str(value))
            twid.setItem(row, col, item)
    twid.resize(1020, 400)
    twid.setEditTriggers(PySide.QtGui.QAbstractItemView.NoEditTriggers)
    twid.show()

    chosen_cell = []
    @PySide.QtCore.Slot(int, int)
    def double_click_cell(row, col):
        chosen_cell.append([row, col])
        print(chosen_cell)
        if len(chosen_cell) == 2:
            app.closeAllWindows()
    twid.cellDoubleClicked.connect(double_click_cell)
    app.exec_()
    return chosen_cell

def get_chosen_cell(grid:numpy.matrix, points:list) -> list:
    print(points)
#FIXME: Only support one cell now
    assert len(points) == 2
    begin = points[0]
    end = points[1]
    ret = []
    for row in range(begin[0], end[0]):
        ret += grid[row].flat
#FIXME: 假定至少有一排
    for col in range(0, end[1] + 1):
        ret.append(grid.item(end[0], col))
    return ret

class ValueType(object):
    '''相比于用 namedtuple 实现的 ValueGroup，还是使用 class 更方便
    '''
    __slots__ = ("name", "average", "minimum", "maximum")
    def __init__(self, l):
        self.minimum = min(l)
        self.maximum = max(l)
        self.average = sum(l) / len(l)
    def __repr__(self):
        return '%s: average %f, data range (%f, %f)' % (self.name, self.average, self.minimum, self.maximum)


def main():
# Create a Qt application
    app = PySide.QtGui.QApplication(sys.argv)

    cell_count = 1 # FIXME: Hard-coded

    def get_cell_value():
        '''得到该细胞的 ValueGroup
        '''
        #path = basic_tools.getOpenFileName(title="选择吸光度文件",
                #directory=os.path.expanduser("~/文档/第十期大创(2014)"),
                #filter_str="Excel files (*.xls)")
        path = "/home/lizhenbo/文档/第十期大创(2014)/15.07.25 CHO C518/20150725 CHO C518 protein.xls"
        absorb = handle_xls(path)
        protein = absorb_to_protein(absorb)

        #cell = get_cell_name()
        cell = "CHO"

        chosen_protein = get_chosen_cell(protein,
                [[0, 0], [1, 5]])
                #get_chosen_range(protein, app))

        #path = basic_tools.getOpenFileName(title="选择萤光强度文件",
                #directory=os.path.expanduser("~/文档/第十期大创(2014)"),
                #filter_str="Excel files (*.xlsx)")
        path = "/home/lizhenbo/文档/第十期大创(2014)/15.07.25 CHO C518/20150725 CHO C518.xlsx"

        if(path[-5:] != ".xlsx"):
            print("Not support yet")
            sys.exit()

        chosen_fluorescence = handle_xlsx(path, cell)

        assert len(chosen_protein) == len(chosen_fluorescence)
        ratio_list = [chosen_fluorescence[i] / chosen_protein[i] for i in range(len(chosen_protein))]
        print(ratio_list)

        import more_itertools
        assert len(ratio_list) % 3 == 0
        ratio_chunk = more_itertools.chunked(ratio_list, 3)
        result_list = [ValueType(chunk)  for chunk in ratio_chunk]
        #print(result_list)

        fin_ingredient = open("ingredient.txt")
        ingredient = [s.strip() for s in fin_ingredient.readlines()]
        #print(ingredient)
        fin_ingredient.close()

        if len(result_list) != len(ingredient):
            print("长度不匹配，自动截断")
            assert len(result_list) > len(ingredient)
            assert (len(result_list) - len(ingredient)) % 3 == 0
            result_list = result_list[:len(ingredient)]
        else:
            print("长度相同，自动匹配")

        for i in range(len(result_list)):
            result_list[i].name = ingredient[i]

        print(result_list)
        return result_list

    print("开始打印图象了")
    import matplotlib.pyplot as plt
    import numpy

    data_list = []
    cell_name = ["CHO"]
    for i in range(cell_count):
        data_list.append(get_cell_value())

    print(cell_count)
    ingredient_count = len(data_list[0])
    print(ingredient_count)
    index = numpy.arange(cell_count) # 对应的是横坐标的起点
    bar_width = 0.35

    def get_rect(ing):
        means = []
        for ic in range(cell_count): # 把每个细胞的信息抓取出来
            print(data_list[ic][ing])
            means.append(data_list[ic][ing].average)
        print(means)
        rect = plt.bar(index + ing * bar_width, means, bar_width, label=data_list[0][ing].name)
        return rect

    rect_list = [get_rect(i) for i in range(ingredient_count)]

    plt.xlabel("Cells")
    plt.ylabel("Relative fluorescence")

    #print(cell_name)
    plt.xticks(index + bar_width, cell_name)
    plt.legend()

    plt.tight_layout()

    plt.savefig("cancer.svg", format="svg")
    plt.show()

    sys.exit()



if __name__ == '__main__':
    main()
else:
    raise Exception("Shouldn't be used by other component")
