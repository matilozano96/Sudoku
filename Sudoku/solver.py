import random, sys

def solve(board):
    find = findEmpty(board)
    if not find:
        return True
    else:
        row, col = find

    poss = [1,2,3,4,5,6,7,8,9]
    random.shuffle(poss)

    for num in poss:
        if valid(board, num, (row, col)):
            board[row][col] = num

            if solve(board):
                return True
            board[row][col] = 0
    return False

def inColumn(board, value, x, y):

    # print('Checking Column for', x,',',y)
    column = []
    for i in range(9):
        column.append(board[i][y])
    if value not in column: return False
    else: return True

def inQuadrant(board, value, x, y):
    
    quad = []
    # print('Checking Quad for', x,',',y)

    if (x < 3):
        x = 0
    elif (x > 2) and (x < 6):
        x = 3
    else: x = 6

    if (y < 3):
        y = 0
    elif (y > 2) and (y < 6):
        y = 3
    else: y = 6

    for i in range(3):
        for j in range(3):
            quad.append(board[i + x][j + y])

    if value not in quad: return False
    else: return True

def findEmpty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i,j)
    return None

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

def shuffle(b):
    for i in range(3):
        for j in range(3):
            num1 = random.randint(0,2)
            num2 = random.randint(0,2)
            b[i*3 + num1], b[i*3 + num2] = b[i*3 + num2], b[i*3 + num1] 
            for x in range(9): b[x][i*3 + num1], b[x][i*3 + num2] = b[x][i*3 + num2], b[x][i*3 + num1]