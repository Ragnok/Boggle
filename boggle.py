#!/usr/bin/python3
import sys
if sys.version_info < (3, 0):
    sys.exit("Boggle requires Python 3.0 or greater. "
             "Please consider upgrading.")
from gui import My_Boggle
"""
MSG Mike Simpson
March 2016
Boggle game was written for, and is to be used for learning purposes only
Hasbro Gaming, Boggle, and all related terms are trademarks of Hasbro.

letter distribution Hasbro in standard 16 dice Plain old Boggle, 1976-1986
http://www.bananagrammer.com/2013/10/the-boggle-cube-redesign-and-its-effect.html

Pictures modified from:
http://www.wordtwist.org/
http://www.reachingteachers.com.au/
http://www.macgasm.net/2010/06/16/boggle-ipad-review/
https://www.pinterest.com/mindyateach/word-work/

"""


def main():
    boggle = My_Boggle()
    boggle.master.title('Boggle')
    boggle.mainloop()

if __name__ == '__main__':
    main()
