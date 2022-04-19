import pygame, random, sys, copy
import button
from state_machine import *
from sudoFunctions import *
from pygame.locals import *
from sudoku_v2 import rgb
pygame.init()


WINSIZE = 800
FPS = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption('Sudoku')

def main():
    looping = True
    sm = State_Machine(WINSIZE)
    while looping:
        sm.update()
        sm.render()

        pygame.display.update()
        fpsClock.tick(FPS)  

if __name__ == "__main__":
    main()