#!/usr/bin/python3
import os, sys

if __name__ == '__main__':

    file = sys.argv[1]
    try:
        symbol = sys.argv[2]
        print(symbol)
    except IndexError:
        print("Default symbol: >")
        symbol = '>'

    file = os.path.abspath(file)
    #print(file)
    fin = open(file, 'r', encoding='utf-8')
    lines = fin.readlines()
    #print(lines)
    fin.close()

    fout = open(file, 'w', encoding='utf-8')
    for line in lines:
        line = symbol + line.rstrip()
        #print(line)
        print(line, file=fout)
    fout.close()

