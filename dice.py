#!/usr/bin/python3
from random import shuffle, choice

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

dice = (('d1', ["A", "A", "C", "I", "O", "T"]),
        ('d2', ["A", "B", "I", "L", "T", "Y"]),
        ('d3', ["A", "B", "J", "M", "O", "QU"]),
        ('d4', ["A", "C", "D", "E", "M", "P"]),
        ('d5', ["A", "C", "E", "L", "R", "S"]),
        ('d6', ["A", "C", "D", "E", "M", "P"]),
        ('d7', ["A", "D", "E", "N", "V", "Z"]),
        ('d8', ["B", "I", "F", "O", "R", "X"]),
        ('d9', ["D", "E", "N", "O", "S", "W"]),
        ('d10', ["D", "K", "N", "O", "T", "U"]),
        ('d11', ["E", "E", "F", "H", "I", "Y"]),
        ('d12', ["E", "G", "k", "L", "U", "Y"]),
        ('d13', ["E", "G", "I", "N", "T", "V"]),
        ('d14', ["E", "H", "I", "N", "P", "S"]),
        ('d15', ["E", "L", "P", "S", "T", "U"]),
        ('d16', ["G", "I", "L", "R", "U", "W"]))


# Dice object class used to shuffle and select the dice used in game
class Dice:
    def __init__(self):
        dice_list = [x[1] for x in dice]
        shuffle(dice_list)
        self._current = 0
        self._dice = dice_list

    def __iter__(self):
        return self

    def __next__(self):
        dice_len = len(self._dice)
        if self._current >= dice_len:
            # 2 char check for
            raise StopIteration
        else:
            my_dice = choice(self._dice[self._current])
            #            result = self._dice[self._current][3]
            self._current += 1
            return my_dice
