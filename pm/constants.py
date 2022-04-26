from pygame.image import load
from pygame.transform import scale

# screen refreshing frequency
FPS = 30

# screen dims and scale
WIDTH, HEIGHT = 700, 770
FACTOR = 3

# colors
BLACK = (0, 0, 0)
#WHITE = (255, 255, 255)

# assets
SPRITE_SHEET = load('assets/pacman1.png')
BACKGROUND = scale(SPRITE_SHEET.subsurface(228, 0, 452-228, 248), (FACTOR*(452-228), FACTOR*248)) # (x, y, w, h)
SMALL_BALL = scale(SPRITE_SHEET.subsurface(11, 11, 2, 2), (FACTOR*2, FACTOR*2))

# background reference point
BG_X = (WIDTH - BACKGROUND.get_width()) // 2
BG_Y = (HEIGHT - BACKGROUND.get_height()) // 2
