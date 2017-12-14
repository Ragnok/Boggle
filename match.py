#!/usr/bin/env python3
from dice import Dice

"""
MSG Mike Simpson
March 2016
Boggle game was written for, and is to be used for learning purposes only
Hasbro Gaming, Boggle, and all related terms are trademarks of Hasbro.

Guidance and direction Brook Eliason Search algorithm modified from
(is_match and on_board) modified from pg.347 -348 of Data Structures
and Algorithms Made Easy"by Narasimha Karumanchi"

letter distribution Hasbro in standard 16 dice Plain old Boggle, 1976-1986
http://www.bananagrammer.com/2013/10/the-boggle-cube-redesign-and-its-effect.html

Pictures modified from:
http://www.wordtwist.org/
http://www.reachingteachers.com.au/
http://www.macgasm.net/2010/06/16/boggle-ipad-review/
https://www.pinterest.com/mindyateach/word-work/

"""


# wordlist class
class Wordlist:
    def __init__(self, max_len, charset):
        self._max_len = max_len
        # if we didn't supply a wordlist, use lowercase ascii
        self._charset = charset
        self._all_words = set()
        # setup partial words as an max_len-1 size array of empty sets
        self._partial_words = [set() for idx in range(max_len)]

    def load_file(self, filename):
        # FIXME should check if this actually succeeds.. ABC
        wordfile = open(filename)

        for word in wordfile:
            self._add_word(word.strip())

    # add a word to our wordlist
    def _add_word(self, word):
        word_len = len(word)
        charset = self._charset.copy()
        # check if the word is too long or too short
        if word_len < 3 or word_len > self._max_len:
            return
        # check if it is in the dice charset
        for idx in range(word_len):
            char = word[idx:idx+1]
            if char not in charset:
                return
            charset.remove(char)

        # now, we it has passed our 'is_word' checks.. import it
        word = word.upper()
        self._all_words.add(word)
        for idx in range(len(word)-1):
            self._partial_words[idx+1].add(word[0:idx+1])

    # simple public function to see if a word is in our wordlist
    # returns True/False
    def is_word(self, word):
        return word in self._all_words

    # simple public function to see if a partial word exists in our wordlist
    # returns True/False
    def is_partial(self, partial):
        word_len = len(partial)
        # first check if our partial word is out of bounds
        if word_len > len(self._partial_words):
            return False
        return partial in self._partial_words[word_len]


# player class
class Player:
    def __init__(self):
        self._score = 0
        self._word_lst = []

    def add_word(self, word, score):
        self._word_lst.append(word)
        self._score += score

    def get_score(self):
        return self._score


# main Match
class Match:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        die = Dice()
        self.difficulty = 0
        self._size = 4
        self._board = [[next(die)
                        for x in range(0, 4)]
                       for y in range(0, 4)]
        self._max_word_len = 0
        self._valid = []
        self._wordlist = self._game_words('/usr/share/dict/american-english')
        # find our words on the actual board
        self._search_board()

    def score(self, word):
        word_len = len(word)
        if word_len < 3:
            return 0
        scores = {3: 1, 4: 1, 5: 2, 6: 3, 7: 5}
        return scores.get(word_len, 11)

    @property
    def size(self):  # public size
        return self._size

    @property
    def board(self):  # public board
        return self._board

    @property
    def valid(self):  # public valid
        return self._valid

    def player_add(self, player, word):  # add word
        word = word.upper()
        score = self.score(word)
        if word in self._valid and score > 0:
            self._valid.remove(word)
            player.add_word(word, score)
            return True
        return False

    # returns a list of tuples of valid adjascent tiles from x/y
    def _adjascent_tiles(self, x, y):
        adj = []
        new_y = y - 1
        if new_y >= 0:
            adj.append((x, new_y))
            new_x = x - 1
            if new_x >= 0:
                adj.append((new_x, new_y))
            new_x = x + 1
            if new_x < self._size:
                adj.append((new_x, new_y))
        new_y = y + 1
        if new_y < self._size:
            adj.append((x, new_y))
            new_x = x - 1
            if new_x >= 0:
                adj.append((new_x, new_y))
            new_x = x + 1
            if new_x < self._size:
                adj.append((new_x, new_y))
        new_x = x - 1
        if new_x >= 0:
            adj.append((new_x, y))
        new_x = x + 1
        if new_x < self._size:
            adj.append((new_x, y))
        return adj

    # recursive private function to build words
    # from the board to compare with our wordlist
    def _walk_tile(self, seq, x, y, used):
        seq += self._board[x][y]
        if self._wordlist.is_word(seq) and seq not in self._valid:
            self._valid.append(seq)
        if not self._wordlist.is_partial(seq):
            return
        used.append((x, y))
        for (new_x, new_y) in self._adjascent_tiles(x, y):
            if (new_x, new_y) not in used:
                self._walk_tile(seq, new_x, new_y, used)
        used.pop()

    # simple private function to call _walk_tile
    # for each tile on the board
    def _search_board(self):
        for x in range(self.size):
            for y in range(self.size):
                self._walk_tile("", x, y, [])

    # private function to generate a wordlist
    # from a file based on the current board
    def _game_words(self, filename):
        # first.. find out our max word length and charset
        # based of the tiles on the board
        max_len = 0
        charset = []
        for x in range(self.size):
            for y in range(self.size):
                max_len += len(self._board[x][y])
                for idx in range(len(self._board[x][y])):
                    # use a lower charset for wordlist class
                    # so we can ignore proper nouns
                    charset.append(self._board[x][y][idx:idx+1].lower())

        # generate our wordlist
        wordlist = Wordlist(max_len, charset)
        wordlist.load_file(filename)
        return wordlist
