# !/usr/bin/python3
import tkinter as tk
import sys
from match import Match
from random import choice

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


# My_Boggle class is the main class for out boggle object
class My_Boggle(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        # countdown
        self.remaining = 0
        self.grid()
        self.game_time = 180
        self.file = "alpha3/"
        # background image
        background_image = tk.PhotoImage(file="background2d.ppm")
        background_label = tk.Label(self, image=background_image)
        self.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # radiobutton
        self._option_frame = tk.Frame(self, bg="royalblue3")
        self.start_button = tk.Button(self._option_frame, text="START",
                                      state="disabled", bg="royalblue2",
                                      command=self._start_)
        self.select = tk.Label(self._option_frame, text="SELECT",
                               bg="royalblue3")
        self.select.grid(row=0, column=0)
        self.R1 = tk.Radiobutton(self._option_frame,
                                 text="Simple Green (Easy)    ", value=1,
                                 command=lambda: self.set_difficulty(0),
                                 bg="SteelBlue2", bd=0)
        self.R1.grid(row=1, column=0)
        self.R1.deselect()
        self.R2 = tk.Radiobutton(self._option_frame,
                                 text="Crazy Colors (Hard)      ", value=2,
                                 command=lambda: self.set_difficulty(1),
                                 bg="SteelBlue2", bd=0)
        self.R2.grid(row=2, column=0)
        self.R2.deselect()
        self.start_button.grid(row=9, column=0)
        self._option_frame.grid(row=6, column=5)
        # computer guess time slider
        self._time_slider = tk.Scale(self._option_frame, from_=1, to=10,
                                     orient='horizontal',
                                     tickinterval=1, length=162,
                                     label="Computer Guess (seconds)",
                                     bg="cornflower blue",
                                     troughcolor="grey")
        self._time_slider.set(7)
        self._time_slider.grid(row=8, column=0)
        self.turn_delay = self._time_slider.get() * 1000
        # win
        self.user_win = tk.Frame(self, width=200, height=200)
        self.win = tk.Label(self.user_win, text="\nYou WIN!\n")
        self.win.grid(row=0, column=0)
        # lose
        self.user_lost = tk.Frame(self, width=200, height=200)
        self.lose = tk.Label(self.user_lost, text="\nYou Lost!\n")
        self.lose.grid(row=0, column=0)
        # tie
        self.user_tie = tk.Frame(self, width=200, height=200)
        self.tie = tk.Label(self.user_tie, text="\nTie Game!\n")
        self.tie.grid(row=0, column=0)
        # print unguessed words
        self._unguessed_frame = tk.Frame(self, bg="royalblue3")
        # remaining words
        self._option_frame2 = tk.Frame(self, width=200, height=200,
                                       bg="royalblue3")
        self.remaining = tk.Label(self._option_frame2, bg="royalblue3",
                                  text="\nWords Remaining:", font="bold")
        self.remain = tk.StringVar()
        self.select3 = tk.Label(self._option_frame2, textvariable=self.remain)
        self.remaining.grid(row=0, column=0)
        self.select3.grid(row=1, column=0)
        # score
        self._p1_score_frame = tk.Frame(self)
        self._p1_score_label = tk.Label(self._p1_score_frame, text='Score:')
        self._cmp_score_frame = tk.Frame(self)
        self._cmp_score_label = tk.Label(self._cmp_score_frame, text='Score:')
        self.score_cmp = tk.StringVar()
        self.score_cmp.set(0)
        self.score_p1 = tk.StringVar()
        self.score_p1.set(0)
        self._p1_score = tk.Label(self._p1_score_frame,
                                  textvariable=self.score_p1, bg='white')
        self._p1_score_label.grid(row=0, column=0)
        self._cmp_score = tk.Label(self._cmp_score_frame,
                                   textvariable=self.score_cmp, bg='white')
        self._cmp_score_label.grid(row=0, column=0)
        self._p1_score.grid(row=0, column=1)
        self._cmp_score.grid(row=0, column=1)
        # dice
        self._dice_frame = tk.Frame(self, bg="white")
        self._quit_frame = tk.Frame(self)
        self._time_frame = tk.Frame(self)
        self._time_label = tk.Label(self._time_frame, text="", width=10,
                                    relief="sunken")
        self._time_label.grid(row=0, column=0)
        self._user_frame = tk.Frame(self, bd=2, bg="light blue")
        # user and computer input windows
        self._guess1_frame = tk.Frame(self, bd=2, bg="red")
        self._guess2_frame = tk.Frame(self, bd=2, bg="green")
        self._computer = tk.Label(self._guess1_frame, text='Computer')
        self._user = tk.Label(self._guess2_frame, text='Player 1')
        self._computer_text = tk.Text(self._guess1_frame, width=10,
                                      height=25, bg='white', bd=2)
        self._user_text = tk.Text(self._guess2_frame, width=10,
                                  height=25, bg='white', bd=2)
        self.user_box = tk.Entry(self._user_frame, width=10, bg='white', bd=2)
        self.input()
        self._game = Match()
        self.board_create()
        self.terms_conditions()

    # terms_conditions fn is the into popup with
    def terms_conditions(self):
        self.tandc = tk.Toplevel(bg="royalblue")
        self.update_idletasks()  # Update requested size
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) / 2
        self.tandc.geometry("%dx%d%+d%+d" % (350, 350, 665, 270))
        self.tandc.wm_title("BOGGLE")
        self.tandc.lift(aboveThis=self)
        self.message = "BOGGLE!\nThe object of this game is to\nscore " \
                       "more points than the computer\nbefore the timer" \
                       " runs out.\n\nYou’ve got 180 seconds to find" \
                       "\nand enter as many words as you\ncan identify" \
                       " on the cubes.\nUse as many of the letters as" \
                       " you can, the\nlonger the word, the higher" \
                       " your score.\n\nThe computer will find a word" \
                       "\nby default every 7 seconds.\n\nThis game was" \
                       " written for and is to be used\nfor student" \
                       " learning purposes only\n\nHasbro Gaming," \
                       " Boggle, and all\nrelated terms are trademarks" \
                       " of Hasbro.\nhttp://www.hasbrotoyshop.com/en/htsusa"
        self.termsandconditions = tk.Label(self.tandc, text=self.message,
                                           anchor=tk.CENTER,
                                           justify=tk.CENTER,
                                           wraplength=500,
                                           font=("Arial 10 bold"),
                                           fg="black", bg="steel blue")
        self.termsandconditions.pack(side="top", pady=10)
        self.terms_conditions_button = tk.Button(self.tandc, text="OK",
                                                 width=4, height=1,
                                                 font=("Arial 10 bold"),
                                                 fg="black",
                                                 command=self.tandc.destroy)
        self.terms_conditions_button.pack(side="top")
        self.tandc.focus_force()
        self.wait_window(self.tandc)

        # def select_wordlist(self):
        # from tkinter import filedialog
        # self.wordlist = filedialog.askopenfilename()

    # fn is used by computer and player to display valid guesses
    def insert_word(self, textobj, word):
        textobj.configure(state="normal")  # allow to write into field
        textobj.insert(tk.INSERT, word)
        self.remain.set(len(self._game.valid))
        textobj.configure(state="disabled")

    # fn this function will populate the 16 dice and call the game to start
    def board_create(self):
        self.dice_start = []
        self.add_dice_start()
        self.d_labels = []
        self._taken = []
        self._quit = []
        self.add_quit()
        self.add_dice()
        self.start_game()

    # this fn will set countdown timer and put curser in the box
    # where user will guess words
    def _start_(self):
        self.turn_delay = self._time_slider.get() * 1000
        self._option_frame.destroy()
        # will destroy the option frame when executed
        self.board_create()
        self.countdown(180)
        # gametime is set here
        self.start_game()
        self.user_box.configure(state="normal")
        self.user_box.focus_set()
        self._option_frame2.grid(row=6, column=5)
        self.foe_tracker = self.after(self.turn_delay, self.add_taken)
        # foe_tracker will hold ID of after fn

    # this function takes user choice for easy or hard and changes letters
    # and how the computerwill act. computer will randomly chose two words
    # easy selects lower point word higher will select the higher point word
    def set_difficulty(self, value):
        self.start_button.configure(state="normal")
        if value == 0:
            self.file = "alpha2/"
            self._game.difficulty = 1
        else:
            self.file = "alpha/"
            self._game.difficulty = 2

    # this function checks the time and shows the win/lose message
    # as well as displays any unguessed words if there are any
    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining
        if self.remaining <= 0:
            self._time_label.configure(text="Game Over", font=("Arial 15"))
            self.user_box.configure(state="disabled")
            self._option_frame2.destroy()
            # will destroy the option frame when executed
            if self._game.player1.get_score() == \
                    self._game.player2.get_score():
                self.user_tie.grid(row=1, column=5)
                self.end_msg = "Tie Game!"
            elif self._game.player1.get_score() > \
                    self._game.player2.get_score():
                self.user_win.grid(row=1, column=5)
                self.end_msg = "You Win!"
            elif self._game.player1.get_score() < \
                    self._game.player2.get_score():
                self.user_lost.grid(row=1, column=5)
                self.end_msg = "You Lost!"
            #            self._unguessed_frame.grid(row=4, column=1)
            r = 0
            c = 0
            top = tk.Toplevel()
            top.title("GAME OVER")
            self._unguessed_frame = tk.Frame(top)
            self._unguessed_frame.grid(row=0, column=0)
            tk.Label(self._unguessed_frame, text=self.end_msg,
                     font="Helvetica 26 bold italic").grid(row=0, column=0)
            tk.Label(self._unguessed_frame,
                     text="Unguessed Words:").grid(row=1, column=0)
            # print remaining points in unguessed words
            remaining_score = 0
            for word in self._game.valid:
                remaining_score += self._game.score(word)
            self._child_unguessed_frame = tk.Frame(self._unguessed_frame)
            while (self._game.valid):
                if r > 10:
                    r = 0
                    c += 1
                tk.Label(self._child_unguessed_frame,
                         text=(self._game.valid.pop())).grid(row=r, column=c)
                r += 1
            self._child_unguessed_frame.grid(row=2, column=0)
            tk.Label(self._unguessed_frame,
                     text="Unguessed Word Points:").grid(row=3, column=0)
            tk.Label(self._unguessed_frame, text=remaining_score).\
                grid(row=4, column=0)

            self.start_button = tk.Button(self._unguessed_frame,
                                          text="QUIT", font=("Arial", 15),
                                          bd=2, bg="royalblue",
                                          state="normal",
                                          command=self.quit)
            self.start_button.grid(row=5, column=0)

            try:
                self.after_cancel(self.foe_tracker)
                # if timer ends will try to close after
            except:
                pass
        else:
            self._time_label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

    # function used to place the dice pictures to the display
    def add_dice_start(self):
        file_path = self.file
        for row in self._game.board:
            for letter in row:
                file = file_path + letter.lower() + '.gif'
                image = tk.PhotoImage(file=file)
                self.dice_start.append(image)

    def add_dice(self):
        for i in range(0, self._game.size ** 2):
            label = tk.Label(self._dice_frame, image=self.dice_start[i],
                             bd=1, bg="black")
            self.d_labels.append(label)

    # fn that defines the quit button
    def add_quit(self):
        quit_button = tk.Button(self._quit_frame, text='Quit',
                                command=self.quit)
        self._quit.append(quit_button)

    # fn used to place all the frames
    def start_game(self):
        # Top
        self._p1_score_frame.grid(row=1, column=10)
        self._cmp_score_frame.grid(row=1, column=0)
        # far left
        self._computer_text.grid(row=3, column=1)
        self._guess1_frame.grid(row=5, column=0)
        # middle
        self._dice_frame.grid(row=5, column=5)
        # right
        self._guess2_frame.grid(row=5, column=10)
        self._user_text.grid(row=1, column=1)
        # guess box
        self._user_frame.grid(row=10, column=5)
        # bottom middle
        self._quit_frame.grid(row=11, column=5)
        self._time_frame.grid(row=0, column=5)
        for i, button in enumerate(self._quit):
            button.grid(row=0, column=i)
        row = 0
        col = 0
        for i, label in enumerate(self.d_labels):
            if i % self._game.size == 0:
                row += 1
                col = 0
            label.grid(row=row, column=col)
            col += 1
        self.focus_set()

    # fn used by computer and player to add to the list of taken words
    def add_taken(self):
        words = self._game.valid
        if words:
            word = choice(self._game.valid)
            alt_word = choice(self._game.valid)
            if (self._game.difficulty == 1):
                if self._game.score(alt_word) < self._game.score(word):
                    word = alt_word
                    # easy setting assign the lesser value word
            if (self._game.difficulty == 2):
                if self._game.score(alt_word) > self._game.score(word):
                    word = alt_word
                    # easy setting assign the greater value word
            if self._game.player_add(self._game.player2, word):
                self.score_cmp.set(self._game.player2.get_score())
                word += '\n'
                self.insert_word(self._computer_text, word)
                self._computer_text.see(tk.END)
                # foe_tracker will hold ID of after fn
                self.foe_tracker = self.after(self.turn_delay, self.add_taken)
        else:
            self.remaining = 0
            return

    # fn used to collect user guesses
    def input(self):
        user_label = tk.Label(self._user_frame, text="Enter Guess:")
        user_label.grid()
        self.user_box.bind('<Return>', self.get_input)
        self.user_box.grid(row=0, column=1)

    # fn used to process user guesses
    def get_input(self, event):
        _ = event
        word = self.user_box.get()
        word = word.upper()
        self.user_box.delete(first=0, last=tk.END)
        if self._game.player_add(self._game.player1, word):
            word += '\n'
            self.insert_word(self._user_text, word)
            self.score_p1.set(self._game.player1.get_score())
