#!/usr/bin/python3
#-*- coding: utf-8 -*-

ENCODE = "utf-8"

WORKING_PATH = "" #Need Initialize

import os, shutil, sys

def _eat(lines):
    '''Will read a list of lines,
    Then return a list of modified lines.
    '''
    return [line.rstrip()  for line in lines]

def handle_file(path, file):
    '''Move $file to ORI_FILE'''
    print(file)
    src = os.path.join(path, file)

    fin = open(src, 'r', encoding=ENCODE)
    lines = fin.readlines()
    fin.close()

    lines = _eat(lines)
    fout = open(src, 'w', encoding=ENCODE)
    for line in lines:
        print(line, file=fout)
    fout.close()

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
