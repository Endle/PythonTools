#!/usr/bin/env python3
import basic_tools
from collections import namedtuple
import sys, os
import numpy
from PySide.QtGui import *

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



def main():
# Create a Qt application
    app = QApplication(sys.argv)
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
    print(path)
    absorb = handle_xls(path)
    print(absorb)

    sys.exit()




if __name__ == '__main__':
    main()
else:
    raise Exception("Shouldn't be used by other component")
