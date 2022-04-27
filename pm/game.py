import pygame
from .constants import BACKGROUND, BLACK, BG_X, BG_Y
from .balls import SmallBall, BigBall
from .pacman import Pacman
from .impassable_point import ImpassablePoint

class Game():
    def __init__(self, win):
        self.win = win
        self.pacman = None
        self.impassable_points = []
        self.small_balls = []
        self.big_balls = []
        self.create_borders()
        self.create_sprites()

    def render(self):
        self.win.fill(BLACK)
        self.win.blit(BACKGROUND, (BG_X, BG_Y))
        for obj in self.small_balls:
            obj.draw(self.win)
        for obj in self.big_balls:
            obj.draw(self.win)
        if self.pacman:
            self.pacman.draw(self.win)
        # for testing purposes
        #for ip in self.impassable_points:
            #ip.draw(self.win)
        pygame.display.update()

    def update(self):
        if self.pacman:
            self.pacman.move()

    def create_borders(self):
        # horizontal lines
        for x in range(3, 221):
            self.impassable_points.append(ImpassablePoint(x, 3))
        for x in list(range(20, 44)) + list(range(60, 92)) + list(range(132, 164)) + \
            list(range(180, 204)):
            self.impassable_points.append(ImpassablePoint(x, 20))
        for x in list(range(20, 44)) + list(range(60, 92)) + list(range(132, 164)) + \
            list(range(180, 204)) + list(range(108, 116)):
            self.impassable_points.append(ImpassablePoint(x, 35))
        for x in list(range(20, 44)) + list(range(60, 68)) + list(range(84, 140)) + \
            list(range(156, 164)) + list(range(180, 204)):
            self.impassable_points.append(ImpassablePoint(x, 52))
        for x in list(range(20, 44)) + list(range(84, 140)) + list(range(180, 204)):
            self.impassable_points.append(ImpassablePoint(x, 59))
        for x in list(range(3, 44)) + list(range(67, 92)) + list(range(132, 157)) + \
            list(range(180, 221)):
            self.impassable_points.append(ImpassablePoint(x, 76))
        for x in list(range(67, 92)) + list(range(108, 116)) + list(range(132, 157)):
            self.impassable_points.append(ImpassablePoint(x, 83))
        for x in list(range(84, 140)):
            self.impassable_points.append(ImpassablePoint(x, 100))
        for x in list(range(87, 137)):
            self.impassable_points.append(ImpassablePoint(x, 103))
        for x in list(range(0, 44)) + list(range(60, 68)) + list(range(156, 164)) + \
            list(range(180, 224)):
            self.impassable_points.append(ImpassablePoint(x, 107))
        for x in list(range(0, 44)) + list(range(60, 68)) + list(range(156, 164)) + \
            list(range(180, 224)):
            self.impassable_points.append(ImpassablePoint(x, 124))
        for x in list(range(87, 137)):
            self.impassable_points.append(ImpassablePoint(x, 128))
        for x in list(range(84, 140)):
            self.impassable_points.append(ImpassablePoint(x, 131))
        for x in list(range(84, 140)):
            self.impassable_points.append(ImpassablePoint(x, 148))
        for x in list(range(3, 44)) + list(range(60, 68)) + list(range(84, 140)) + \
            list(range(156, 164)) + list(range(180, 221)):
            self.impassable_points.append(ImpassablePoint(x, 155))
        for x in list(range(20, 44)) + list(range(60, 92)) + list(range(132, 164)) + \
            list(range(180, 204)):
            self.impassable_points.append(ImpassablePoint(x, 172))
        for x in list(range(20, 44)) + list(range(60, 92)) + list(range(132, 164)) + \
            list(range(180, 204)) + list(range(108, 116)):
            self.impassable_points.append(ImpassablePoint(x, 179))
        for x in list(range(3, 20)) + list(range(60, 68)) + list(range(84, 140)) + \
            list(range(156, 164)) + list(range(204, 221)):
            self.impassable_points.append(ImpassablePoint(x, 196))
        for x in list(range(3, 20)) + list(range(36, 44)) + list(range(84, 140)) + \
            list(range(180, 188)) + list(range(204, 221)):
            self.impassable_points.append(ImpassablePoint(x, 203))
        for x in list(range(20, 92)) + list(range(132, 204)):
            self.impassable_points.append(ImpassablePoint(x, 220))
        for x in list(range(20, 92)) + list(range(132, 204)):
            self.impassable_points.append(ImpassablePoint(x, 227))
        for x in range(3, 221):
            self.impassable_points.append(ImpassablePoint(x, 244))

        # vertical lines
        for y in list(range(3, 77)) + list(range(155, 245)):
            self.impassable_points.append(ImpassablePoint(3, y))
        for y in range(196, 204):
            self.impassable_points.append(ImpassablePoint(19, y))
        for y in list(range(20, 36)) + list(range(52, 60)) + list(range(172, 180)) + \
            list(range(220, 228)):
            self.impassable_points.append(ImpassablePoint(20, y))
        for y in range(179, 204):
            self.impassable_points.append(ImpassablePoint(36, y))
        for y in list(range(20, 36)) + list(range(52, 60)) + list(range(76, 108)) + \
            list(range(124, 156)) + list(range(172, 204)):
            self.impassable_points.append(ImpassablePoint(43, y))
        for y in list(range(20, 36)) + list(range(52, 108)) + list(range(124, 156)) + \
            list(range(172, 180)) + list(range(196, 221)):
            self.impassable_points.append(ImpassablePoint(60, y))
        for y in list(range(52, 108)) + list(range(124, 156)) + list(range(196, 221)):
            self.impassable_points.append(ImpassablePoint(67, y))
        for y in list(range(52, 60)) + list(range(100, 132)) + list(range(148, 156)) + \
            list(range(196, 204)):
            self.impassable_points.append(ImpassablePoint(84, y))
        for y in range(103, 129):
            self.impassable_points.append(ImpassablePoint(87, y))
        for y in list(range(20, 36)) + list(range(76, 84)) + list(range(172, 180)) + \
            list(range(220, 228)):
            self.impassable_points.append(ImpassablePoint(91, y))
        for y in list(range(3, 36)) + list(range(59, 84)) + list(range(155, 180)) + \
            list(range(204, 228)):
            self.impassable_points.append(ImpassablePoint(108, y))
        # mirror reflection
        for y in list(range(3, 77)) + list(range(155, 245)):
            self.impassable_points.append(ImpassablePoint(220, y))
        for y in range(196, 204):
            self.impassable_points.append(ImpassablePoint(204, y))
        for y in list(range(20, 36)) + list(range(52, 60)) + list(range(172, 180)) + \
            list(range(220, 228)):
            self.impassable_points.append(ImpassablePoint(203, y))
        for y in range(179, 204):
            self.impassable_points.append(ImpassablePoint(187, y))
        for y in list(range(20, 36)) + list(range(52, 60)) + list(range(76, 108)) + \
            list(range(124, 156)) + list(range(172, 204)):
            self.impassable_points.append(ImpassablePoint(180, y))
        for y in list(range(20, 36)) + list(range(52, 108)) + list(range(124, 156)) + \
            list(range(172, 180)) + list(range(196, 221)):
            self.impassable_points.append(ImpassablePoint(163, y))
        for y in list(range(52, 108)) + list(range(124, 156)) + list(range(196, 221)):
            self.impassable_points.append(ImpassablePoint(156, y))
        for y in list(range(52, 60)) + list(range(100, 132)) + list(range(148, 156)) + \
            list(range(196, 204)):
            self.impassable_points.append(ImpassablePoint(139, y))
        for y in range(103, 129):
            self.impassable_points.append(ImpassablePoint(136, y))
        for y in list(range(20, 36)) + list(range(76, 84)) + list(range(172, 180)) + \
            list(range(220, 228)):
            self.impassable_points.append(ImpassablePoint(132, y))
        for y in list(range(3, 36)) + list(range(59, 84)) + list(range(155, 180)) + \
            list(range(204, 228)):
            self.impassable_points.append(ImpassablePoint(115, y))

    # this method is not optimal but does not have to because it runs only once per game and the both loops are quite short
    def create_sprites(self):
        # dynamic objects
        self.pacman = Pacman(112, 188)

        # 2D coordinate system - height: 31 (rows), width: 28 (cols) with the external border
        for row in range(1, 30): # from 1 to 29
            for col in range(1, 27): # from 1 to 26
                if row == 1:
                    if col != 13 and col != 14:
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 2:
                    if col in (1, 6, 12, 15, 21, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 3:
                    if col in (6, 12, 15, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif col in (1, 26):
                        self.big_balls.append(BigBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 4:
                    if col in (1, 6, 12, 15, 21, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 5:
                    self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 6:
                    if col in (1, 6, 9, 18, 21, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 7:
                    if col in (1, 6, 9, 18, 21, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 8:
                    if col not in (7, 8, 13, 14, 19, 20):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 9:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 10:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 11:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 12:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 13:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 14:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 15:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 16:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 17:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 18:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 19:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 20:
                    if col != 13 and col != 14:
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 21:
                    if col in (1, 6, 12, 15, 21, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 22:
                    if col in (1, 6, 12, 15, 21, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 23:
                    if col in (2, 3, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 24, 25):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    elif col in (1, 26):
                        self.big_balls.append(BigBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 24:
                    if col in (3, 6, 9, 18, 21, 24):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 25:
                    if col in (3, 6, 9, 18, 21, 24):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 26:
                    if col not in (7, 8, 13, 14, 19, 20):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 27:
                    if col in (1, 12, 15, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 28:
                    if col in (1, 12, 15, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 29:
                    self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
