import tkinter as tk
from tkinter import ttk
from itertools import cycle
from tkinter import font
from tkinter import *

from functools import partial

class sudokuSolver(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Board")
        self.cells = {}
        self.create_sudoku_board()
        self.resizable(height = 0, width = 0)
    
    def create_sudoku_board(self):
        grid_frame =  tk.Frame(master=self)
        grid_frame.pack()

        for row in range(9):
            self.rowconfigure(row, weight=0, minsize=25)
            self.columnconfigure(row, weight=0, minsize=25)
            for column in range(9):
                button = tk.Button(
                    master = grid_frame,
                    text = '',
                    font = font.Font(size=25, weight="bold"),
                    fg = "black",
                    width = 3,
                    height = 1,
                    highlightbackground = "lightblue",
                    relief = "solid",
                    command= partial(self.increaseNumber, row,column)
                )
                # button.bind("<Button-2>", partial(self.decreaseNumber, row,column))
                button.bind("<Button-3>", partial(self.decreaseNumber, row, column))
                
                self.cells[row*9+column+1] = button
                button.grid(
                    row=row,
                    column=column,
                    padx=2,
                    pady=2,
                )
                
    def increaseNumber(self, row, column):
        button = self.cells[row*9+column+1]
        
        number = int(button['text']) + 1  if button['text'] != '' else 1
        
        if number >= 10:
            number = ''
        button['text'] = number        
        
    def decreaseNumber(self, row, column, useless):
        button = self.cells[row*9+column+1]
        
        number = int(button['text']) - 1  if button['text'] != '' else 9
        
        if number <= 0:
            number = ''
        button['text'] = number        

def main():
    board = sudokuSolver()
    board.mainloop()

if __name__ == '__main__':
    main()