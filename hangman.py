"""
File: hangman.py
Authors: Trevor Ralston
Brief: Implementation of hangman using tkinter
Date: 2023/11/7
ChatGPT was utilized to assist with implementing this program
"""

import tkinter as tk
import random

# List of words for the game
word_list = ["python", "hangman", "programming", "computer", "keyboard"]

# Initialize variables
selected_word = ""
guessed_word = []
attempts = 6


class Hangman:

    # main_tkinter is the tkinter (root) passed in from main
    def __init__(self, main_tkinter):
        global word_label, attempts_label, result_label, guess_entry, guess_button, new_game_button
        window = main_tkinter

        # Create labels, pack procedures are in a different function
        word_label = tk.Label(window, text="", font=("Arial", 20))
        attempts_label = tk.Label(window, text="", font=("Arial", 12))
        result_label = tk.Label(window, text="", font=("Arial", 14))

        # Create entry and buttons, pack procedures are in a different function
        guess_entry = tk.Entry(window, font=("Arial", 12))
        guess_button = tk.Button(window, text="Guess", command=self.guess_letter)
        new_game_button = tk.Button(window, text="New Game", command=self.new_game)

        self.new_game()
        window.mainloop()

    # Function to start a new game
    def new_game(self):
        global selected_word, guessed_word, attempts
        selected_word = random.choice(word_list)
        guessed_word = ["_"] * len(selected_word)
        attempts = 6
        self.update_display()
        guess_entry.config(state="normal")

    # Function to handle a guessed letter
    def guess_letter(self):
        global attempts
        letter = guess_entry.get().lower()
        guess_entry.delete(0, tk.END)
        if letter in selected_word:
            for i in range(len(selected_word)):
                if selected_word[i] == letter:
                    guessed_word[i] = letter
        else:
            attempts -= 1

        self.update_display()
        guess_entry.config(state="normal")

    # Function to update the display
    def update_display(self):
        word_label.config(text=" ".join(guessed_word))
        attempts_label.config(text=f"Attempts left: {attempts}")

        if "_" not in guessed_word:
            result_label.config(text="You win!")
            guess_entry.config(state="disabled")
        elif attempts == 0:
            result_label.config(text=f"You lose. The word was: {selected_word}")
            guess_entry.config(state="disabled")
        else:
            result_label.config(text="")

# Functions used to pack and unpack elements
def pack_hangman_elements():
    word_label.pack(pady=20)
    attempts_label.pack()
    result_label.pack()
    guess_entry.pack()
    guess_button.pack()
    new_game_button.pack()

def unpack_hangman_elements():
    word_label.pack_forget()
    attempts_label.pack_forget()
    result_label.pack_forget()
    guess_entry.pack_forget()
    guess_button.pack_forget()
    new_game_button.pack_forget()

# the functions only work properly if they're called using these
def call_pack():
    pack_hangman_elements()

def call_unpack():
    unpack_hangman_elements()
