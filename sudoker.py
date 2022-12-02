from enum import Enum
from sudokuUtilities import sudokuUtilities
from table import table

class sudokuSolver:
    def __init__(self):
        self.table = []
        self.detailedTable = list()
        self.state = Enum('state', ['error'])
        self.changes = 0
        self.bigSquare_Changes = 0
        self.line_Changes = 0
        self.column_Changes = 0
        self.utilities = sudokuUtilities()
         
    def solveSudoku(self, table):
        self.table = table
        print('sudokuSolver start to Check for errors')
        if self.check_logicError():
            return self.stopSolving()
        print('sudokuSolver start to solve the sudoku')
        self.tableDetailer()
        print('table detailed')
        while True:
            somethingChange = self.check_all_OneChance()
            if somethingChange == False:
                break
        return self.check_isFinished()
    
    def stopSolving(self):
        print('Imposible sudoku')
    
    def tableDetailer(self):
        self.detailedTable.clear()
        for r, row in enumerate(self.table):
            for c, number in enumerate(row):
                if self.check_singleSquare(r,c) != self.state.error:
                    forbiddenNumbers = self.check_singleSquare(r,c)
                else:
                    return self.stopSolving()
                possibleNumbers = self.convertToPossibleNumbers(forbiddenNumbers)
                squareNumber = self.utilities.convertToSquareNumber(r,c)
                
                self.detailedTable.append({
                    'number': number,
                    'row': r,
                    'column': c,
                    'squareNumber': squareNumber,
                    'isConstant': number != 0,
                    'possibleNumbers': list(possibleNumbers) if number == 0 else [0],
                    'forbiddenNumbers': list(forbiddenNumbers) if number == 0 else [0]
                })        
        # self.detailedTableJson = list()        
        # for i in self.detailedTable:
        #     self.detailedTableJson.append(json.dumps(i))        
    
    def check_logicError(self):

        
        for row in self.table:
            for number in row:
                if number != 0 and row.count(number) >= 2:
                    return True
                
        columnNumbers = list()
        for column in range(9):
            columnNumbers.append(list())
            
        for row in self.table:
            for i, number in enumerate(row):
                columnNumbers[i].append(number)
        
        for column in columnNumbers:
            for number in column:
                if number != 0 and columnNumbers.count(number) >= 2:
                    return True
                    
        return False

    def check_Line(self, line):
        forbiddenNumbers = list()
        for square in self.table[line]:
            if(square != 0):
                forbiddenNumbers.append(square)
        if self.check_logicError() == False:
            return forbiddenNumbers
        else:
            return self.state.error

    def check_Column(self, column):
        forbiddenNumbers = list()
        for row in self.table:
            for i, square in enumerate(row):
                if i == column and square != 0:
                    forbiddenNumbers.append(square)
            
        if self.check_logicError() == False:
            return forbiddenNumbers
        else:
            return self.state.error
        
    def check_3x3Square(self, squareNumber):
        forbiddenNumbers = list()
        startingRow = 0
        startingColumn = 0
        
        if squareNumber > 2:
            if squareNumber > 5:
                startingRow = 6
            else:
                startingRow = 3
        
        if squareNumber == 0 or squareNumber == 3 or squareNumber == 6:
            startingColumn = 0
        if squareNumber == 1 or squareNumber == 4 or squareNumber == 7:
            startingColumn = 3
        if squareNumber == 2 or squareNumber == 5 or squareNumber == 8:
            startingColumn = 6
        
        for row in range(startingRow, startingRow + 3):
            for column in range(startingColumn, startingColumn + 3):
                if self.table[row][column] != 0:
                    forbiddenNumbers.append(self.table[row][column])
        if self.check_logicError() == False:
            return forbiddenNumbers
        else:
            return self.state.error

    def check_all_OneChance(self):
        somethingChange = [False, False, False]
        somethingChange[0] = self.check_All3x3Square_OneChance()
        somethingChange[1] = self.check_AllColumn_OneChance()
        somethingChange[2] = self.check_AllLine_OneChance()
        
        if True in somethingChange:
            while True in somethingChange:
                self.tableDetailer()
                somethingChange = [False, False, False]
                somethingChange[0] = self.check_All3x3Square_OneChance()
                somethingChange[1] = self.check_AllColumn_OneChance()
                somethingChange[2] = self.check_AllLine_OneChance()
        else:
            return False
        return True
    
    def check_3x3Square_OneChance(self, squareNumber):
        somethingChange = False
        possibleNumbers = {
            '1':0,
            '2':0,
            '3':0,
            '4':0,
            '5':0,
            '6':0,
            '7':0,
            '8':0,
            '9':0
        }
        for square in self.detailedTable:
            if square['squareNumber'] == squareNumber:
                for number in square['possibleNumbers']:
                    if square['isConstant'] == False:
                        possibleNumbers[str(number)] += 1
                        
        oneChanceNumbers = list()
        for possibleNumber, repetitions in possibleNumbers.items():
            if repetitions == 1:
                oneChanceNumbers.append(int(possibleNumber))
        
        for oneChanceNumber in oneChanceNumbers:
            for square in self.detailedTable:
                if square['squareNumber'] == squareNumber:
                    if oneChanceNumber in square['possibleNumbers']:
                        self.bigSquare_Changes += 1
                        somethingChange = True
                        square['possibleNumbers'] = [oneChanceNumber]
                        self.check_oneChanceNumber()
                        break

        return somethingChange

    def check_All3x3Square_OneChance(self):
        somethingChange = list()
        for i in range(0,9):
            somethingChange.append(list())
            
        for i in range(0,9):
            somethingChange[i] = self.check_3x3Square_OneChance(i)
        
        somethingChange = True if True in somethingChange else False
        
        return somethingChange
    
    def check_Line_OneChance(self, row):
        somethingChange = False
        possibleNumbers = {
            '1':0,
            '2':0,
            '3':0,
            '4':0,
            '5':0,
            '6':0,
            '7':0,
            '8':0,
            '9':0
        }
        
        for square in self.detailedTable:
            if square['row'] == row:
                for number in square['possibleNumbers']:
                    if square['isConstant'] == False:
                        possibleNumbers[str(number)] += 1
                        
        oneChanceNumbers = list()
        for possibleNumber, repetitions in possibleNumbers.items():
            if repetitions == 1:
                oneChanceNumbers.append(int(possibleNumber))

        for oneChanceNumber in oneChanceNumbers:
            for square in self.detailedTable:
                if square['row'] == row:
                    if oneChanceNumber in square['possibleNumbers']:
                        self.line_Changes += 1
                        somethingChange = True
                        square['possibleNumbers'] = [oneChanceNumber]
                        self.check_oneChanceNumber()
                        break
        return somethingChange

    def check_AllLine_OneChance(self):
        somethingChange = list()
        for i in range(0,9):
            somethingChange.append(list())
            
        for i in range(0,9):
            somethingChange[i] = self.check_Line_OneChance(i)
        somethingChange = True if True in somethingChange else False
        return somethingChange
            
    def check_column_OneChance(self, column):
        somethingChange = False
        possibleNumbers = {
            '1':0,
            '2':0,
            '3':0,
            '4':0,
            '5':0,
            '6':0,
            '7':0,
            '8':0,
            '9':0
        }
        
        for square in self.detailedTable:
            if square['column'] == column:
                for number in square['possibleNumbers']:
                    if square['isConstant'] == False:
                        possibleNumbers[str(number)] += 1
                        
        oneChanceNumbers = list()
        
        for possibleNumber, repetitions in possibleNumbers.items():
            if repetitions == 1:
                oneChanceNumbers.append(int(possibleNumber))
        
        for oneChanceNumber in oneChanceNumbers:
            for square in self.detailedTable:
                if square['column'] == column:
                    if oneChanceNumber in square['possibleNumbers']:
                        self.column_Changes += 1
                        somethingChange = True
                        square['possibleNumbers'] = [oneChanceNumber]
                        self.check_oneChanceNumber()
                        break

        return somethingChange

    def check_AllColumn_OneChance(self):
        somethingChange = list()
        for i in range(0,9):
            somethingChange.append(list())
            
        for i in range(0,9):
            somethingChange[i] = self.check_column_OneChance(i)
        somethingChange = True if True in somethingChange else False
        return somethingChange

    def check_singleSquare(self, row, column):
        forbiddenNumbers = set()    
        squareNumber = self.utilities.convertToSquareNumber(row, column)
        
        if self.check_3x3Square(squareNumber) != self.state.error:
            forbiddenNumbers.update( set(self.check_3x3Square(squareNumber)) )
        else:
            return self.state.error
        if self.check_Column(column) != self.state.error:
            forbiddenNumbers.update( set(self.check_Column(column)) )
        else:
            return self.state.error
        if self.check_Line(row) != self.state.error:
            forbiddenNumbers.update( set(self.check_Line(row)) )
        else:
            return self.state.error

        forbiddenNumbers = list(forbiddenNumbers)    
        
        return forbiddenNumbers

    def convertToPossibleNumbers(self, forbiddenNumbers):
        allNumbers = {1,2,3,4,5,6,7,8,9}
        forbiddenNumbers = set(forbiddenNumbers)
        possibleNumbers = allNumbers.difference(forbiddenNumbers)
            
        return possibleNumbers

    def check_oneChanceNumber(self):
        somethingChange = False
        for square in self.detailedTable:
            if square["isConstant"] == False:
                if len(square['possibleNumbers']) == 1:
                    somethingChange = True
                    row = square['row']
                    column = square['column']
                    newNumber = square['possibleNumbers'][0]
                    self.table[row][column] = newNumber
        return somethingChange
    
    def check_isFinished(self):
        for row in self.table:
            for square in row:
                if square == 0:
                    print('The sudoku is not finished yet')
                    self.utilities.printBeautySudoku(self.table)
                    return False
        self.changes = self.bigSquare_Changes + self.line_Changes + self.column_Changes
        print(f'The sudoku is solved ')
        print(f'Changes: {self.changes}')
        print(f'3x3 square: {self.bigSquare_Changes}')
        print(f'line Changes: {self.line_Changes}')
        print(f'Column Changes: {self.column_Changes}')
        return self.utilities.printBeautySudoku(self.table)


if __name__ == '__main__':
    sudolver = sudokuSolver()
    sudolver.solveSudoku(table)