import pygame
from .constants import BACKGROUND, BLACK, BG_X, BG_Y, FACTOR, WHITE, PACMAN_LIFE, RED
from .balls import SmallBall, BigBall
from .pacman import Pacman
from .intersection import Intersection
from .ghosts import Blinky, Inky, Pinky, Clyde
from math import sqrt

class Game():
    def __init__(self, win):
        self.win = win
        self.high_score = 0
        self.restart()

    def restart(self, next_level=False):
        self.pacman = None
        self.intersections = []
        self.small_balls = []
        self.big_balls = []
        self.ghosts = []
        if not next_level:
            self.gameover = False
            self.level = 1
            self.score = 0
            self.lives = 3
        self.create_sprites(self.level)

    def render(self):
        # the background
        self.win.fill(BLACK)
        self.win.blit(BACKGROUND, (BG_X, BG_Y))
        
        # small balls
        for obj in self.small_balls:
            obj.draw(self.win)

        # big balls
        for obj in self.big_balls:
            if obj.IMG:
                obj.draw(self.win)

        # the Pacman
        if self.pacman:
            self.pacman.draw(self.win)

        # ghosts
        for obj in self.ghosts:
            obj.draw(self.win)

        # points of intersections (for testing purposes)
        for i in self.intersections:
            i.draw(self.win)

        # an upper bar
        font = pygame.font.SysFont('comicsans', 20)
        caption = font.render(f'LVL: {self.level}\
                    SCORE: {self.score}\
                    HIGH SCORE: {self.high_score}', 1, WHITE)
        self.win.blit(caption, (int(BG_X + 10), int(BG_Y - caption.get_height() / 2 - 13)))

        # a bottom bar
        font = pygame.font.SysFont('comicsans', 15)
        caption = font.render('LIVES: ', 1, WHITE)
        self.win.blit(caption, (int(BG_X + 10), int(BG_Y + BACKGROUND.get_height() + caption.get_height() / 2 - 11)))
        DX = PACMAN_LIFE.get_width() + 5
        x = caption.get_width() + 15
        temp = self.lives - 1
        while temp > 0:
            self.win.blit(PACMAN_LIFE, (int(BG_X + x), int(BG_Y + BACKGROUND.get_height() + PACMAN_LIFE.get_height() / 2)))
            x += DX
            temp -= 1

        # a game over caption
        if self.gameover:
            font = pygame.font.SysFont('comicsans', 35)
            caption = font.render('GAME OVER', 1, RED)
            self.win.blit(caption, (int(BG_X + BACKGROUND.get_width() / 2 - caption.get_width() / 2), int(BG_Y + 140 * FACTOR - caption.get_height() / 2)))

        pygame.display.update()

    def update(self):
        # high score update
        if self.score > self.high_score:
            self.high_score = self.score

        # next level condition
        if not self.small_balls and not self.big_balls:
            self.level += 1
            self.restart(next_level=True)

        if self.pacman:
            # the decaying animation of the pacman
            if self.pacman.decaying:
                if self.pacman.decay():
                    pass # do nothing - let static objects animate until it finishes
                else:
                    self.lives -= 1
                    self.pacman = None
                    # game over condition
                    if self.lives <= 0:
                        self.gameover = True
                    else:
                        self.create_sprites(self.level, reset_static_objects=False) # reset only dynamic objects (the Pacman and ghosts)
            else:
                # collision between the pacman and intersections
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

                # collision between the pacman and small balls
                for sb in self.small_balls:
                    if self.collision_detection(self.pacman, sb):
                        self.small_balls.remove(sb)
                        self.score += 10

                # collision between the pacman and big balls
                for bb in self.big_balls:
                    if self.collision_detection(self.pacman, bb):
                        self.big_balls.remove(bb)
                        self.score += 50

                # collision between the pacman and ghosts
                for g in self.ghosts:
                    if self.collision_detection(self.pacman, g):
                        self.ghosts = []
                        self.pacman.decaying = True
                        self.pacman.stop()
                        break

                # the tunnel for the Pacman
                if self.pacman.x + self.pacman.IMG.get_width() // 2 < BG_X:
                    self.pacman.x = BG_X + BACKGROUND.get_width() + self.pacman.IMG.get_width() // 2
                elif self.pacman.x - self.pacman.IMG.get_width() // 2 > BG_X + BACKGROUND.get_width():
                    self.pacman.x = BG_X - self.pacman.IMG.get_width() // 2

        # an animation of a static object - a big ball
        for bb in self.big_balls:
            bb.change_image()

        for g in self.ghosts:
            # the tunnel for the ghosts (it has to be before collision detection with intersections due to STEP changing)
            if g.x + g.IMG.get_width() // 2 < BG_X:
                g.x = BG_X + BACKGROUND.get_width() + g.IMG.get_width() // 2
            elif g.x - g.IMG.get_width() // 2 > BG_X + BACKGROUND.get_width():
                g.x = BG_X - g.IMG.get_width() // 2
            if g.y == BG_Y + 116 * FACTOR and (g.x < BG_X + 52 * FACTOR or g.x > BG_X + 172 * FACTOR):
                g.STEP = g.STEP_SLOWER
            else:
                g.STEP = g.STEP_NORMAL

            g.move() # move according to the current_dir (it has to be before collision detection with intersections due to STEP changing)
            g.change_image() # an animation

            # collision between ghosts and intersections
            for i in self.intersections:
                if self.collision_detection(g, i):
                    break

            # stay at home collision condition
            if g.stay_at_home:
                if g.y - g.IMG.get_height() // 2 < BG_Y + 103 * FACTOR:
                    g.y = BG_Y + 103 * FACTOR + g.IMG.get_height() // 2
                    g.set_future_dir('DOWN')
                    g.change_dir()
                elif g.y + g.IMG.get_height() // 2 > BG_Y + 128 * FACTOR:
                    g.y = BG_Y + 128 * FACTOR - g.IMG.get_height() // 2
                    g.set_future_dir('UP')
                    g.change_dir()

    def collision_detection(self, obj1, obj2): # obj1 is a dynamic object, obj2 is considered as a static object even though it is a dynamic object
        if (obj1.TYPE == 'PACMAN' or obj1.TYPE == 'GHOST') and obj2.TYPE == 'INTERSECTION':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < FACTOR * obj1.STEP: # the radius of a collision - it should be lesser than STEP * FACTOR but not lesser than a half of STEP * FACTOR of a dynamic object to work properly
                obj1.x = obj2.x # alignment to the center of obj2
                obj1.y = obj2.y # alignment to the center of obj2
                if obj1.TYPE == 'GHOST':
                    obj1.generate_random_dir()
                if obj1.future_dir in obj2.dirs:
                    # if there is a possibility to change dir then do it firstly
                    obj1.change_dir() # assign future_dir to current_dir
                elif obj1.current_dir in obj2.dirs:
                    pass # if there is a possibility to keep going then do not change anything
                else:
                    obj1.stop() # assign None value to current_dir if there is no possibility to move forward or wherever you wish
                return True
                
        elif obj1.TYPE == 'PACMAN' and obj2.TYPE == 'SMALL_BALL':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < obj1.IMG.get_width() // 2 + obj2.IMG.get_width() // 2:
                return True

        elif obj1.TYPE == 'PACMAN' and obj2.TYPE == 'BIG_BALL':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < obj1.IMG.get_width() // 2 + obj2.IMG_WIDTH // 2:
                return True

        elif obj1.TYPE == 'PACMAN' and obj2.TYPE == 'GHOST':
            if sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2) < obj1.IMG.get_width() // 2 + obj2.IMG.get_width() // 2:
                return True

        return False

    def create_sprites(self, lvl, reset_static_objects=True):
        # dynamic objects
        if lvl == 1:
            step = 1
        elif lvl == 2:
            step = 2
        else:
            step = 3

        ghost_step = 2/3 * step
        self.pacman = Pacman(112, 188, step)
        self.ghosts.append(Blinky(112, 92, ghost_step))
        self.ghosts.append(Inky(96, 116, ghost_step))
        self.ghosts.append(Pinky(112, 116, ghost_step))
        self.ghosts.append(Clyde(128, 116, ghost_step))

        # static objects
        if reset_static_objects:
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
                        if col == 6:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT', 'DOWN'))
                        elif col == 9:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'DOWN'))
                        elif col == 18:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'RIGHT', 'DOWN'))
                        elif col == 21:
                            self.intersections.append(Intersection((col - 1) * 8 + 12, (row - 1) * 8 + 12, 'UP', 'LEFT', 'RIGHT', 'DOWN'))
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
