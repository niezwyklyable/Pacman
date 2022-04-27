from .sprite import Sprite
from .constants import PACMAN_LEFT_1, PACMAN_LEFT_2, PACMAN_RIGHT_1, PACMAN_RIGHT_2,\
     PACMAN_UP_1, PACMAN_UP_2, PACMAN_DOWN_1, PACMAN_DOWN_2, PACMAN_FULL

class Pacman(Sprite):
    STEP = 3

    def __init__(self, x, y):
        super().__init__(IMG=PACMAN_FULL, TYPE='PACMAN', x=x, y=y)
        self.dir = 'LEFT'
        #self.img_state = 0

    def change_dir(self, dir):
        if dir == 'LEFT':
            self.dir = 'LEFT'
        elif dir == 'RIGHT':
            self.dir = 'RIGHT'
        elif dir == 'UP':
            self.dir = 'UP'
        elif dir == 'DOWN':
            self.dir = 'DOWN'

    def stop(self):
        self.dir = None

    def move(self):
        if self.dir == 'LEFT':
            self.x -= self.STEP
        elif self.dir == 'RIGHT':
            self.x += self.STEP
        elif self.dir == 'UP':
            self.y -= self.STEP
        elif self.dir == 'DOWN':
            self.y += self.STEP

    def change_image(self):
        if self.dir == 'LEFT':
            pass
