import random
from enum import Enum
from sudokuUtilities import sudokuUtilities
from table import table

class sudokuSolver:
    def __init__(self):
        self.table = []
        self.branchedTable = []
        self.detailedTable = list()
        self.branchedDetailedTable = list()
        self.state = Enum('state', ['error'])
        self.branch = Enum('branch', ['oneChance', 'finished', 'needBranch'])
        self.changes = 0
        self.bigSquare_Changes = 0
        self.line_Changes = 0
        self.column_Changes = 0
        self.utilities = sudokuUtilities()
    
    def solveSudoku(self, table):
        self.table = table
        self.detailedTable = self.create_detailedTable(self.table)
        if self.check_logicError():
            return self.stopSolving()
        
        while True:
            if self.check_isFinished() == False:
                while True:
                    somethingChange = self.check_all_OneChance()
                    if somethingChange == False:
                        break
                    elif somethingChange == self.state.error:
                        self.stopSolving()
                        break
                # self.utilities.printBeautySudoku(self.table)
                    
                branching = self.startBranching()
                if branching == self.branch.finished:
                    break
                if branching == self.branch.needBranch:
                    print("need sub-branch")
                    self.utilities.printBeautySudoku(self.branchedTable)
                    break
                    
                if branching == self.state.error:
                    self.stopSolving()
                    # self.utilities.printBeautySudoku(self.branchedTable)
                    break
                if branching == self.branch.oneChance:
                    print("returning to logic")
                    pass
            else:
                break
        
        return self.table
        
    def startBranching(self):
        self.branchedTable = []
        for row in self.table:
            self.branchedTable.append(row.copy())
            
        self.branchedDetailedTable = self.create_detailedTable(self.branchedTable, True)
        
        changedCell_info = self.find_MostPossibleCell()
        
        row = changedCell_info['row']
        column = changedCell_info['column']
        changedCell = self.branchedDetailedTable[row*9 + column]
        realChangedCell = self.detailedTable[row*9 + column]
        number = int(changedCell['possibleNumbers'][0])
        
        self.branchedTable[row][column] = number
        self.branchedDetailedTable[row*9 + column]['number'] = number
        
        tableDetailer = self.tableDetailer(True)
        if tableDetailer == self.state.error:
            return self.state.error
        
        while True:
            somethingChange = self.check_all_OneChance(True)
            
            if somethingChange == False:
                if self.check_isFinished(True):
                    return self.branch.finished
                else:
                    return self.branch.needBranch
                
            if somethingChange == self.state.error:
                realChangedCell['possibleNumbers'].pop(0)
                break
            
        if len(realChangedCell['possibleNumbers']) == 1:
            self.table[row][column] = realChangedCell['possibleNumbers'][0]
            self.branchedDetailedTable.clear()
            self.branchedTable.clear()
            return self.branch.oneChance        
        return False
    
    def stopSolving(self):
        print('Imposible sudoku')
    
    def create_detailedTable(self, table, isBranch = False):
        detailedTable = list()
        if self.check_logicError():
           return self.state.error
        for r, row in enumerate(table):
            for c, number in enumerate(row):
                if self.check_singleSquare(r,c, isBranch) != self.state.error:
                    forbiddenNumbers = self.check_singleSquare(r,c, isBranch)
                else:
                    return self.stopSolving()
                possibleNumbers = self.convertToPossibleNumbers(forbiddenNumbers)
                squareNumber = self.utilities.convertToSquareNumber(r,c)
                
                detailedTable.append({
                    'number': number,
                    'row': r,
                    'column': c,
                    'squareNumber': squareNumber,
                    'isConstant': number != 0,
                    'possibleNumbers': list(possibleNumbers) if number == 0 else [0],
                    'forbiddenNumbers': list(forbiddenNumbers) if number == 0 else [0]
                })
        return detailedTable
    
    def tableDetailer(self, isBranch = False):
        
        detailedTable = self.branchedDetailedTable if isBranch else self.detailedTable
        table = self.branchedTable if isBranch else self.table
        
        if self.check_logicError(isBranch):
            print('Error en tableDetailer')
            return self.state.error
        
        for r, row in enumerate(table):
            for c, number in enumerate(row):                
                detailedSquare = detailedTable[(r*9 + c)]
                if self.check_singleSquare(r,c, isBranch) != self.state.error:
                    forbiddenNumbers = self.check_singleSquare(r,c, isBranch)
                else:
                    return self.stopSolving()
                possibleNumbers = self.convertToPossibleNumbers(forbiddenNumbers)
                
                detailedSquare['number'] = number
                detailedSquare['isConstant'] = number != 0 and not isBranch
                detailedSquare['possibleNumbers'] = list(possibleNumbers) if number == 0 else [0]
                detailedSquare['forbiddenNumbers'] = list(forbiddenNumbers) if number == 0 else [0]
   
    def check_logicError(self, isBranch = False):
        
        table = self.branchedTable if isBranch else self.table
        squareNumbers = list()
        for square in range(9):
            squareNumbers.append(list())
            
        for r, row in enumerate(table):
            for c, number in enumerate(row):
                squareNumber = self.utilities.convertToSquareNumber(r,c)
                squareNumbers[squareNumber].append(number) 
        
        for i, square in enumerate(squareNumbers):
            for number in square:
                if number != 0 and square.count(number) >= 2:
                    return True
                
        for row in table:
            for number in row:
                if number != 0 and row.count(number) >= 2:
                    return True
                
        columnNumbers = list()
        for column in range(9):
            columnNumbers.append(list())
            
        for row in table:
            for i, number in enumerate(row):
                columnNumbers[i].append(number)
        
        for column in columnNumbers:
            for number in column:
                if number != 0 and columnNumbers.count(number) >= 2:
                    return True

        return False

    def check_Line(self, line, isBranch = False):
        table = self.branchedTable if isBranch else self.table
        
        forbiddenNumbers = list()
        for square in table[line]:
            if(square != 0):
                forbiddenNumbers.append(square)
        if self.check_logicError() == False:
            return forbiddenNumbers
        else:
            return self.state.error

    def check_Column(self, column, isBranch = False):
        table = self.branchedTable if isBranch else self.table
        
        forbiddenNumbers = list()
        for row in table:
            for i, square in enumerate(row):
                if i == column and square != 0:
                    forbiddenNumbers.append(square)
            
        if self.check_logicError() == False:
            return forbiddenNumbers
        else:
            return self.state.error
        
    def check_3x3Square(self, squareNumber, isBranch = False):
        table = self.branchedTable if isBranch else self.table
        
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
                if table[row][column] != 0:
                    forbiddenNumbers.append(table[row][column])
        if self.check_logicError() == False:
            return forbiddenNumbers
        else:
            return self.state.error

    def check_all_OneChance(self, isBranch = False):
        somethingChange = [False, False, False]
        somethingChange[0] = self.check_All3x3Square_OneChance(isBranch)
        somethingChange[1] = self.check_AllColumn_OneChance(isBranch)
        somethingChange[2] = self.check_AllLine_OneChance(isBranch)
        if True in somethingChange:
            while True in somethingChange:
                self.check_oneChanceNumber(isBranch)
                tableDetailer = self.tableDetailer(isBranch)
                if tableDetailer == self.state.error:
                    return self.state.error
                somethingChange = [False, False, False]
                somethingChange[0] = self.check_All3x3Square_OneChance(isBranch)
                somethingChange[1] = self.check_AllColumn_OneChance(isBranch)
                somethingChange[2] = self.check_AllLine_OneChance(isBranch)
        else:
            return False
        return True
    
    def check_3x3Square_OneChance(self, squareNumber, isBranch = False):
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
        
        table = self.branchedDetailedTable if isBranch else self.detailedTable
        
        for square in table:
            if square['squareNumber'] == squareNumber:
                if square['number'] == 0:
                    for number in square['possibleNumbers']:
                        possibleNumbers[str(number)] += 1
                        
        oneChanceNumbers = list()
        for possibleNumber, repetitions in possibleNumbers.items():
            if repetitions == 1:
                oneChanceNumbers.append(int(possibleNumber))
        
        for oneChanceNumber in oneChanceNumbers:
            for square in table:
                if square['squareNumber'] == squareNumber:
                    if oneChanceNumber in square['possibleNumbers']:
                        self.bigSquare_Changes += 1
                        somethingChange = True
                        square['possibleNumbers'] = [oneChanceNumber]
                        break
        return somethingChange

    def check_All3x3Square_OneChance(self, isBranch):
        somethingChange = list()
        for i in range(0,9):
            somethingChange.append(list())
        for i in range(0,9):
            somethingChange[i] = self.check_3x3Square_OneChance(i, isBranch)
        
        somethingChange = True if True in somethingChange else False
        
        return somethingChange
    
    def check_Line_OneChance(self, row, isBranch): 
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
        
        table = self.branchedDetailedTable if isBranch else self.detailedTable

        for square in table:
            if square['row'] == row:
                for number in square['possibleNumbers']:
                    if square['number'] == 0:
                        possibleNumbers[str(number)] += 1
                        
        oneChanceNumbers = list()
        for possibleNumber, repetitions in possibleNumbers.items():
            if repetitions == 1:
                oneChanceNumbers.append(int(possibleNumber))
        for oneChanceNumber in oneChanceNumbers:
            for square in table:
                if square['row'] == row:
                    if oneChanceNumber in square['possibleNumbers']:
                        self.line_Changes += 1
                        somethingChange = True
                        square['possibleNumbers'] = [oneChanceNumber]
                        break
        
        return somethingChange

    def check_AllLine_OneChance(self, isBranch):
        somethingChange = list()
        for i in range(0,9):
            somethingChange.append(list())
            
        for i in range(0,9):
            somethingChange[i] = self.check_Line_OneChance(i, isBranch)

            
        somethingChange = True if True in somethingChange else False
        return somethingChange
            
    def check_column_OneChance(self, column, isBranch):
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
        
        table = self.branchedDetailedTable if isBranch else self.detailedTable
        
        for square in table:
            if square['column'] == column:
                if square['number'] == 0:
                    for number in square['possibleNumbers']:
                        possibleNumbers[str(number)] += 1
                        
        oneChanceNumbers = list()
        
        for possibleNumber, repetitions in possibleNumbers.items():
            if repetitions == 1:
                oneChanceNumbers.append(int(possibleNumber))
        
        for oneChanceNumber in oneChanceNumbers:
            for square in table:
                if square['column'] == column:
                    if oneChanceNumber in square['possibleNumbers']:
                        self.column_Changes += 1
                        somethingChange = True
                        square['possibleNumbers'] = [oneChanceNumber]                            
                        break
        return somethingChange

    def check_AllColumn_OneChance(self, isBranch):
        somethingChange = list()
        for i in range(0,9):
            somethingChange.append(list())
            
        for i in range(0,9):
            somethingChange[i] = self.check_column_OneChance(i, isBranch)
        
        somethingChange = True if True in somethingChange else False
        
        return somethingChange

    def check_singleSquare(self, row, column, isBranch):
        forbiddenNumbers = set()
        squareNumber = self.utilities.convertToSquareNumber(row, column)
        
        if self.check_3x3Square(squareNumber, isBranch) != self.state.error:
            forbiddenNumbers.update( set(self.check_3x3Square(squareNumber, isBranch)) )
        else:
            return self.state.error
        if self.check_Column(column) != self.state.error:
            forbiddenNumbers.update( set(self.check_Column(column, isBranch)) )
        else:
            return self.state.error
        if self.check_Line(row) != self.state.error:
            forbiddenNumbers.update( set(self.check_Line(row, isBranch)) )
        else:
            return self.state.error

        forbiddenNumbers = list(forbiddenNumbers)    
        
        return forbiddenNumbers

    def convertToPossibleNumbers(self, forbiddenNumbers):
        allNumbers = {1,2,3,4,5,6,7,8,9}
        forbiddenNumbers = set(forbiddenNumbers)
        possibleNumbers = allNumbers.difference(forbiddenNumbers)
            
        return possibleNumbers

    def check_oneChanceNumber(self, isBranch = False):
        somethingChange = False
        
        detailedTable = self.branchedDetailedTable if isBranch else self.detailedTable
        table = self.branchedTable if isBranch else self.table
        
        for square in detailedTable:
            if square["number"] == 0:
                if len(square['possibleNumbers']) == 1:
                    somethingChange = True
                    row = square['row']
                    column = square['column']
                    newNumber = square['possibleNumbers'][0]
                    table[row][column] = newNumber
        return somethingChange
    
    def find_MostPossibleCell(self):            
        mostPossibleCell = None
        for square in self.branchedDetailedTable:
            squarePosibilities = len(square['possibleNumbers'])
            if square['number'] == 0:
                if mostPossibleCell == None:                
                    mostPossibleCell = {
                        'row': square['row'],
                        'column': square['column'],
                        'countNumbers': squarePosibilities
                    }
                elif squarePosibilities <= mostPossibleCell['countNumbers']:
                    mostPossibleCell['row'] = square['row']
                    mostPossibleCell['column'] = square['column']
                    mostPossibleCell['countNumbers'] = squarePosibilities
                    
                    if mostPossibleCell['countNumbers'] == 2:
                        break
        return mostPossibleCell
    
    def check_isFinished(self, isBranch = False):
        
        table = self.branchedTable if isBranch else self.table
        
        for row in table:
            for square in row:
                if square == 0:
                    return False
        self.utilities.printBeautySudoku(table)
        self.changes = self.bigSquare_Changes + self.line_Changes + self.column_Changes
        print(f'The sudoku is solved ')
        print(f'Changes: {self.changes}')
        print(f'3x3 square: {self.bigSquare_Changes}')
        print(f'line Changes: {self.line_Changes}')
        print(f'Column Changes: {self.column_Changes}')
        self.utilities.printBeautySudoku(table)
        
        if isBranch == True:
            self.table = self.branchedTable
        
        return True

if __name__ == '__main__':
    sudolver = sudokuSolver()
    sudolver.solveSudoku(table)