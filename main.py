import tkinter as tk
from checkers import Checkers
from hangman import Hangman, call_pack,call_unpack
from snake import Snake


game_running = False  # Flag to track whether a game is currently running


root = tk.Tk()
root.title("Team Pheonix")
root.geometry("900x700")
root.state('zoomed') # Defaults to maximized view

# Each function will start the selected game and close all other games
def play_hangman():
    call_pack()
    checkers_canvas_widget.pack_forget()
    snake_canvas_widget.pack_forget()

def play_snake():
    call_unpack()
    checkers_canvas_widget.pack_forget()
    snake_canvas_widget.pack(pady=100)

def play_checkers():
    call_unpack()
    checkers_canvas_widget.pack(pady=100)
    snake_canvas_widget.pack_forget()


radio = tk.IntVar()

#Radio buttons to play each game, 
game1_radio = tk.Radiobutton(root, text="Play Hangman", variable=radio, value=1, command=play_hangman).place(x=650, y=800)
game2_radio = tk.Radiobutton(root, text="Play Snake", variable=radio, value=2, command=play_snake).place(x=650, y=820)
game3_radio = tk.Radiobutton(root, text="Play Checkers", variable=radio, value=3, command=play_checkers).place(x=650,y=840)


checkers_canvas_widget = tk.Canvas(root, width=400, height=400)
checkers_game = Checkers(checkers_canvas_widget)

snake_canvas_widget = tk.Canvas(root, width=400, height=400, bg="black")
snake_game = Snake(root,snake_canvas_widget)

# Used to reset the snake game, we need to 
restart_button = tk.Button(root, text="Restart Game", command=snake_game.restart_game).place(x=850,y=800)

# Hangman must be last otherwise it bombs out
Hangman(root)

root.mainloop()
