from .constants import FRUIT_1, FRUIT_2, FRUIT_3, FRUIT_4, FRUIT_5, FRUIT_6, FRUIT_7,\
     FRUIT_8, FRUIT_CAPTION_1, FRUIT_CAPTION_2, FRUIT_CAPTION_3, FRUIT_CAPTION_4,\
         FRUIT_CAPTION_5, FRUIT_CAPTION_6, FRUIT_CAPTION_7, FRUIT_CAPTION_8
from .sprite import Sprite

class Fruit(Sprite):
    HIDE_THRESHOLD = 300

    def __init__(self, x, y, lvl):
        super().__init__(IMG=None, TYPE='FRUIT', x=x, y=y)
        if lvl >= 8:
            self.type_num = 8
        else:
            self.type_num = lvl
        self.FRUIT_IMGS = [FRUIT_1, FRUIT_2, FRUIT_3, FRUIT_4, FRUIT_5, FRUIT_6, \
            FRUIT_7, FRUIT_8]
        self.IMG = self.FRUIT_IMGS[self.type_num - 1]
        self.frames = 0

class FruitCaption(Fruit):
    HIDE_THRESHOLD = 50

    def __init__(self, x, y, lvl):
        super().__init__(x=x, y=y, lvl=lvl)
        self.TYPE = 'FRUIT_CAPTION'
        self.FRUIT_CAPTIONS = [FRUIT_CAPTION_1, FRUIT_CAPTION_2, FRUIT_CAPTION_3,\
             FRUIT_CAPTION_4, FRUIT_CAPTION_5, FRUIT_CAPTION_6, FRUIT_CAPTION_7,\
                  FRUIT_CAPTION_8]
        self.VALUES = [100, 300, 500, 700, 1000, 2000, 3000, 5000]
        self.IMG = self.FRUIT_CAPTIONS[self.type_num - 1]
        self.VALUE = self.VALUES[self.type_num - 1]
