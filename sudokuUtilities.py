class sudokuUtilities:
    def __init__(self) -> None:
        pass
    def convertToSquareNumber(self, row, column):
        squareNumber = 0
        
        if row < 3:
            if column < 3:
                squareNumber = 0
            elif column < 6:
                squareNumber = 1
            else:
                squareNumber = 2
        elif row < 6:
            if column < 3:
                squareNumber = 3
            elif column < 6:
                squareNumber = 4
            else:
                squareNumber = 5
        else:
            if column < 3:
                squareNumber = 6
            elif column < 6:
                squareNumber = 7
            else:
                squareNumber = 8
                
        return squareNumber
    
    def printBeautySudoku(self, table):
        sudokuText = '['
        separators = [2, 5]
        for r, row in enumerate(table):
            sudokuText += '\n\t['
            for c, number in enumerate(row):
                sudokuText += str(number)
                if c != 8:
                    sudokuText += ','
                else:
                    sudokuText += ']'
                    if r != 8:
                        sudokuText += ','
                        
                if c in separators:
                    sudokuText += '\t'
            if table.index(row) in separators:
                sudokuText += '\n'
        sudokuText += '\n]'
        
        return print(sudokuText)