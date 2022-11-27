from enum import Enum
import json

class sudokuSolver:
    def __init__(self, table):
        self.table = table
        self.detailedTable = list()
        self.state = Enum('state', ['error'])
        self.changes = 0
        print('sudokuSolver instantiated')
        self.solveProcess()
        
    def solveProcess(self):
        print('sudokuSolver start to solve the sudoku')
        self.tableDetailer()
        print('table detailed')
        
        while self.check_isFinished() == False:
            while True:
                somethingChange = self.check_oneChanceNumber()
                self.tableDetailer()
                if somethingChange == False:
                    break
            print("First method is dead")
            
            if self.check_isFinished() == False:
                print(f'sudoku not finished, But this is the remain table')
                print(f'{table}')
                break
      
    def tableDetailer(self):
        self.detailedTable.clear()
        for r, row in enumerate(self.table):
            for c, number in enumerate(row):
                forbiddenNumbers = self.check_singleSquare(r, c)
                possibleNumbers = self.convertToPossibleNumbers(forbiddenNumbers)
                squareNumber = self.convertToSquareNumber(r,c)
                
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
    
    def check_logicError(self, numbers):
        for number in numbers:
            if numbers.count(number) >= 2:
                return True
        return False

    def check_Line(self, line):
        forbiddenNumbers = list()
        for square in table[line]:
            if(square != 0):
                forbiddenNumbers.append(square)
        if self.check_logicError(forbiddenNumbers) == False:
            return forbiddenNumbers
        else:
            return self.state.error

    def check_Column(self, column):
        forbiddenNumbers = list()
        for row in table:
            for i, square in enumerate(row):
                if i == column and square != 0:
                    forbiddenNumbers.append(square)
            
        if self.check_logicError(forbiddenNumbers) == False:
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
            
        # print(f'squareNumber: {squareNumber}')
        # print(f'startingRow: {startingRow}')
        # print(f'startingColumn: {startingColumn}')    
        
        for row in range(startingRow, startingRow + 3):
            for column in range(startingColumn, startingColumn + 3):
                if table[row][column] != 0:
                    forbiddenNumbers.append(table[row][column])
        # print(forbiddenNumbers)
        if self.check_logicError(forbiddenNumbers) == False:
            return forbiddenNumbers
        else:
            return self.state.error

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

    def check_singleSquare(self, row, column):
        forbiddenNumbers = set()    
        squareNumber = self.convertToSquareNumber(row, column)
        
        # print(row,",",column)
        # print(f'squareNumber: {squareNumber}')
        forbiddenNumbers.update( set(self.check_3x3Square(squareNumber)) )
        # print(f'3x3 square: {forbiddenNumbers}')
        forbiddenNumbers.update( set(self.check_Column(column)) )
        # print(f'column: {forbiddenNumbers}')
        forbiddenNumbers.update( set(self.check_Line(row)) )
        # print(f'line: {forbiddenNumbers}')
        forbiddenNumbers = list(forbiddenNumbers)    
        # print(f'{forbiddenNumbers}')
        # print("-----------------")   
        
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
                    self.changes += 1
                    row = square['row']
                    column = square['column']
                    newNumber = square['possibleNumbers'][0]
                    self.table[row][column] = newNumber
                    # print(row, column)
                    # print(f"is now: {newNumber}")
        return somethingChange

    def check_isFinished(self):
        for row in table:
            for square in row:
                if square == 0:
                    return False
        print(f'The sudoku is solved \n')
        print(f'{self.table}')

class tableMaker:
    def __init__(self):
        self.emptyTable = list()

        for r in range(0,9):
            self.row = list()
            for c in range(0,9):
                self.row.append(0)
            self.emptyTable.append(self.row)
    
    def addNumber(self, row, column, number):
        self.table = self.emptyTable.copy()
        self.table[row][column] = number               


table = [
    [0,8,9,  0,4,0,  2,7,0],
    [0,0,0,  0,7,0,  0,0,0],
    [3,0,0,  0,9,0,  0,0,6],
      
    [0,0,7,  4,0,5,  3,0,0],
    [6,0,0,  0,0,0,  0,0,4],
    [0,0,3,  9,0,1,  7,0,0],
      
    [4,0,0,  0,3,0,  0,0,9],
    [0,0,0,  0,1,0,  0,0,0],
    [0,9,2,  0,5,0,  1,8,0]
]

if __name__ == '__main__':
    sudolver = sudokuSolver(table)