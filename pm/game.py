import pygame
from .constants import BLACK

class Game():
    def __init__(self, win):
        self.win = win

    def render(self):
        self.win.fill(BLACK)
        pygame.display.update()

    def update(self):
        pass