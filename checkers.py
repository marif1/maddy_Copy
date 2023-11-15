"""
File: checkers.py
Authors: William Turner
Brief: Implementation of checkers using tkinter GUI
Date: 2023/10/14
"""

# OpenAI's ChatGPT was utilized to assist in the creation of this program

import tkinter as tk

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 8
SQUARE_SIZE = WIDTH // GRID_SIZE
WHITE = "white"
BLACK = "black"
RED = "red"
GREEN = "#008000"
BEIGE = "#daa06d"
P1 = 1  # Black player
P2 = 2  # White player


# Checkers classs
class Checkers:

    # the_canvas_window is a canvas widget created in main specifically for checkers and passed in via call
    def __init__(self, the_canvas_window):
        self.board = self.init_board()
        self.selected_piece = None
        self.jump_in_progress = False
        self.current_player = P1
        self.canvas = the_canvas_window
        self.canvas.bind("<Button-1>", self.select_square)
        self.draw_board()

    # Initialize 2D list for board
    def init_board(self):
        board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        
        # Place black pieces (player 1)
        for row in range(GRID_SIZE - 3, GRID_SIZE):
            for col in range(GRID_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = P1

        # Place white pieces (player 2)
        for row in range(3):
            for col in range(GRID_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = P2
        return board

    # Handle user selecting a square/piece
    def select_square(self, event):
        x, y = event.x, event.y
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE

        # If clicked square is not empty and belongs to current player
        if self.selected_piece is None:
            if self.board[row][col] == self.current_player:
                self.selected_piece = (row, col)
            self.draw_board()
        else:
            # Deselect piece if it's clicked again
            if (row, col) == self.selected_piece: 
                self.selected_piece = None
            # Select new piece if clicked square belongs to current player    
            elif self.board[row][col] == self.current_player: 
                self.selected_piece = (row, col)
            else:
                # Attempt to move the selected piece to the clicked square
                if self.move_piece((row, col)):
                    if self.can_jump(self.selected_piece):
                        self.jump_in_progress = True
                        self.selected_piece = (row, col)
                    else:
                        self.jump_in_progress = False
                        self.selected_piece = None

            self.draw_board()

    # Handle movement of pieces
    def move_piece(self, end_pos):
        row, col = end_pos

        is_valid, jumped_piece = self.is_valid_move(end_pos)

        if is_valid:
            self.board[row][col] = self.current_player
            self.board[self.selected_piece[0]][self.selected_piece[1]] = 0
            if jumped_piece is not None:
                self.board[jumped_piece[0]][jumped_piece[1]] = 0
            self.current_player = P1 if self.current_player == P2 else P2
            
        if self.jump_in_progress:
            # If a jump is in progress, check if the current player can make another jump.
            if self.can_jump(end_pos):
                self.selected_piece = end_pos  # Set the new selected piece
                return True
            else:
                self.jump_in_progress = False  # Reset jump_in_progress
        # else:
        #     self.jump_in_progress = False  # Reset jump_in_progress

        self.selected_piece = None
        self.draw_board()
        return True

    # Check if selected end position is valid
    def is_valid_move(self, end_pos):
        row_start, col_start = self.selected_piece
        row_end, col_end = end_pos

        # Selected piece belongs to current player
        if self.board[row_start][col_start] != self.current_player:
            return False, None

        # Board boundaries
        if row_end < 0 or row_end >= GRID_SIZE or col_end < 0 or col_end >= GRID_SIZE:
            return False, None

        # End position is empty square
        if self.board[row_end][col_end] != 0:
            return False, None

        # Set play direction
        if self.current_player == P1:
            move_direction = -1
        else:
            move_direction = 1

        # Regular move
        if row_end == row_start + move_direction and abs(col_end - col_start) == 1:
            return True, None

        # Jump move
        if row_end == row_start + 2 * move_direction and abs(col_end - col_start) == 2:
            # Position of jumped square
            jumped_row = (row_start + row_end) // 2
            jumped_col = (col_start + col_end) // 2
            # If there's a piece to jump over and destination is empty
            if self.board[jumped_row][jumped_col] == (3 - self.current_player):
                return True, (jumped_row, jumped_col)
            
        return False, None

    def can_jump(self, start_pos):
        if start_pos is None:
            return False
        
        row, col = start_pos
        for row_offset, col_offset in [(2, -2), (2, 2)] if self.current_player == P1 else [(-2, -2), (-2, 2)]:
            new_row = row + row_offset
            new_col = col + col_offset
            if self.is_valid_move((new_row, new_col)):
                return True
        return False

    # Handle all graphics - draws board and pieces
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Board squares
                color = BEIGE if (row + col) % 2 == 0 else GREEN
                self.canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE, (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, fill=color)
                # Red selection outline 
                if self.selected_piece is not None and (row, col) == self.selected_piece:
                    self.canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE, (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, outline=RED, width=2)
                # Black pieces
                if self.board[row][col] == P1:
                    self.canvas.create_oval(col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5, (col + 1) * SQUARE_SIZE - 5, (row + 1) * SQUARE_SIZE - 5, fill=BLACK)
                # White pieces
                elif self.board[row][col] == P2:
                    self.canvas.create_oval(col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5, (col + 1) * SQUARE_SIZE - 5, (row + 1) * SQUARE_SIZE - 5, fill=WHITE)

    def check_win(self):
        opponent = P1 if self.current_player == P2 else P2

        # Check if the opponent has no pieces remaining
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == opponent:
                    return False

        # Check if the opponent can move any piece
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == self.current_player:
                    if self.can_jump((row, col)):
                        return False  # The opponent can still jump
                    # Check regular moves
                    for row_offset, col_offset in [(1, -1), (1, 1)] if self.current_player == P1 else [(-1, -1), (-1, 1)]:
                        new_row = row + row_offset
                        new_col = col + col_offset
                        if self.is_valid_move((new_row, new_col))[0]:
                            return False  # The opponent can still make a regular move

        # If no opponent pieces left or they can't move, the current player wins
        tk.messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
        #self.root.quit()  # Exit the main loop when a player wins
        return True      

    # def run(the_root_window):
    #     the_root_window.mainloop()

'''
These are used to play the game from the main file.
Uncomment these if you need to debug the checkers game itself
'''

# checker_game = Checkers()
# checker_game.run()