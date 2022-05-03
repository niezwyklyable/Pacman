from .sprite import Sprite
from .constants import PACMAN_LEFT_1, PACMAN_LEFT_2, PACMAN_RIGHT_1, PACMAN_RIGHT_2,\
     PACMAN_UP_1, PACMAN_UP_2, PACMAN_DOWN_1, PACMAN_DOWN_2, PACMAN_FULL, FACTOR, WHITE
from pygame import draw

class Pacman(Sprite):
    #STEP = 2 # be careful with it.. (it has a linkage with collision_detection method in the Game class)
    REPLICATE = 2 # the extension of the lifetime of the current IMG

    def __init__(self, x, y, STEP):
        super().__init__(IMG=PACMAN_FULL, TYPE='PACMAN', x=x, y=y)
        self.STEP = STEP
        self.current_dir = 'LEFT'
        self.future_dir = 'LEFT'
        self.img_state = 0 # PACMAN_FULL image always independently from a dir
        self.STATES_LEFT = [PACMAN_FULL, PACMAN_LEFT_2, PACMAN_LEFT_1, PACMAN_LEFT_2]
        self.STATES_RIGHT = [PACMAN_FULL, PACMAN_RIGHT_2, PACMAN_RIGHT_1, PACMAN_RIGHT_2]
        self.STATES_UP = [PACMAN_FULL, PACMAN_UP_2, PACMAN_UP_1, PACMAN_UP_2]
        self.STATES_DOWN = [PACMAN_FULL, PACMAN_DOWN_2, PACMAN_DOWN_1, PACMAN_DOWN_2]

    def set_future_dir(self, dir):
        if dir == 'LEFT':
            self.future_dir = 'LEFT'
        elif dir == 'RIGHT':
            self.future_dir = 'RIGHT'
        elif dir == 'UP':
            self.future_dir = 'UP'
        elif dir == 'DOWN':
            self.future_dir = 'DOWN'

    def change_dir(self):
        self.current_dir = self.future_dir

    def stop(self):
        self.current_dir = None

    def move(self):
        if self.current_dir == 'LEFT':
            self.x -= self.STEP * FACTOR
        elif self.current_dir == 'RIGHT':
            self.x += self.STEP * FACTOR
        elif self.current_dir == 'UP':
            self.y -= self.STEP * FACTOR
        elif self.current_dir == 'DOWN':
            self.y += self.STEP * FACTOR
        else:
            pass # do nothing if current_dir is None

    def draw(self, win):
        super().draw(win)
        if self.future_dir == 'LEFT':
            draw.polygon(win, WHITE, [(self.x - self.IMG.get_width() // 2 - FACTOR * 5, self.y), \
                (self.x - self.IMG.get_width() // 2 - FACTOR * 3, self.y - FACTOR * 2),\
                    (self.x - self.IMG.get_width() // 2 - FACTOR * 3, self.y + FACTOR * 2)])
        elif self.future_dir == 'RIGHT':
            draw.polygon(win, WHITE, [(self.x + self.IMG.get_width() // 2 + FACTOR * 5, self.y), \
                (self.x + self.IMG.get_width() // 2 + FACTOR * 3, self.y - FACTOR * 2),\
                    (self.x + self.IMG.get_width() // 2 + FACTOR * 3, self.y + FACTOR * 2)])
        elif self.future_dir == 'UP':
            draw.polygon(win, WHITE, [(self.x, self.y - self.IMG.get_height() // 2 - FACTOR * 5), \
                (self.x - FACTOR * 2, self.y - self.IMG.get_height() // 2 - FACTOR * 3),\
                    (self.x + FACTOR * 2, self.y - self.IMG.get_height() // 2 - FACTOR * 3)])
        elif self.future_dir == 'DOWN':
            draw.polygon(win, WHITE, [(self.x, self.y + self.IMG.get_height() // 2 + FACTOR * 5), \
                (self.x - FACTOR * 2, self.y + self.IMG.get_height() // 2 + FACTOR * 3),\
                    (self.x + FACTOR * 2, self.y + self.IMG.get_height() // 2 + FACTOR * 3)])

    def change_image(self):
        t = tuple()
        if self.current_dir == 'LEFT':
            for s in self.STATES_LEFT:
                t += (s, ) * self.REPLICATE
        elif self.current_dir == 'RIGHT':
            for s in self.STATES_RIGHT:
                t += (s, ) * self.REPLICATE
        elif self.current_dir == 'UP':
            for s in self.STATES_UP:
                t += (s, ) * self.REPLICATE
        elif self.current_dir == 'DOWN':
            for s in self.STATES_DOWN:
                t += (s, ) * self.REPLICATE
        else:
            return # if Pacman's current_dir is None

        states = tuple(enumerate(t))
        if self.img_state == len(states) - 1:
            self.IMG = states[0][1] # PACMAN_FULL
            self.img_state = 0
            return

        for state, image in states:
            if state == self.img_state:
                self.IMG = states[states.index((state, image)) + 1][1]
                self.img_state = state + 1
                break
