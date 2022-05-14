from .constants import FRUIT_1, FRUIT_2, FRUIT_3, FRUIT_4, FRUIT_5, FRUIT_6, FRUIT_7, FRUIT_8
from .sprite import Sprite

class Fruit(Sprite):
    HIDE_THRESHOLD = 300

    def __init__(self, x, y, lvl):
        super().__init__(IMG=None, TYPE='FRUIT', x=x, y=y)
        if lvl >= 8:
            self.type_num = 8
        else:
            self.type_num = lvl
        self.FRUIT_IMGS = [FRUIT_1, FRUIT_2, FRUIT_3, FRUIT_4, FRUIT_5, FRUIT_6, FRUIT_7, FRUIT_8]
        self.IMG = self.FRUIT_IMGS[self.type_num - 1]
        self.frames = 0
