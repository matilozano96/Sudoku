import pygame, random, sys, copy
import button
from sudoFunctions import *
from pygame.locals import *
from abc import ABC

class State(ABC):
    def __init__(self, WINDOW, WINSIZE, FONT):
        self.WINDOW = WINDOW
        self.WINSIZE = WINSIZE
        self.FONT = FONT
    def update(self, stack, events):
        pass
    def render(self):
        pass

class State_Machine():
    states = []
    def __init__(self, WINSIZE):
        self.WINSIZE = WINSIZE
        dif = WINSIZE / 9
        self.numPos = dif / 3
        self.WINDOW = pygame.display.set_mode((WINSIZE, WINSIZE + int(dif)))
        self.FONT = pygame.font.SysFont(None, int(WINSIZE / 10))

        self.states.append(Menu_State(self.WINDOW, WINSIZE, self.FONT))

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        self.states[len(self.states)-1].update(self.states, events)

    def render(self):
        self.WINDOW.fill(rgb().background)
        for state in self.states:
            state.render()
    
    def add(self, s):
        self.states.append(s)

    def remove(self, s):
        self.states.remove(s)

class Menu_State(State):
    difficulty = 2
    active = True
    def __init__(self, WINDOW, WINSIZE, FONT):
        super().__init__(WINDOW, WINSIZE, FONT)
        print("Menu Active")

    def update(self, stack, events):
        keys = pygame.key.get_pressed()
        if keys[K_s]:
            self.active = False

        if not (keys[K_s]) and not self.active:
            stack.remove(self)
            stack.append(Game_State(self.difficulty, self.WINDOW, self.WINSIZE, self.FONT))

    def render(self):
        pass

class Game_State(State):
    active = True
    def __init__(self, difficulty, WINDOW, WINSIZE, FONT):
        super().__init__(WINDOW, WINSIZE, FONT)
        print("Game Active")
        self.b = board(difficulty, self.WINSIZE)
        self.difficulty = difficulty
        for row in self.b.grid:
            for s in row:
                print (s.answer, end=' ')
            print()

    def update(self, stack, events):
        dif = self.WINSIZE / 9
        x,y = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if keys[K_s]:
            self.active = False

        if not (keys[K_s]) and not self.active:
            stack.remove(self)
            stack.append(Menu_State(self.WINDOW, self.WINSIZE, self.FONT))

        for i in range(9):
            for j in range(9):
                if x > (j * dif) and x < ((j+1) * dif) and y > (i * dif) and y < ((i+1) * dif): 
                    self.b.hover = ((j*dif, i*dif),(dif+1, dif+1))
                    self.b.sqHover = (j,i)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.b.select()

        if keys[K_1] or keys[K_KP1]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 1)
        elif keys[K_2] or keys[K_KP2]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 2)
        elif keys[K_3] or keys[K_KP3]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 3)
        elif keys[K_4] or keys[K_KP4]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 4)
        elif keys[K_5] or keys[K_KP5]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 5)
        elif keys[K_6] or keys[K_KP6]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 6)
        elif keys[K_7] or keys[K_KP7]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 7)
        elif keys[K_8] or keys[K_KP8]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 8)
        elif keys[K_9] or keys[K_KP9]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 9)
        elif keys[K_0] or keys[K_KP0]: self.b.inputValue(self.b.sqSelected[0], self.b.sqSelected[1], 0)

        if self.winCheck(): stack.append(Win_State(self.WINDOW, self.WINSIZE, self.FONT, self.difficulty))

    def winCheck(self):
        for i in range(9):
            for j in range(9):
                if self.b.grid[i][j].showed == 0:
                    if self.b.grid[i][j].input != self.b.grid[i][j].answer: return False
        return True

    def render(self):
        self.b.draw(self.WINDOW, self.WINSIZE, self.FONT)

class Win_State(State):
    def __init__(self, WINDOW, WINSIZE, FONT, diff):
        super().__init__(WINDOW, WINSIZE, FONT)
        self.dif = self.WINSIZE / 9
        self.difficulty = diff
        print("Game Won")
    
    def update(self, stack, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                stack.clear()
                stack.append(Game_State(self.difficulty, self.WINDOW, self.WINSIZE, self.FONT))

    def render(self):
        pygame.draw.rect(self.WINDOW,(rgb().black),((self.WINSIZE/3 - self.dif - 2, self.WINSIZE/3 - self.dif - 2),(self.WINSIZE/3 + 2*self.dif + 4, self.WINSIZE/3 + 2*self.dif + 4)))
        pygame.draw.rect(self.WINDOW,(rgb().white),((self.WINSIZE/3 - self.dif, self.WINSIZE/3 - self.dif),(self.WINSIZE/3 + 2*self.dif, self.WINSIZE/3 + 2*self.dif)))