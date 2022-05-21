from .sprite import Sprite
from pygame import draw
from .constants import RED

class Intersection(Sprite):
    def __init__(self, x, y, **kwargs):
        super().__init__(IMG=None, TYPE='INTERSECTION', x=x, y=y)
        self.dirs = kwargs

    # overriding this method because objects instantiated from this class will be invisible
    def draw(self, win):
        pass
        #draw.rect(win, RED, (self.x - 3, self.y - 3, 6, 6), 5) # for testing purposes
