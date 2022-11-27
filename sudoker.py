from enum import Enum
import json


table = [
    [0,9,2,  0,0,0,  3,5,0],
    [0,0,0,  3,0,2,  0,0,0],
    [0,0,1,  0,7,0,  9,0,0],
      
    [0,4,0,  9,0,3,  0,2,0],
    [9,0,3,  0,2,0,  8,0,1],
    [0,7,0,  1,0,8,  0,3,0],
      
    [0,0,7,  0,6,0,  1,0,0],
    [0,0,0,  8,0,4,  0,0,0],
    [0,3,5,  0,0,0,  4,9,0]
]

detailedTable = list()

state = Enum('state', ['error'])

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

def tableDetailer():
    detailedTable.clear()
    for r, row in enumerate(table):
        for c, number in enumerate(row):
            forbiddenNumbers = check_singleSquare(r, c)
            possibleNumbers = convertToPossibleNumbers(forbiddenNumbers)
            squareNumber = convertToSquareNumber(r,c)
            
            detailedTable.append({
                'number': number,
                'row': r,
                'column': c,
                'squareNumber': squareNumber,
                'isConstant': number != 0,
                'possibleNumbers': list(possibleNumbers) if number == 0 else [0],
                'forbiddenNumbers': list(forbiddenNumbers) if number == 0 else [0]
            })
    
    detailedTableJson = list()
    
    for i in detailedTable:
        detailedTableJson.append(json.dumps(i))
        
    check_oneChanceNumber()

def check_oneChanceNumber():
    somethingChange = False
    for square in detailedTable:
        if square["isConstant"] == False:
            if len(square['possibleNumbers']) == 1:
                somethingChange = True
                row = square['row']
                column = square['column']
                newNumber = square['possibleNumbers'][0]
                table[row][column] = newNumber
                # print(row, column)
                # print(f"is now: {newNumber}")

    if somethingChange:
        tableDetailer()
    else:
        print(table)
        return
    
def check_logicError(numbers):
    for number in numbers:
        if numbers.count(number) >= 2:
            return True
    return False

def check_Line(line):
    forbiddenNumbers = list()
    for square in table[line]:
        if(square != 0):
            forbiddenNumbers.append(square)
    if check_logicError(forbiddenNumbers) == False:
        return forbiddenNumbers
    else:
        return state.error

def check_Column(column):
    forbiddenNumbers = list()
    for row in table:
        for i, square in enumerate(row):
            if i == column and square != 0:
                forbiddenNumbers.append(square)
        
    if check_logicError(forbiddenNumbers) == False:
        return forbiddenNumbers
    else:
        return state.error
    
def check_3x3Square(squareNumber):
    
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
    
    if check_logicError(forbiddenNumbers) == False:
        return forbiddenNumbers
    else:
        return state.error

def convertToSquareNumber(row, column):
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

def check_singleSquare(row, column):
    forbiddenNumbers = set()    
    squareNumber = convertToSquareNumber(row, column)
      
    # print(row,",",column)
    # print(f'squareNumber: {squareNumber}')
    forbiddenNumbers.update( set(check_3x3Square(squareNumber)) )
    # print(f'3x3 square: {forbiddenNumbers}')
    forbiddenNumbers.update( set(check_Column(column)) )
    # print(f'column: {forbiddenNumbers}')
    forbiddenNumbers.update( set(check_Line(row)) )
    # print(f'line: {forbiddenNumbers}')
    forbiddenNumbers = list(forbiddenNumbers)    
    # print(f'{forbiddenNumbers}')
    # print("-----------------")   
    
    return forbiddenNumbers

def convertToPossibleNumbers(forbiddenNumbers):
    allNumbers = {1,2,3,4,5,6,7,8,9}
    forbiddenNumbers = set(forbiddenNumbers)
    possibleNumbers = allNumbers.difference(forbiddenNumbers)
        
    return possibleNumbers
   
if __name__ == '__main__':
    
    # tableMaker()
    # tableDetailer()
    # check_Column(0)
    # check_3x3Square(2)
    # check_singleSquare(3,0)