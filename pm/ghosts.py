from .pacman import Pacman
from .constants import BLINKY_RIGHT_1, BLINKY_RIGHT_2, BLINKY_LEFT_1, BLINKY_LEFT_2, \
    BLINKY_UP_1, BLINKY_UP_2, BLINKY_DOWN_1, BLINKY_DOWN_2, \
    PINKY_DOWN_1, PINKY_DOWN_2, PINKY_LEFT_1, PINKY_LEFT_2, PINKY_UP_1, PINKY_UP_2, PINKY_RIGHT_1, PINKY_RIGHT_2, \
    INKY_DOWN_1, INKY_DOWN_2, INKY_LEFT_1, INKY_LEFT_2, INKY_RIGHT_1, INKY_RIGHT_2, INKY_UP_1, INKY_UP_2, \
    CLYDE_DOWN_1, CLYDE_DOWN_2, CLYDE_LEFT_1, CLYDE_LEFT_2, CLYDE_RIGHT_1, CLYDE_RIGHT_2, CLYDE_UP_1, CLYDE_UP_2
import random

class Ghost(Pacman):
    def __init__(self, x, y, STEP):
        super().__init__(x=x, y=y, STEP=STEP)
        self.IMG = None
        self.TYPE = 'GHOST'
        self.STEP_NORMAL = STEP
        self.STEP_SLOWER = STEP * 0.55
        self.stay_at_home = True # if it is True the ghost cannot escape the home (the centre of the map)
        #self.FORCED_DIRS = ['LEFT', 'DOWN', 'LEFT', 'LEFT', 'UP', 'RIGHT', 'UP', 'LEFT', 'DOWN', \
        # 'DOWN', 'DOWN'] # for testing purposes only
    
    # needed to be uncomment later
    # def draw(self, win):
    #     win.blit(self.IMG, (self.x - self.IMG.get_width() // 2, \
    #          self.y - self.IMG.get_height() // 2))

    # a temporarily method, ultimately it will move smartly (AI?) as the original Pacman rules say
    def generate_random_dir(self):
        dir = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        #dir = self.FORCED_DIRS.pop(0) # for testing purposes only
        self.set_future_dir(dir)

class Blinky(Ghost):
    def __init__(self, x, y, STEP):
        super().__init__(x=x, y=y, STEP=STEP)
        self.IMG = BLINKY_LEFT_1
        self.STATES_LEFT = [BLINKY_LEFT_1, BLINKY_LEFT_2]
        self.STATES_RIGHT = [BLINKY_RIGHT_1, BLINKY_RIGHT_2]
        self.STATES_UP = [BLINKY_UP_1, BLINKY_UP_2]
        self.STATES_DOWN = [BLINKY_DOWN_1, BLINKY_DOWN_2]
        self.stay_at_home = False

class Inky(Ghost):
    def __init__(self, x, y, STEP):
        super().__init__(x=x, y=y, STEP=STEP)
        self.current_dir = 'UP'
        self.future_dir = 'UP'
        self.IMG = INKY_UP_1
        self.STATES_LEFT = [INKY_LEFT_1, INKY_LEFT_2]
        self.STATES_RIGHT = [INKY_RIGHT_1, INKY_RIGHT_2]
        self.STATES_UP = [INKY_UP_1, INKY_UP_2]
        self.STATES_DOWN = [INKY_DOWN_1, INKY_DOWN_2]

class Pinky(Ghost):
    def __init__(self, x, y, STEP):
        super().__init__(x=x, y=y, STEP=STEP)
        self.current_dir = 'DOWN'
        self.future_dir = 'DOWN'
        self.IMG = PINKY_DOWN_1
        self.STATES_LEFT = [PINKY_LEFT_1, PINKY_LEFT_2]
        self.STATES_RIGHT = [PINKY_RIGHT_1, PINKY_RIGHT_2]
        self.STATES_UP = [PINKY_UP_1, PINKY_UP_2]
        self.STATES_DOWN = [PINKY_DOWN_1, PINKY_DOWN_2]

class Clyde(Ghost):
    def __init__(self, x, y, STEP):
        super().__init__(x=x, y=y, STEP=STEP)
        self.current_dir = 'UP'
        self.future_dir = 'UP'
        self.IMG = CLYDE_UP_1
        self.STATES_LEFT = [CLYDE_LEFT_1, CLYDE_LEFT_2]
        self.STATES_RIGHT = [CLYDE_RIGHT_1, CLYDE_RIGHT_2]
        self.STATES_UP = [CLYDE_UP_1, CLYDE_UP_2]
        self.STATES_DOWN = [CLYDE_DOWN_1, CLYDE_DOWN_2]
