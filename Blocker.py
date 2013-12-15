'''This program should read text from stdin,
and get the block_list from argv

**REMEMBER: KISS**
'''
import os, sys

if __name__ == '__main__':
    block_list = list(sys.argv[1:])
    ignore_case = False
    if '-i' in block_list:
        ignore_case = True

    config = (block_list, ignore_case) #ugly here

    #to be continue
