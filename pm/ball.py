from .sprite import Sprite
from .constants import SMALL_BALL

class SmallBall(Sprite):
    def __init__(self, x, y):
        super().__init__(IMG=SMALL_BALL, TYPE='SMALL_BALL',x=x, y=y)
