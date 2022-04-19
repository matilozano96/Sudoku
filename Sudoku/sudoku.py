import pygame, random, sys, copy
from solver import solve
from pygame.locals import *
pygame.init()
 
GREY = (200,210,200)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
WINSIZE = 800
BACKGROUND = (200,200,170)

difficulty = 30

FPS = 60
fpsClock = pygame.time.Clock()
dif = WINSIZE / 9
numPos = dif / 3
 
WINDOW = pygame.display.set_mode((WINSIZE, WINSIZE + int(dif)))
pygame.display.set_caption('Sudoku')

font = pygame.font.SysFont(None, int(WINSIZE / 10))
    
def main():
    looping = True
    board = generateBoard()
    answers = copy.deepcopy(board)

    for i in range(9):
        for j in range(9):
            if answers[i][j] != 0:
                answers[i][j] = -1

    selected = (-1,-1),(-1,-1)
    sqSelected = (-1,-1)
    sqHover = None

    while looping:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        WINDOW.fill(BACKGROUND)
        x,y = pygame.mouse.get_pos()

        # Highlight empty square being hovered
        hover = (0,0),(0,0)
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0 and x > (i * dif) and x < ((i+1) * dif) and y > (j * dif) and y < ((j+1) * dif): 
                    hover = ((i*dif, j*dif),(dif+1, dif+1))
                    sqHover = (i,j)

        # Highlight selected square
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected = hover
            sqSelected = sqHover
        pygame.draw.rect(WINDOW,(WHITE),((sqSelected[0]*dif, sqSelected[1]*dif),(dif+1, dif+1)))

        if selected != ((-1,-1),(-1,-1)):
            for i in range(9):
                for j in range(9):
                    related = ((i*dif, j*dif),(dif+1, dif+1))
                    if i == sqSelected[0] and j != sqSelected[1]: pygame.draw.rect(WINDOW,GREY,(related))
                    elif j == sqSelected[1] and i != sqSelected[0]: pygame.draw.rect(WINDOW,GREY,(related))
                    elif checkQuad(board, i, j) == checkQuad(board, sqSelected[0], sqSelected[1]) and (i,j) != sqSelected: pygame.draw.rect(WINDOW,GREY,(related))

        pygame.draw.rect(WINDOW,WHITE,(hover))

        # Temp: Selected Coords
        coords = str('X: ' + str(sqSelected[0] + 1))
        img = font.render(coords, True, BLACK)
        WINDOW.blit(img, (numPos, 9 * dif + numPos * 0.7))
        coords = str('Y: ' + str(sqSelected[1] + 1))
        img = font.render(coords, True, BLACK)
        WINDOW.blit(img, (WINSIZE/2 + numPos, 9 * dif + numPos * 0.7))
        
        # Read keys
        keys = pygame.key.get_pressed()
        if keys[K_1] or keys[K_KP1]:
            answers[sqSelected[0]][sqSelected[1]] = 1
        elif keys[K_2] or keys[K_KP2]:
            answers[sqSelected[0]][sqSelected[1]] = 2
        elif keys[K_3] or keys[K_KP3]:
            answers[sqSelected[0]][sqSelected[1]] = 3
        elif keys[K_4] or keys[K_KP4]:
            answers[sqSelected[0]][sqSelected[1]] = 4
        elif keys[K_5] or keys[K_KP5]:
            answers[sqSelected[0]][sqSelected[1]] = 5
        elif keys[K_6] or keys[K_KP6]:
            answers[sqSelected[0]][sqSelected[1]] = 6
        elif keys[K_7] or keys[K_KP7]:
            answers[sqSelected[0]][sqSelected[1]] = 7
        elif keys[K_8] or keys[K_KP8]:
            answers[sqSelected[0]][sqSelected[1]] = 8
        elif keys[K_9] or keys[K_KP9]:
            answers[sqSelected[0]][sqSelected[1]] = 9
        elif keys[K_0] or keys[K_KP0]:
            answers[sqSelected[0]][sqSelected[1]] = 0
        elif keys[K_c]:
            for i in range(9):
                for j in range(9):
                    if answers[i][j] > 0: answers[i][j] = 0
        for i in keys:
            if i == True: print(keys[i])
        
        # Form grid          
        for i in range(10):
            if i % 3 == 0 :
                thick = 7
            else:
                thick = 1
            pygame.draw.line(WINDOW, BLACK, (0, i * dif), (WINSIZE, i * dif), thick)
            pygame.draw.line(WINDOW, BLACK, (i * dif, 0), (i * dif, WINSIZE), thick)

        # Print Board
        for i in range(9):
            for j in range(9):
                if (board[i][j] != 0): 
                    if board[i][j] == answers[sqSelected[0]][sqSelected[1]]: img = font.render(str(board[i][j]), True, (255,255,255))
                    else: img = font.render(str(board[i][j]), True, BLACK)
                    WINDOW.blit(img, (i * dif + numPos, j * dif + numPos * 0.7))


        # Answers Board
        for i in range(9):
            for j in range(9):
                if answers[i][j] > 0:
                    img = font.render(str(answers[i][j]), True, RED)
                    WINDOW.blit(img, (i * dif + numPos, j * dif + numPos * 0.7))
        
        pygame.display.update()
        fpsClock.tick(FPS)  

def generateBoard():
    board = [[0 for i in range(9)] for j in range(9)]
    solve(board)

    c = 0
    while (c < difficulty):
        r1 = random.randint(0,8)
        r2 = random.randint(0,8)

        if board[r1][r2] != 0:
            board[r1][r2] = 0
            c += 1

    # for i in range(len(board)): print(board[i])
    # print('Valid board after', c, 'attempts')
    return board

def checkQuad(board, x, y):
    if (x < 3): i = 0
    elif (x > 2) and (x < 6): i = 3
    else: i = 6

    if (y < 3): j = 0
    elif (y > 2) and (y < 6): j = 3
    else: j = 6

    return (i,j)

if __name__ == "__main__":
    main()