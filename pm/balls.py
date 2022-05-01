from .sprite import Sprite
from .constants import SMALL_BALL, BIG_BALL

class SmallBall(Sprite):
    def __init__(self, x, y):
        super().__init__(IMG=SMALL_BALL, TYPE='SMALL_BALL',x=x, y=y)

class BigBall(SmallBall):
    REPLICATE = 6 # the extension of the lifetime of the current IMG

    def __init__(self, x, y):
        super().__init__(x=x, y=y)
        self.IMG = BIG_BALL
        self.TYPE = 'BIG_BALL'
        self.img_state = 0
        self.IMG_WIDTH = BIG_BALL.get_width()

    def change_image(self):
        STATES = tuple(enumerate((BIG_BALL, ) * self.REPLICATE + (None, ) * self.REPLICATE))

        if self.img_state == len(STATES) - 1:
            self.IMG = BIG_BALL
            self.img_state = 0
            return

        for state, image in STATES:
            if state == self.img_state:
                self.IMG = STATES[STATES.index((state, image)) + 1][1]
                self.img_state = state + 1
                break
