#!/usr/bin/python3
#-*- coding: utf-8 -*-

ENCODE = "utf-8"

WORKING_PATH = "" #Need Initialize


import os, shutil, sys

def report(file, line, flag):
    if not flag:
        print("In  " + file)
    print ("  " + line)
    return True

def _find(lines, file):
    flag = False
    for line in lines:
        if '\t' in line:
            flag = report(file, line, flag)

def handle_file(path, file):
    print(file)
    src = os.path.join(path, file)

    fin = open(src, 'r', encoding=ENCODE)
    lines = fin.readlines()
    fin.close()

    _find(lines, src)

def walk_path(path):
    for name in os.listdir(path):
        if name[0] == '.':
            continue    #Ignore
        name = os.path.join(path, name)
        if os.path.isfile(name):
            handle_file(path, name)
        elif os.path.isdir(name):
            walk_path(name)

if __name__ == '__main__':
    if len(sys.argv) < 2:
       work_list = ('.',)
    else:
        work_list = tuple(sys.argv[1:])

    for work in work_list:
        WORKING_PATH = os.path.abspath(work)
        walk_path(WORKING_PATH)
