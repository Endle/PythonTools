#!/usr/bin/env python3

""" 从命令行中不断读取新字符串，直到EOF
生成 markdown 标题
"""

import sys

ret = ""
for line in sys.stdin:
    ret += " " + line.rstrip()

ret = "## " + ret + "  \n"
print(ret)
