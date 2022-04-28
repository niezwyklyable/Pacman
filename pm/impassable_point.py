from .sprite import Sprite
from pygame import draw
from .constants import RED

class ImpassablePoint(Sprite):
    def __init__(self, x, y):
        super().__init__(IMG=None, TYPE='IMPASSABLE_POINT', x=x, y=y)

    # overriding this method because objects instantiated from this class will be invisible
    def draw(self, win):
        #pass
        draw.rect(win, RED, (self.x, self.y, 2, 2), 2) # for testing purposes
