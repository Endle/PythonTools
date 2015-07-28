#!/usr/bin/env python3
import basic_tools
from collections import namedtuple
import sys, os
import numpy
#from PySide.QtGui import *
import PySide.QtGui

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

def _standart_curve(a:float=10, b:float=100):
    return lambda x : a * x + b

def funm(dat:numpy.matrix, f) -> numpy.matrix:
    '''Dirty copycat for scipy.linalg.funm'''
    ret = dat.copy()
    for x in numpy.nditer(ret, op_flags=['readwrite']):
        x[...] = f(x)

    return ret


def absorb_to_protein(absorb:numpy.matrix) -> numpy.matrix:
    f = _standart_curve()
    ret = funm(absorb, f)
    return ret

def get_cell_name() -> str:
    import PySide.QtGui
    dialog = PySide.QtGui.QInputDialog()
    return dialog.getText(dialog, "", "Cell name: ")[0]

def choose_protein_data(grid:numpy.matrix) -> list:
    import PySide.QtGui
    size = grid.shape
    twid = PySide.QtGui.QTableWidget(size[0], size[1])
    for row in range(size[0]):
        for col in range(size[1]):
            value = grid.item(row, col)
            item = PySide.QtGui.QTableWidgetItem(value)
            twid.setItem(row, col, item)

    twid.setWindowTitle('Simple')
    twid.resize(800, 600)
    twid.show()
    return []


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
    path = "/home/lizhenbo/文档/第十期大创(2014)/20150708 H1299 NIH3T3.xls"
    absorb = handle_xls(path)

    protein = absorb_to_protein(absorb)

    #cell = get_cell_name()
    cell = "H1299"

    cell_data = choose_protein_data(protein)
    #print(cell_data)

    _MAIN_WINDOW = PySide.QtGui.QWidget()
    _MAIN_WINDOW.setWindowTitle('Luciferase')
    _MAIN_WINDOW.resize(800, 600)
    _MAIN_WINDOW.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
else:
    raise Exception("Shouldn't be used by other component")
