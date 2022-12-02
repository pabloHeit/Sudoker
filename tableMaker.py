import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import *
from functools import partial
from sudoker import sudokuSolver, sudokuUtilities
from asyncore import read
from table import table

class tableMaker(tk.Tk):
    def __init__(self, prefabTable = None):
        super().__init__()
        self.utilities = sudokuUtilities()
        self.title("Sudoku Board")
        self.prefabTable = prefabTable
        self.sudokuTable = []
        self.formatedSudokuTable = []
        self.cells = {}        
        self.create_sudoku_board()
        self.resizable(height = 0, width = 0)
        
        button = tk.Button(
            master              = self,
            text                = 'Print board',
            font                = font.Font(size=25, weight="bold"),
            fg                  = "black",
            highlightbackground = "lightblue",
            relief              = "solid",
            command             = self.printBoard
        )
        
        button2 = tk.Button(
            master              = self,
            text                = 'Solve sudoku',
            font                = font.Font(size=25, weight="bold"),
            fg                  = "black",
            highlightbackground = "lightblue",
            relief              = "solid",
            command             = self.solveSudoku
        )
        button.pack()
        button2.pack()
    
    def create_sudoku_board(self):
        grid_frame =  tk.Frame(master=self)
        grid_frame.pack()
        buttonRow = 0       
        for row in range(1,10):
            buttonColumn = 0       
            self.rowconfigure(row, weight=0, minsize=25)
            self.columnconfigure(row, weight=0, minsize=25)
            for column in range(1,10):
                if self.prefabTable != None and self.prefabTable[row-1][column-1] != 0:
                    number = self.prefabTable[row-1][column-1]
                else: 
                    number = ''
                    
                button = tk.Button(
                    master = grid_frame,
                    text = number,
                    font = font.Font(size=25, weight="bold"),
                    fg = "black",
                    width = 3,
                    height = 1,
                    highlightbackground = "lightblue",
                    relief = "solid",
                    command = partial(self.increaseNumber, row,column)
                )
                button.bind("<Button-3>", partial(self.decreaseNumber, row, column))
                
                self.cells[(row-1)*9 + column] = button
                
                button.grid(
                    row     = row    + buttonRow,
                    column  = column + buttonColumn,
                    pady    = 2,
                    padx    = 2,
                )
                
                if column % 3 == 0 and column != 9:
                    buttonColumn += 1
                    spacer = tk.Label(master = grid_frame, text="         ")
                    spacer.grid(row=row, column=column + buttonColumn)    
                    
                if row % 3 == 0 and column == 9:
                    buttonRow += 1               
                    spacer = tk.Label(master = grid_frame, text=" ")
                    spacer.grid(row=row + buttonRow, column=0)
     
    def updateBoard(self):
        self.convertListToSudoku()
        for cell in self.cells.items():
            if self.sudokuTable[cell[0]-1] != 0:
                cell[1]['text'] = self.sudokuTable[cell[0]-1]
            else:
                cell[1]['text'] = ''
                                      
    def increaseNumber(self, row, column):
        button = self.cells[(row-1)*9 + column]
        
        number = int(button['text']) + 1  if button['text'] != '' else 1
        
        if number >= 10:
            number = ''
        button['text'] = number        
        
    def decreaseNumber(self, row, column, useless):
        button = self.cells[(row-1)*9 + column]
        
        number = int(button['text']) - 1  if button['text'] != '' else 9
        
        if number <= 0:
            number = ''
        button['text'] = number        

    def convertSudokuToList(self):
        self.formatedSudokuTable.clear()
        for row in range(9):
            self.formatedSudokuTable.append(list())            
        
        row = 0
        for i, button in enumerate(self.cells.items()):
            if button[1]['text'] != '':
                self.formatedSudokuTable[row].append(int(button[1]['text']))
            else:
                self.formatedSudokuTable[row].append(0)
            if (i+1)% 9 == 0:
                row += 1 

    def convertListToSudoku(self):
        self.sudokuTable.clear()
        for row in self.formatedSudokuTable:
            for number in row:
                self.sudokuTable.append(number)

    def printBoard(self):
        self.convertSudokuToList()
        self.utilities.printBeautySudoku(self.formatedSudokuTable)
    
    def solveSudoku(self):
        self.convertSudokuToList()
        print(self.formatedSudokuTable)
        sudoku = sudokuSolver()
        sudoku.solveSudoku(self.formatedSudokuTable)
        self.updateBoard()
        
if __name__ == '__main__':
    board = tableMaker(table)
    board.mainloop()
    
    