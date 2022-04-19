import random, sys
import pygame

class slot:
    def __init__(self):
        self.answer = 0
        self.input = 0
        self.showed = 0
        self.pos = (0,0)

class board:
    selected = (-1,-1),(-1,-1)
    sqSelected = (-1,-1)
    hover = (-1,-1),(-1,-1)
    sqHover = (-1,-1)

    def __init__(self, diff, WINSIZE):
        self.grid = [[slot() for i in range(9)] for j in range(9)]
        self.dif = WINSIZE / 9
        # Generate  full grid
        solve(self)
        for i in range(9):
            for j in range(9):
                self.grid[i][j].showed = self.grid[i][j].answer
        # Generate partial grid
        c = 0
        while (c < diff):
            r1 = random.randint(0,8)
            r2 = random.randint(0,8)

            if self.grid[r1][r2].showed != 0:
                self.grid[r1][r2].showed = 0
                c += 1

    def inputValue(self, x, y, value):
        self.grid[y][x].input = value

    def draw(self, WINDOW, WINSIZE, FONT):
        numPos = self.dif/3
        x,y = pygame.mouse.get_pos()
        for i in range(9):
            for j in range(9):
                # Highlight neighbor squares
                if self.selected != ((-1,-1),(-1,-1)):
                    related = ((j*self.dif, i*self.dif),(self.dif+1, self.dif+1))
                    if (j == self.sqSelected[0] and i != self.sqSelected[1]) or (i == self.sqSelected[1] and j != self.sqSelected[0]) or (checkQuad(j, i) == checkQuad(self.sqSelected[0], self.sqSelected[1]) and (j,i) != self.sqSelected): pygame.draw.rect(WINDOW, rgb().grey,(related))
        
        # Highlight empty square being hovered
        if self.grid[self.sqHover[1]][self.sqHover[0]].showed == 0: 
            pygame.draw.rect(WINDOW, rgb().white,(self.hover))
        
        # Highlight selected square
        pygame.draw.rect(WINDOW,(rgb().white),((self.sqSelected[0]*self.dif, self.sqSelected[1]*self.dif),(self.dif+1, self.dif+1)))

        # Form grid          
        for i in range(10):
            if i % 3 == 0 :
                thick = 7
            else:
                thick = 1
            pygame.draw.line(WINDOW, rgb().black, (0, i * self.dif), (WINSIZE, i * self.dif), thick)
            pygame.draw.line(WINDOW, rgb().black, (i * self.dif, 0), (i * self.dif, WINSIZE), thick)

        # Print Board
        for i in range(9):
            for j in range(9):
                if (self.grid[i][j].showed != 0):
                    if self.grid[i][j].showed == self.grid[self.sqSelected[1]][self.sqSelected[0]].input: img = FONT.render(str(self.grid[i][j].showed), True, rgb().highlight)
                    else: img = FONT.render(str(self.grid[i][j].showed), True, rgb().black)
                    WINDOW.blit(img, (j * self.dif + numPos, i * self.dif + numPos * 0.7))
                if self.grid[i][j].input > 0:
                    if self.grid[i][j].input == self.grid[self.sqSelected[1]][self.sqSelected[0]].input and (j,i) != self.sqSelected and self.grid[i][j].input != 0: img = FONT.render(str(self.grid[i][j].input), True, rgb().highlight)
                    else: img = FONT.render(str(self.grid[i][j].input), True, rgb().red)
                    WINDOW.blit(img, (j * self.dif + numPos, i * self.dif + numPos * 0.7))        

    def select(self):
        if (self.grid[self.sqHover[1]][self.sqHover[0]].showed == 0):
            self.selected = self.hover
            self.sqSelected = self.sqHover

class rgb:
    def __init__(self):
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.red = (200,0,0)
        self.highlight = (0,0,255)
        self.background = (200,200,170)
        self.grey = (200,200,200)
        self.blur = (255,255,255,50)

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
            board.grid[row][col].answer = num
            board.grid[row][col].pos = (row,col)

            if solve(board):
                return True
            board.grid[row][col].answer = 0
    return False

def test(board):
    find = findUsed(board)
    if not find:
        return True
    else:
        row, col = find

    poss = [1,2,3,4,5,6,7,8,9]
    random.shuffle(poss)
    for num in poss:
        if not valid(board, num, (row, col)):
            poss.pop(num)

def findUsed(board):
    x = [0,1,2,3,4,5,6,7,8]
    y = [0,1,2,3,4,5,6,7,8]
    random.shuffle(x)
    random.shuffle(y)
    for i in x:
        for j in y:
            if board.grid[i][j].answer > 0:
                return (i,j)
    return None

def findEmpty(board):
    for i in range(len(board.grid)):
        for j in range(len(board.grid[0])):
            if board.grid[i][j].answer == 0:
                return (i,j)
    return None

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo.grid[0])):
        if bo.grid[pos[0]][i].answer == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo.grid)):
        if bo.grid[i][pos[1]].answer == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo.grid[i][j].answer == num and (i,j) != pos:
                return False

    return True

def checkQuad(x, y):
    if (x < 3): i = 0
    elif (x > 2) and (x < 6): i = 3
    else: i = 6

    if (y < 3): j = 0
    elif (y > 2) and (y < 6): j = 3
    else: j = 6

    return (i,j)

def checkWin(board):
    for i in range(9):
        for j in range(9):
            ans = board.grid[i][j].answer
            if ans != board.grid[i][j].input and board.grid[i][j].showed != ans: return False
    return True

def generateBoard():
    board = [[0 for i in range(9)] for j in range(9)]
    solve(board)

    c = 0
    while (c < 30):
        r1 = random.randint(0,8)
        r2 = random.randint(0,8)

        if board[r1][r2] != 0:
            board[r1][r2] = 0
            c += 1

    # for i in range(len(board)): print(board[i])
    # print('Valid board after', c, 'attempts')
    return board