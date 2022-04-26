import pygame
from .constants import BACKGROUND, BLACK, BG_X, BG_Y
from .ball import SmallBall

class Game():
    def __init__(self, win):
        self.win = win
        self.create_board()

    def render(self):
        self.win.fill(BLACK)
        self.win.blit(BACKGROUND, (BG_X, BG_Y))
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                obj = self.board[row][col]
                if obj != -1:
                    obj.draw(self.win)

        pygame.display.update()

    def update(self):
        pass

    def create_board(self):
        self.board = [[-1 for _ in range(26)] for _ in range(29)] # height: 29 (rows), width: 26 (cols)
        self.board[0][0] = SmallBall(12, 12)
