from pygame.image import load
from pygame.transform import scale

# screen refreshing frequency
FPS = 30

# screen dims and scale
WIDTH, HEIGHT = 700, 790
FACTOR = 3

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# assets
SPRITE_SHEET = load('assets/pacman1.png')
BACKGROUND = scale(SPRITE_SHEET.subsurface(228, 0, 452-228, 248), (FACTOR*(452-228), FACTOR*248)) # (x, y, w, h)
SMALL_BALL = scale(SPRITE_SHEET.subsurface(11, 11, 2, 2), (FACTOR*2, FACTOR*2))
BIG_BALL = scale(SPRITE_SHEET.subsurface(8, 24, 8, 8), (FACTOR*8, FACTOR*8))
PACMAN_RIGHT_1 = scale(SPRITE_SHEET.subsurface(457, 1, 13, 13), (FACTOR*13, FACTOR*13))
PACMAN_RIGHT_2 = scale(SPRITE_SHEET.subsurface(473, 1, 13, 13), (FACTOR*13, FACTOR*13))
PACMAN_LEFT_1 = scale(SPRITE_SHEET.subsurface(457, 17, 13, 13), (FACTOR*13, FACTOR*13))
PACMAN_LEFT_2 = scale(SPRITE_SHEET.subsurface(473, 17, 13, 13), (FACTOR*13, FACTOR*13))
PACMAN_UP_1 = scale(SPRITE_SHEET.subsurface(457, 34, 13, 13), (FACTOR*13, FACTOR*13))
PACMAN_UP_2 = scale(SPRITE_SHEET.subsurface(473, 34, 13, 13), (FACTOR*13, FACTOR*13))
PACMAN_DOWN_1 = scale(SPRITE_SHEET.subsurface(457, 49, 13, 13), (FACTOR*13, FACTOR*13))
PACMAN_DOWN_2 = scale(SPRITE_SHEET.subsurface(473, 49, 13, 13), (FACTOR*13, FACTOR*13))
PACMAN_FULL = scale(SPRITE_SHEET.subsurface(489, 1, 13, 13), (FACTOR*13, FACTOR*13))
PACMAN_LIFE = scale(SPRITE_SHEET.subsurface(587, 18, 10, 11), (10, 11))
PACMAN_DECAY_1 = scale(SPRITE_SHEET.subsurface(505, 1, 13, 15), (FACTOR*13, FACTOR*15))
PACMAN_DECAY_2 = scale(SPRITE_SHEET.subsurface(520, 1, 15, 15), (FACTOR*15, FACTOR*15))
PACMAN_DECAY_3 = scale(SPRITE_SHEET.subsurface(536, 1, 15, 15), (FACTOR*15, FACTOR*15))
PACMAN_DECAY_4 = scale(SPRITE_SHEET.subsurface(552, 1, 15, 15), (FACTOR*15, FACTOR*15))
PACMAN_DECAY_5 = scale(SPRITE_SHEET.subsurface(568, 1, 15, 15), (FACTOR*15, FACTOR*15))
PACMAN_DECAY_6 = scale(SPRITE_SHEET.subsurface(584, 1, 15, 15), (FACTOR*15, FACTOR*15))
PACMAN_DECAY_7 = scale(SPRITE_SHEET.subsurface(601, 1, 13, 15), (FACTOR*13, FACTOR*15))
PACMAN_DECAY_8 = scale(SPRITE_SHEET.subsurface(619, 1, 9, 15), (FACTOR*9, FACTOR*15))
PACMAN_DECAY_9 = scale(SPRITE_SHEET.subsurface(637, 1, 5, 15), (FACTOR*5, FACTOR*15))
PACMAN_DECAY_10 = scale(SPRITE_SHEET.subsurface(655, 1, 1, 15), (FACTOR*1, FACTOR*15))
PACMAN_DECAY_11 = scale(SPRITE_SHEET.subsurface(666, 6, 11, 11), (FACTOR*11, FACTOR*11))
BLINKY_RIGHT_1 = scale(SPRITE_SHEET.subsurface(457, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_RIGHT_2 = scale(SPRITE_SHEET.subsurface(473, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_LEFT_1 = scale(SPRITE_SHEET.subsurface(489, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_LEFT_2 = scale(SPRITE_SHEET.subsurface(505, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_UP_1 = scale(SPRITE_SHEET.subsurface(521, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_UP_2 = scale(SPRITE_SHEET.subsurface(537, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_DOWN_1 = scale(SPRITE_SHEET.subsurface(553, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_DOWN_2 = scale(SPRITE_SHEET.subsurface(569, 65, 14, 14), (FACTOR*14, FACTOR*14))

# background reference point
BG_X = (WIDTH - BACKGROUND.get_width()) // 2
BG_Y = (HEIGHT - BACKGROUND.get_height()) // 2
