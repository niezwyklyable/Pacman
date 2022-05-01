import pygame
from .constants import BACKGROUND, BLACK, BG_X, BG_Y, FACTOR
from .balls import SmallBall, BigBall
from .pacman import Pacman
from .intersection import Intersection
from math import sqrt

class Game():
    def __init__(self, win):
        self.win = win
        self.pacman = None
        self.intersections = []
        self.small_balls = []
        self.big_balls = []
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
        for i in self.intersections:
            i.draw(self.win)
        pygame.display.update()

    def update(self):
        if self.pacman:
            for i in self.intersections:
                if self.collision_detection(self.pacman, i):
                    break # if there is a collision just pass the rest of a loop and the part of code below (optimization issue)
            else: 
                # available moves between two intersections (when there is no collision)
                if self.pacman.current_dir == 'LEFT' and self.pacman.future_dir == 'RIGHT':
                    self.pacman.change_dir()
                elif self.pacman.current_dir == 'RIGHT' and self.pacman.future_dir == 'LEFT':
                    self.pacman.change_dir()
                elif self.pacman.current_dir == 'UP' and self.pacman.future_dir == 'DOWN':
                    self.pacman.change_dir()
                elif self.pacman.current_dir == 'DOWN' and self.pacman.future_dir == 'UP':
                    self.pacman.change_dir()

            self.pacman.move() # move according to the current_dir
            self.pacman.change_image() # an animation

    def collision_detection(self, obj1, obj2): # obj1 is a dynamic object, obj2 is considered as a static object even though it is a dynamic object
        if obj1.TYPE == 'PACMAN' and obj2.TYPE == 'INTERSECTION':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < FACTOR * obj1.STEP: # the radius of a collision - it should be lesser than STEP * FACTOR but not lesser than a half of STEP * FACTOR of a dynamic object to work properly
                obj1.x = obj2.x # alignment to the center of obj2
                obj1.y = obj2.y # alignment to the center of obj2
                if obj1.future_dir in obj2.dirs:
                    # if there is a possibility to change dir then do it firstly
                    obj1.change_dir() # assign future_dir to current_dir
                elif obj1.current_dir in obj2.dirs:
                    pass # if there is a possibility to keep going then do not change anything
                else:
                    obj1.stop() # assign None value to current_dir if there is no possibility to move forward or wherever you wish
                return True
                
        return False

    # this method is not optimal but does not have to because it runs only once per game and the both loops are quite short
    def create_sprites(self):
        # dynamic objects
        self.pacman = Pacman(112, 188)

        # 2D coordinate system - height: 31 (rows), width: 28 (cols) with the external border
        for row in range(1, 30): # from 1 to 29
            for col in range(28): # from 0 to 27
                if row == 1:
                    if col not in (0, 13, 14, 27):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    if col == 1: 
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'RIGHT', 'DOWN'))
                    elif col == 6:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'RIGHT', 'DOWN'))
                    elif col == 12:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'DOWN'))
                    elif col == 15:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'RIGHT', 'DOWN'))
                    elif col == 21:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'RIGHT', 'DOWN'))
                    elif col == 26:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'DOWN'))
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
                    if col not in (0, 27):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    if col == 1: 
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT', 'DOWN'))
                    elif col == 6:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT', 'DOWN'))
                    elif col == 9:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'RIGHT', 'DOWN'))
                    elif col == 12:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'UP', 'RIGHT'))
                    elif col == 15:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'UP', 'RIGHT'))
                    elif col == 18:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'RIGHT', 'DOWN'))
                    elif col == 21:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT', 'DOWN'))
                    elif col == 26:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'DOWN'))
                elif row == 6:
                    if col in (1, 6, 9, 18, 21, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 7:
                    if col in (1, 6, 9, 18, 21, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 8:
                    if col not in (0, 7, 8, 13, 14, 19, 20, 27):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    if col == 1: 
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT'))
                    elif col == 6:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'DOWN'))
                    elif col == 9:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT'))
                    elif col == 12:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'DOWN'))
                    elif col == 15:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'RIGHT', 'DOWN'))
                    elif col == 18:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT'))
                    elif col == 21:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT', 'DOWN'))
                    elif col == 26:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT'))
                elif row == 9:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 10:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 11:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    if col == 9:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'RIGHT'))
                    elif col == 12:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT'))
                    elif col == 15:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT'))
                    elif col == 18:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'LEFT'))
                elif row == 12:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 13:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 14:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    if col == 0: 
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'RIGHT')) # the passage in the future
                    elif col == 6:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT', 'DOWN'))
                    elif col == 9:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'DOWN'))
                    elif col == 18:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT', 'DOWN'))
                    elif col == 21:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT', 'DOWN'))
                    elif col == 27:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT')) # the passage in the future
                elif row == 15:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 16:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 17:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    if col == 9:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT', 'DOWN'))
                    elif col == 18:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'DOWN'))
                elif row == 18:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 19:
                    if col in (6, 21):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 20:
                    if col not in (0, 13, 14, 27):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    if col == 1: 
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'RIGHT'))
                    elif col == 6:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT', 'DOWN'))
                    elif col == 9:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT'))
                    elif col == 12:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'DOWN'))
                    elif col == 15:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'RIGHT', 'DOWN'))
                    elif col == 18:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT'))
                    elif col == 21:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT', 'LEFT', 'DOWN'))
                    elif col == 26:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'LEFT'))
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
                    if col == 1: 
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT'))
                    elif col == 3:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'DOWN'))
                    elif col == 6:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT', 'DOWN'))
                    elif col == 9:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'LEFT', 'RIGHT'))
                    elif col == 12:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'UP', 'RIGHT'))
                    elif col == 15:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'UP', 'RIGHT'))
                    elif col == 18:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'LEFT', 'RIGHT'))
                    elif col == 21:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'DOWN'))
                    elif col == 24:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'RIGHT'))
                    elif col == 26:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT'))
                elif row == 24:
                    if col in (3, 6, 9, 18, 21, 24):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 25:
                    if col in (3, 6, 9, 18, 21, 24):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 26:
                    if col not in (0, 7, 8, 13, 14, 19, 20, 27):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    if col == 1: 
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'RIGHT'))
                    elif col == 3:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT'))
                    elif col == 6:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT'))
                    elif col == 9:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT'))
                    elif col == 12:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'LEFT', 'DOWN'))
                    elif col == 15:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'RIGHT'))
                    elif col == 18:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT'))
                    elif col == 21:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT'))
                    elif col == 24:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT'))
                    elif col == 26:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'DOWN', 'LEFT'))
                elif row == 27:
                    if col in (1, 12, 15, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 28:
                    if col in (1, 12, 15, 26):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                elif row == 29:
                    if col not in (0, 27):
                        self.small_balls.append(SmallBall((col - 1) * 8 + 12, (row - 1) * 8 + 12))
                    if col == 1: 
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT'))
                    elif col == 12:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT'))
                    elif col == 15:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT'))
                    elif col == 26:
                        self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT'))

        #for i in self.intersections:
            #print(i.dirs)
