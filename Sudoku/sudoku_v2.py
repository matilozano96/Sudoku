import pygame, random, sys, copy
import button
from sudoFunctions import *
from pygame.locals import *
pygame.init()

WINSIZE = 800
FPS = 60
fpsClock = pygame.time.Clock()
dif = WINSIZE / 9
numPos = dif / 3
 
WINDOW = pygame.display.set_mode((WINSIZE, WINSIZE + int(dif)))
pygame.display.set_caption('Sudoku')

FONT = pygame.font.SysFont(None, int(WINSIZE / 10))

def main():
    looping = True
    menu = True
    game = False
    difficulty = 20
    while looping:
        WINDOW.fill(rgb().background)
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if menu:
            keys = pygame.key.get_pressed()
            if keys[K_s]:
                b = board(difficulty, WINSIZE)
                for row in b.grid:
                    for s in row:
                        print (s.answer, end=' ')
                    print()
                menu = False
                game = True
            
        if game:
            for i in range(9):
                for j in range(9):
                    if x > (j * dif) and x < ((j+1) * dif) and y > (i * dif) and y < ((i+1) * dif): 
                        b.hover = ((j*dif, i*dif),(dif+1, dif+1))
                        b.sqHover = (j,i)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                b.selected = b.hover
                b.sqSelected = b.sqHover
            b.draw()
            # Read keys
            keys = pygame.key.get_pressed()
            if keys[K_1] or keys[K_KP1]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 1)
            elif keys[K_2] or keys[K_KP2]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 2)
            elif keys[K_3] or keys[K_KP3]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 3)
            elif keys[K_4] or keys[K_KP4]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 4)
            elif keys[K_5] or keys[K_KP5]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 5)
            elif keys[K_6] or keys[K_KP6]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 6)
            elif keys[K_7] or keys[K_KP7]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 7)
            elif keys[K_8] or keys[K_KP8]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 8)
            elif keys[K_9] or keys[K_KP9]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 9)
            elif keys[K_0] or keys[K_KP0]: b.inputValue(b.sqSelected[0], b.sqSelected[1], 0)
            if keys[K_a]:
                game = False
                menu = True

            if checkWin(b) == True:
                print('Win')
                img = FONT.render('You win!', True, rgb().black)
                WINDOW.blit(img, (numPos, 9 * dif + numPos * 0.7))
                img = FONT.render('Press S', True, rgb().black)
                WINDOW.blit(img, (WINSIZE/2 + numPos, 9 * dif + numPos * 0.7))
        pygame.display.update()
        fpsClock.tick(FPS) 
if __name__ == "__main__":
    main()