from .sprite import Sprite
from .constants import SMALL_BALL, BIG_BALL

class SmallBall(Sprite):
    def __init__(self, x, y):
        super().__init__(IMG=SMALL_BALL, TYPE='SMALL_BALL',x=x, y=y)

class BigBall(SmallBall):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)
        self.IMG = BIG_BALL
        self.TYPE = 'BIG_BALL'
