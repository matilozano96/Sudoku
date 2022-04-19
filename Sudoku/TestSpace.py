import pygame, random, sys, copy
import button
from sudoFunctions import *
from pygame.locals import *
pygame.init()

scrSize = 800
FPS = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((scrSize, scrSize))
pygame.display.set_caption('Sudoku')

def main():
    buttons = []
    buttons.append(button.button(position=(200, 200), size=(100,100), clr=[100, 100, 100], cngclr=[200, 200, 200], func = goMenu, text='Menu', font="Segoe Print", font_size=16, font_clr=[0, 0, 0]))
    buttons.append(button.button(position=(500, 200), size=(100,100), clr=[100, 100, 100], cngclr=[200, 200, 200], func = notMenu, text='Not Menu', font="Segoe Print", font_size=16, font_clr=[0, 0, 0]))
    print(buttons)
    loop = True
    while loop:
        pos = pygame.mouse.get_pos()
        screen.fill([255, 255, 255])
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        for b in buttons: b.draw(screen)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                if b.rect.collidepoint(pos):
                    b.call_back()



        pygame.display.update()
        fpsClock.tick(FPS)  

def goMenu():
    print("Menu")

def notMenu():
    print("Not Menu")

if __name__ == "__main__":
    main()