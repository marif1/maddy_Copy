import tkinter as tk
from checkers import Checkers
from hangman import Hangman, call_pack, call_unpack
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
# game1_radio = tk.Radiobutton(root, text="Play Hangman", variable=radio, value=1, command=play_hangman).place(x=200, y=400)
# game2_radio = tk.Radiobutton(root, text="Play Snake", variable=radio, value=2, command=play_snake).place(x=200, y=450)
# game3_radio = tk.Radiobutton(root, text="Play Checkers", variable=radio, value=3, command=play_checkers).place(x=200,y=500)

# Define a custom font
custom_font = ("Helvetica", 12)

# Create radio buttons with button-like style
game1_radio = tk.Radiobutton(root, text="Play Hangman", variable=radio, value=1, command=play_hangman, font=custom_font, bg="lightblue", relief="raised").place(x=200, y=400)
game2_radio = tk.Radiobutton(root, text="Play Snake", variable=radio, value=2, command=play_snake, font=custom_font, bg="lightgreen", relief="raised").place(x=200, y=450)
game3_radio = tk.Radiobutton(root, text="Play Checkers", variable=radio, value=3, command=play_checkers, font=custom_font, bg="lightcoral", relief="raised").place(x=200, y=500)



checkers_canvas_widget = tk.Canvas(root, width=400, height=400)
checkers_game = Checkers(checkers_canvas_widget)

snake_canvas_widget = tk.Canvas(root, width=400, height=400, bg="black")
snake_game = Snake(root,snake_canvas_widget)

# Define a custom font for the button
button_font = ("Helvetica", 12)

# Create a restart button with style
restart_button = tk.Button(root, text="Restart Game", command=snake_game.restart_game, font=button_font, bg="lightgray", relief="raised")
restart_button.place(x=400, y=600)


# Hangman must be last otherwise it bombs out
Hangman(root)

root.mainloop()
