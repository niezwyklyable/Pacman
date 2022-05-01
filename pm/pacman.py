from .sprite import Sprite
from .constants import PACMAN_LEFT_1, PACMAN_LEFT_2, PACMAN_RIGHT_1, PACMAN_RIGHT_2,\
     PACMAN_UP_1, PACMAN_UP_2, PACMAN_DOWN_1, PACMAN_DOWN_2, PACMAN_FULL, FACTOR, WHITE
from pygame import draw

class Pacman(Sprite):
    STEP = 2 # be careful with it.. (it has a linkage with collision_detection method in the Game class)
    REPLICATE = 2 # the extension of the lifetime of the current IMG

    def __init__(self, x, y):
        super().__init__(IMG=PACMAN_FULL, TYPE='PACMAN', x=x, y=y)
        self.current_dir = 'LEFT'
        self.future_dir = 'LEFT'
        self.img_state = 0 # PACMAN_FULL image always independently from a dir

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
        if self.current_dir == 'LEFT':
            STATES = tuple(enumerate((PACMAN_FULL, ) * self.REPLICATE + (PACMAN_LEFT_2, ) * self.REPLICATE + \
                (PACMAN_LEFT_1, ) * self.REPLICATE + (PACMAN_LEFT_2, ) * self.REPLICATE))
        elif self.current_dir == 'RIGHT':
            STATES = tuple(enumerate((PACMAN_FULL, ) * self.REPLICATE + (PACMAN_RIGHT_2, ) * self.REPLICATE + \
                (PACMAN_RIGHT_1, ) * self.REPLICATE + (PACMAN_RIGHT_2, ) * self.REPLICATE))
        elif self.current_dir == 'UP':
            STATES = tuple(enumerate((PACMAN_FULL, ) * self.REPLICATE + (PACMAN_UP_2, ) * self.REPLICATE + \
                (PACMAN_UP_1, ) * self.REPLICATE + (PACMAN_UP_2, ) * self.REPLICATE))
        elif self.current_dir == 'DOWN':
            STATES = tuple(enumerate((PACMAN_FULL, ) * self.REPLICATE + (PACMAN_DOWN_2, ) * self.REPLICATE + \
                (PACMAN_DOWN_1, ) * self.REPLICATE + (PACMAN_DOWN_2, ) * self.REPLICATE))
        else:
            return # if Pacman's current_dir is None

        if self.img_state == len(STATES) - 1:
            self.IMG = PACMAN_FULL
            self.img_state = 0
            return

        for state, image in STATES:
            if state == self.img_state:
                self.IMG = STATES[STATES.index((state, image)) + 1][1]
                self.img_state = state + 1
                break
