#!/usr/bin/python3
#-*- coding: utf-8 -*-

ORI_FILE = "_origin"
OPT_FILE = "_result"
ENCODE = "utf-8"

WORKING_PATH = "" #Need Initialize

import os, shutil, sys

def _eat(src, dst):
    '''Will read src and write to dst
    Then close these file.'''
    fin = open(src, 'r', encoding=ENCODE)
    fout = open(dst, 'w', encoding=ENCODE)
    for line in fin:
        print(line.rstrip(), file=fout)

    fin.close()
    fout.close()

def move_file(path, file):
    '''Move $file to ORI_FILE'''
    print(file)
    src = os.path.join(path, ORI_FILE)
    dst = os.path.join(path, OPT_FILE)

    shutil.move(file, src)
    _eat(src, dst)
    shutil.move(dst, file)
    os.remove(src)

def walk_path(path):
    for name in os.listdir(path):
        if name[0] == '.':
            continue    #Ignore
        name = os.path.join(path, name)
        if os.path.isfile(name):
            move_file(path, name)
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
