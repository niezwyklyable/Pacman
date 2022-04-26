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
                if obj != -1 and obj != 0:
                    obj.draw(self.win)

        pygame.display.update()

    def update(self):
        pass

    # this method is not optimal but does not have to because it runs only once per game and the both loops are quite short
    def create_board(self): # -1 means impassable wall point, 0 means passable empty point, every different value is an object
        self.board = [[-1 for _ in range(28)] for _ in range(31)] # height: 31 (rows), width: 28 (cols) with border
        for row in range(1, 30): # from 1 to 29
            for col in range(1, 27): # from 1 to 26
                if row == 1:
                    if col != 13 and col != 14:
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 2:
                    if col in (1, 6, 12, 15, 21, 26):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 3:
                    if col in (6, 12, 15, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (1, 26):
                        pass # two big balls have to be here
                elif row == 4:
                    if col in (1, 6, 12, 15, 21, 26):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 5:
                    self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 6:
                    if col in (1, 6, 9, 18, 21, 26):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 7:
                    if col in (1, 6, 9, 18, 21, 26):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 8:
                    if col not in (7, 8, 13, 14, 19, 20):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 9:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (12, 15):
                        self.board[row][col] = 0
                elif row == 10:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (12, 15):
                        self.board[row][col] = 0
                elif row == 11:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in range(9, 19):
                        self.board[row][col] = 0
                elif row == 12:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (9, 18):
                        self.board[row][col] = 0
                elif row == 13:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (9, 11, 12, 13, 14, 15, 16, 18):
                        self.board[row][col] = 0
                elif row == 14:
                    if col not in (10, 17):
                        self.board[row][col] = 0
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (11, 13, 15): # 12, 14 and 16 have to theoretically empty
                        pass # three ghosts have to be here...
                elif row == 15:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (9, 11, 12, 13, 14, 15, 16, 18):
                        self.board[row][col] = 0
                elif row == 16:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (9, 18):
                        self.board[row][col] = 0
                elif row == 17:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in range(9, 19):
                        self.board[row][col] = 0
                elif row == 18:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (9, 18):
                        self.board[row][col] = 0
                elif row == 19:
                    if col in (6, 21):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (9, 18):
                        self.board[row][col] = 0
                elif row == 20:
                    if col != 13 and col != 14:
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 21:
                    if col in (1, 6, 12, 15, 21, 26):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 22:
                    if col in (1, 6, 12, 15, 21, 26):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 23:
                    if col in (2, 3, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 24, 25):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                    elif col in (1, 26):
                        pass # two big balls have to be here
                    elif col == 13:
                        self.board[row][col] = 0
                    elif col == 14:
                        pass # pacman has to be here
                elif row == 24:
                    if col in (3, 6, 9, 18, 21, 24):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 25:
                    if col in (3, 6, 9, 18, 21, 24):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 26:
                    if col not in (7, 8, 13, 14, 19, 20):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 27:
                    if col in (1, 12, 15, 26):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 28:
                    if col in (1, 12, 15, 26):
                        self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)
                elif row == 29:
                    self.board[row][col] = SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12)

        # for testing purposes
        for row in range(len(self.board)):
            temp_list = []
            for col in range(len(self.board[0])):
                if self.board[row][col] not in (-1, 0):
                    temp_list.append(1)
                else:
                    temp_list.append(self.board[row][col])

            #print(temp_list)
