from enum import Enum

table = [
    [0,9,2,0,0,0,3,5,0],
    [0,0,0,3,0,2,0,0,0],
    [0,0,1,0,7,0,9,0,0],
    [0,4,0,9,0,3,0,2,0],
    [9,0,3,0,2,0,8,0,1],
    [0,7,0,1,0,8,0,3,0],
    [0,0,7,0,6,0,1,0,0],
    [0,0,0,8,0,4,0,0,0],
    [0,3,5,0,0,0,4,9,0]
]
state = Enum('state', ['error'])

def tableDetailer():
    detailedTable = list()
    
    for r, row in table:
        for c, number in row:
            possibleNumbers = check_singleSquare(r, c)
            possibleNumbers = convertToPossibleNumbers(possibleNumbers)
            print("possible numbers: ", possibleNumbers)
            
            detailedTable.append({
                "number": number,
                "isConstant": number != 0,
                "possibleNumbers": possibleNumbers
            })
            
    print(detailedTable)
       
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
        startingRow = 3
    elif squareNumber > 5:
        startingRow = 6
    
    if squareNumber % 3 == 0:
        startingColumn = 0
    elif squareNumber % 2 != 0:
        startingColumn = 3
    else:
        startingColumn = 6
        
    for row in range(startingRow, startingRow + 3):
        for column in range(startingColumn, startingColumn + 3):
            if table[row][column] != 0:
                forbiddenNumbers.append(table[row][column])
    
    print(forbiddenNumbers)
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
    
    forbiddenNumbers.update(check_3x3Square(squareNumber))
    forbiddenNumbers.update(check_Column(column))
    forbiddenNumbers.update(check_Line(row))    
    
    return forbiddenNumbers

def convertToPossibleNumbers(forbiddenNumbers):
    allNumbers = {1,2,3,4,5,6,7,8,9}
    
    possibleNumbers = allNumbers.difference(forbiddenNumbers)
        
    return possibleNumbers

    
if __name__ == '__main__':
    tableDetailer()
    # check_Line(0)
    # check_Column(0)
    # check_3x3Square(2)
    # check_singleSquare(3,0)