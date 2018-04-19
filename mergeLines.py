#!/usr/bin/env python3

""" 从命令行中不断读取新字符串，直到EOF
生成 markdown 标题
"""

#https://stackoverflow.com/a/18403812/1166518
isascii = lambda s: len(s) == len(s.encode())

import sys

ret = ""
for line in sys.stdin:
    ret += " " + line.rstrip()

ret = "## " + ret + "  \n"
print(ret)
if not isascii(ret):
    print("WARNING: non-ASC II")

