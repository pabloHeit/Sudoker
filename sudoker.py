from enum import Enum

class sudokuSolver:
    def __init__(self):
        self.table = []
        self.detailedTable = list()
        self.state = Enum('state', ['error'])
        self.changes = 0
        self.utilities = sudokuUtilities()
         
    def solveSudoku(self, table):
        self.table = table
        print('sudokuSolver start to solve the sudoku')
        self.tableDetailer()
        print('table detailed')
        
        iterations = 0
        while self.check_isFinished() == False:
            self.check_all_OneChance()
            iterations += 1
            if iterations >= 81:
                break
        return self.table
        
    def tableDetailer(self):
        self.detailedTable.clear()
        for r, row in enumerate(self.table):
            for c, number in enumerate(row):
                forbiddenNumbers = self.check_singleSquare(r,c)
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
    
    def check_logicError(self, numbers):
        for number in numbers:
            if numbers.count(number) >= 2:
                return True
        return False

    def check_Line(self, line):
        forbiddenNumbers = list()
        for square in self.table[line]:
            if(square != 0):
                forbiddenNumbers.append(square)
        if self.check_logicError(forbiddenNumbers) == False:
            return forbiddenNumbers
        else:
            return self.state.error

    def check_Column(self, column):
        forbiddenNumbers = list()
        for row in self.table:
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
        
        for row in range(startingRow, startingRow + 3):
            for column in range(startingColumn, startingColumn + 3):
                if self.table[row][column] != 0:
                    forbiddenNumbers.append(self.table[row][column])
        if self.check_logicError(forbiddenNumbers) == False:
            return forbiddenNumbers
        else:
            return self.state.error

    def check_all_OneChance(self):
        somethingChange = [False, False, False]
        somethingChange[0] = self.check_All3x3Square_OneChance()
        self.tableDetailer()
        somethingChange[1] = self.check_AllColumn_OneChance()
        self.tableDetailer()
        somethingChange[2] = self.check_AllLine_OneChance()
        self.tableDetailer()
        
        if True in somethingChange:
            while True in somethingChange:
                somethingChange = [False, False, False]
                somethingChange[0] = self.check_All3x3Square_OneChance()
                self.tableDetailer()
                somethingChange[1] = self.check_AllColumn_OneChance()
                self.tableDetailer()
                somethingChange[2] = self.check_AllLine_OneChance()
                self.tableDetailer()
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
                        somethingChange = True
                        square['possibleNumbers'] = [oneChanceNumber]
                        self.check_oneChanceNumber()
                        break

        return somethingChange

    def check_All3x3Square_OneChance(self):
        for i in range(0,9):
            somethingChange = self.check_3x3Square_OneChance(i)
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
                        somethingChange = True
                        square['possibleNumbers'] = [oneChanceNumber]
                        self.check_oneChanceNumber()
                        break
        return somethingChange

    def check_AllLine_OneChance(self):
        for i in range(0,9):
            somethingChange = self.check_Line_OneChance(i)
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
                        somethingChange = True
                        square['possibleNumbers'] = [oneChanceNumber]
                        self.check_oneChanceNumber()
                        break

        return somethingChange

    def check_AllColumn_OneChance(self):
        for i in range(0,9):
            somethingChange = self.check_column_OneChance(i)
        return somethingChange

    def check_singleSquare(self, row, column):
        forbiddenNumbers = set()    
        squareNumber = self.utilities.convertToSquareNumber(row, column)
        
        forbiddenNumbers.update( set(self.check_3x3Square(squareNumber)) )
        forbiddenNumbers.update( set(self.check_Column(column)) )
        forbiddenNumbers.update( set(self.check_Line(row)) )
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
                    return False
        print(f'The sudoku is solved ')
        return self.utilities.printBeautySudoku(self.table)

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
        sudokuText = ''
        separators = [2, 5]
        for row in table:
            for c, number in enumerate(row):
                sudokuText += str(number) + ' '
                if c in separators:
                    sudokuText += '\t'
            sudokuText += '\n'
            if table.index(row) in separators:
                sudokuText += '\n'
        
        return print(sudokuText)
    
""" table = [
    [0, 9, 2,    0, 0, 0,    3, 5, 0],
    [0, 0, 0,    3, 0, 2,    0, 0, 0],
    [0, 0, 1,    0, 7, 0,    9, 0, 0],
    
    [0, 4, 0,    9, 0, 3,    0, 2, 0],
    [9, 0, 3,    0, 2, 0,    8, 0, 1],
    [0, 7, 0,    1, 0, 8,    0, 3, 0],
    
    [0, 0, 7,    0, 6, 0,    1, 0, 0],
    [0, 0, 0,    8, 0, 4,    0, 0, 0],
    [0, 3, 5,    0, 0, 0,    4, 9, 0]
] """

if __name__ == '__main__':
    table = [
    [0, 9, 2,    0, 0, 0,    3, 5, 0],
    [0, 0, 0,    3, 0, 2,    0, 0, 0],
    [0, 0, 1,    0, 7, 0,    9, 0, 0],
    
    [0, 4, 0,    9, 0, 3,    0, 2, 0],
    [9, 0, 3,    0, 2, 0,    8, 0, 1],
    [0, 7, 0,    1, 0, 8,    0, 3, 0],
    
    [0, 0, 7,    0, 6, 0,    1, 0, 0],
    [0, 0, 0,    8, 0, 4,    0, 0, 0],
    [0, 3, 5,    0, 0, 0,    4, 9, 0]
]
    sudolver = sudokuSolver()
    sudolver.solveSudoku(table)