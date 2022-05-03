from .pacman import Pacman
from .constants import BLINKY_RIGHT_1, BLINKY_RIGHT_2, BLINKY_LEFT_1, BLINKY_LEFT_2, \
    BLINKY_UP_1, BLINKY_UP_2, BLINKY_DOWN_1, BLINKY_DOWN_2
import random

class Ghost(Pacman):
    def __init__(self, x, y, STEP):
        super().__init__(x=x, y=y, STEP=STEP)
        self.IMG = None
        self.TYPE = 'GHOST'
    
    # needed to be uncomment later
    # def draw(self, win):
    #     win.blit(self.IMG, (self.x - self.IMG.get_width() // 2, \
    #          self.y - self.IMG.get_height() // 2))

    # a temporarily method, ultimately it will move smartly (AI?) as the original Pacman rules say
    def generate_random_dir(self):
        dir = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        self.set_future_dir(dir)

class Blinky(Ghost):
    def __init__(self, x, y, STEP):
        super().__init__(x=x, y=y, STEP=STEP)
        self.IMG = BLINKY_LEFT_1
        self.STATES_LEFT = [BLINKY_LEFT_1, BLINKY_LEFT_2]
        self.STATES_RIGHT = [BLINKY_RIGHT_1, BLINKY_RIGHT_2]
        self.STATES_UP = [BLINKY_UP_1, BLINKY_UP_2]
        self.STATES_DOWN = [BLINKY_DOWN_1, BLINKY_DOWN_2]
