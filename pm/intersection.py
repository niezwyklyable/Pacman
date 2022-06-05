from .sprite import Sprite

class Intersection(Sprite):
    def __init__(self, x, y, **kwargs):
        super().__init__(IMG=None, TYPE='INTERSECTION', x=x, y=y)
        self.dirs = kwargs

    # overriding this method because objects instantiated from this class will be invisible
    def draw(self, win):
        pass
