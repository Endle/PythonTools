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
    for col in range(0, end[1]):
        ret.append(grid.item(end[0], col))
    return ret

def main():
# Create a Qt application
    app = PySide.QtGui.QApplication(sys.argv)
    '''
    path = basic_tools.getOpenFileName(title="选择萤光强度文件",
            directory=os.path.expanduser("~/文档/第十期大创(2014)"),
            filter_str="Excel files (*.xls *.xlsx)")
    print(path)

    if(path[-5:] == ".xlsx"):
        print("Not support yet")
        sys.exit()

    handle_xls(path)

    sys.exit()
    '''
    '''
    path = basic_tools.getOpenFileName(title="选择吸光度文件",
            directory=os.path.expanduser("~/文档/第十期大创(2014)"),
            filter_str="Excel files (*.xls)")
    '''
    #path = "/home/lizhenbo/文档/第十期大创(2014)/20150708 H1299 NIH3T3.xls"
    path = "/home/lizhenbo/sample.xls"
    absorb = handle_xls(path)

    protein = absorb_to_protein(absorb)

    #cell = get_cell_name()
    cell = "H1299"

    chosen_protein = get_chosen_cell(protein,
            get_chosen_range(protein, app))
    print(chosen_protein)




if __name__ == '__main__':
    main()
else:
    raise Exception("Shouldn't be used by other component")
