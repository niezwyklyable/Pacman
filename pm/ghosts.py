from .pacman import Pacman
from .constants import BLINKY_RIGHT_1, BLINKY_RIGHT_2, BLINKY_LEFT_1, BLINKY_LEFT_2, \
    BLINKY_UP_1, BLINKY_UP_2, BLINKY_DOWN_1, BLINKY_DOWN_2, \
    PINKY_DOWN_1, PINKY_DOWN_2, PINKY_LEFT_1, PINKY_LEFT_2, PINKY_UP_1, PINKY_UP_2, PINKY_RIGHT_1, PINKY_RIGHT_2, \
    INKY_DOWN_1, INKY_DOWN_2, INKY_LEFT_1, INKY_LEFT_2, INKY_RIGHT_1, INKY_RIGHT_2, INKY_UP_1, INKY_UP_2, \
    CLYDE_DOWN_1, CLYDE_DOWN_2, CLYDE_LEFT_1, CLYDE_LEFT_2, CLYDE_RIGHT_1, CLYDE_RIGHT_2, CLYDE_UP_1, CLYDE_UP_2
import random

class Ghost(Pacman):
    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD):
        super().__init__(x=x, y=y, STEP=STEP)
        self.IMG = None
        self.TYPE = 'GHOST'
        self.STEP_NORMAL = STEP
        self.STEP_SLOWER = STEP * 0.55
        self.stay_at_home = True # if it is True the ghost cannot escape the home (the centre of the map)
        self.GO_OUT_THRESHOLD = GO_OUT_THRESHOLD # number of frames to go out (escape the home)
        #self.FORCED_DIRS = ['LEFT', 'DOWN', 'LEFT', 'LEFT', 'UP', 'RIGHT', 'UP', 'LEFT', 'DOWN', \
        # 'DOWN', 'DOWN'] # for testing purposes only
        self.state = 'NORMAL'
        self.STATES_DOWN = []
        self.STATES_DOWN_NORMAL = []
        self.STATES_UP = []
        self.STATES_UP_NORMAL = []
        self.STATES_LEFT = []
        self.STATES_LEFT_NORMAL = []
        self.STATES_RIGHT = []
        self.STATES_RIGHT_NORMAL = []
        self.FULL_BLUE = [] # fill up in the future with 2 constants
        self.HALF_BLUE = [] # fill up in the future with 4 constants
        self.EYES_LEFT = [] # fill up in the future with 1 constant
        self.EYES_RIGHT = [] # fill up in the future with 1 constant
        self.EYES_UP = [] # fill up in the future with 1 constant
        self.EYES_DOWN = [] # fill up in the future with 1 constant

    def change_state(self, state):
        if state == 'NORMAL':
            self.state = 'NORMAL'
            self.STATES_LEFT = self.STATES_LEFT_NORMAL
            self.STATES_RIGHT = self.STATES_RIGHT_NORMAL
            self.STATES_UP = self.STATES_UP_NORMAL
            self.STATES_DOWN = self.STATES_DOWN_NORMAL
        elif state == 'FULL_BLUE':
            self.state = 'FULL_BLUE'
            self.STATES_LEFT = self.FULL_BLUE
            self.STATES_RIGHT = self.FULL_BLUE
            self.STATES_UP = self.FULL_BLUE
            self.STATES_DOWN = self.FULL_BLUE
        elif state == 'HALF_BLUE':
            self.state = 'HALF_BLUE'
            self.STATES_LEFT = self.HALF_BLUE
            self.STATES_RIGHT = self.HALF_BLUE
            self.STATES_UP = self.HALF_BLUE
            self.STATES_DOWN = self.HALF_BLUE
        elif state == 'EYES':
            self.state = 'EYES'
            self.STATES_LEFT = self.EYES_LEFT
            self.STATES_RIGHT = self.EYES_RIGHT
            self.STATES_UP = self.EYES_UP
            self.STATES_DOWN = self.EYES_DOWN
    
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
    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD=0):
        super().__init__(x=x, y=y, STEP=STEP, GO_OUT_THRESHOLD=GO_OUT_THRESHOLD)
        self.IMG = BLINKY_LEFT_1
        self.STATES_LEFT_NORMAL = [BLINKY_LEFT_1, BLINKY_LEFT_2]
        self.STATES_RIGHT_NORMAL = [BLINKY_RIGHT_1, BLINKY_RIGHT_2]
        self.STATES_UP_NORMAL = [BLINKY_UP_1, BLINKY_UP_2]
        self.STATES_DOWN_NORMAL = [BLINKY_DOWN_1, BLINKY_DOWN_2]
        self.stay_at_home = False
        self.change_state('NORMAL')
        #self.SUBTYPE = 'BLINKY'

class Inky(Ghost):
    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD):
        super().__init__(x=x, y=y, STEP=STEP, GO_OUT_THRESHOLD=GO_OUT_THRESHOLD)
        self.current_dir = 'UP'
        self.future_dir = 'UP'
        self.IMG = INKY_UP_1
        self.STATES_LEFT_NORMAL = [INKY_LEFT_1, INKY_LEFT_2]
        self.STATES_RIGHT_NORMAL = [INKY_RIGHT_1, INKY_RIGHT_2]
        self.STATES_UP_NORMAL = [INKY_UP_1, INKY_UP_2]
        self.STATES_DOWN_NORMAL = [INKY_DOWN_1, INKY_DOWN_2]
        self.change_state('NORMAL')
        #self.SUBTYPE = 'INKY'

class Pinky(Ghost):
    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD):
        super().__init__(x=x, y=y, STEP=STEP, GO_OUT_THRESHOLD=GO_OUT_THRESHOLD)
        self.current_dir = 'DOWN'
        self.future_dir = 'DOWN'
        self.IMG = PINKY_DOWN_1
        self.STATES_LEFT_NORMAL = [PINKY_LEFT_1, PINKY_LEFT_2]
        self.STATES_RIGHT_NORMAL = [PINKY_RIGHT_1, PINKY_RIGHT_2]
        self.STATES_UP_NORMAL = [PINKY_UP_1, PINKY_UP_2]
        self.STATES_DOWN_NORMAL = [PINKY_DOWN_1, PINKY_DOWN_2]
        self.change_state('NORMAL')
        #self.SUBTYPE = 'PINKY'

class Clyde(Ghost):
    def __init__(self, x, y, STEP, GO_OUT_THRESHOLD):
        super().__init__(x=x, y=y, STEP=STEP, GO_OUT_THRESHOLD=GO_OUT_THRESHOLD)
        self.current_dir = 'UP'
        self.future_dir = 'UP'
        self.IMG = CLYDE_UP_1
        self.STATES_LEFT_NORMAL = [CLYDE_LEFT_1, CLYDE_LEFT_2]
        self.STATES_RIGHT_NORMAL = [CLYDE_RIGHT_1, CLYDE_RIGHT_2]
        self.STATES_UP_NORMAL = [CLYDE_UP_1, CLYDE_UP_2]
        self.STATES_DOWN_NORMAL = [CLYDE_DOWN_1, CLYDE_DOWN_2]
        self.change_state('NORMAL')
        #self.SUBTYPE = 'CLYDE'
