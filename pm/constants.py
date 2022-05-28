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

# basic assets
SPRITE_SHEET = load('assets/pacman1.png')
BACKGROUND = scale(SPRITE_SHEET.subsurface(228, 0, 452-228, 248), (FACTOR*(452-228), FACTOR*248)) # (x, y, w, h)
SMALL_BALL = scale(SPRITE_SHEET.subsurface(11, 11, 2, 2), (FACTOR*2, FACTOR*2))
BIG_BALL = scale(SPRITE_SHEET.subsurface(8, 24, 8, 8), (FACTOR*8, FACTOR*8))

# pacman's assets
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

# ghosts' assets
# Blinky
BLINKY_RIGHT_1 = scale(SPRITE_SHEET.subsurface(457, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_RIGHT_2 = scale(SPRITE_SHEET.subsurface(473, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_LEFT_1 = scale(SPRITE_SHEET.subsurface(489, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_LEFT_2 = scale(SPRITE_SHEET.subsurface(505, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_UP_1 = scale(SPRITE_SHEET.subsurface(521, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_UP_2 = scale(SPRITE_SHEET.subsurface(537, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_DOWN_1 = scale(SPRITE_SHEET.subsurface(553, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLINKY_DOWN_2 = scale(SPRITE_SHEET.subsurface(569, 65, 14, 14), (FACTOR*14, FACTOR*14))
# Pinky
PINKY_RIGHT_1 = scale(SPRITE_SHEET.subsurface(457, 81, 14, 14), (FACTOR*14, FACTOR*14))
PINKY_RIGHT_2 = scale(SPRITE_SHEET.subsurface(473, 81, 14, 14), (FACTOR*14, FACTOR*14))
PINKY_LEFT_1 = scale(SPRITE_SHEET.subsurface(489, 81, 14, 14), (FACTOR*14, FACTOR*14))
PINKY_LEFT_2 = scale(SPRITE_SHEET.subsurface(505, 81, 14, 14), (FACTOR*14, FACTOR*14))
PINKY_UP_1 = scale(SPRITE_SHEET.subsurface(521, 81, 14, 14), (FACTOR*14, FACTOR*14))
PINKY_UP_2 = scale(SPRITE_SHEET.subsurface(537, 81, 14, 14), (FACTOR*14, FACTOR*14))
PINKY_DOWN_1 = scale(SPRITE_SHEET.subsurface(553, 81, 14, 14), (FACTOR*14, FACTOR*14))
PINKY_DOWN_2 = scale(SPRITE_SHEET.subsurface(569, 81, 14, 14), (FACTOR*14, FACTOR*14))
# Inky
INKY_RIGHT_1 = scale(SPRITE_SHEET.subsurface(457, 97, 14, 14), (FACTOR*14, FACTOR*14))
INKY_RIGHT_2 = scale(SPRITE_SHEET.subsurface(473, 97, 14, 14), (FACTOR*14, FACTOR*14))
INKY_LEFT_1 = scale(SPRITE_SHEET.subsurface(489, 97, 14, 14), (FACTOR*14, FACTOR*14))
INKY_LEFT_2 = scale(SPRITE_SHEET.subsurface(505, 97, 14, 14), (FACTOR*14, FACTOR*14))
INKY_UP_1 = scale(SPRITE_SHEET.subsurface(521, 97, 14, 14), (FACTOR*14, FACTOR*14))
INKY_UP_2 = scale(SPRITE_SHEET.subsurface(537, 97, 14, 14), (FACTOR*14, FACTOR*14))
INKY_DOWN_1 = scale(SPRITE_SHEET.subsurface(553, 97, 14, 14), (FACTOR*14, FACTOR*14))
INKY_DOWN_2 = scale(SPRITE_SHEET.subsurface(569, 97, 14, 14), (FACTOR*14, FACTOR*14))
# Clyde
CLYDE_RIGHT_1 = scale(SPRITE_SHEET.subsurface(457, 113, 14, 14), (FACTOR*14, FACTOR*14))
CLYDE_RIGHT_2 = scale(SPRITE_SHEET.subsurface(473, 113, 14, 14), (FACTOR*14, FACTOR*14))
CLYDE_LEFT_1 = scale(SPRITE_SHEET.subsurface(489, 113, 14, 14), (FACTOR*14, FACTOR*14))
CLYDE_LEFT_2 = scale(SPRITE_SHEET.subsurface(505, 113, 14, 14), (FACTOR*14, FACTOR*14))
CLYDE_UP_1 = scale(SPRITE_SHEET.subsurface(521, 113, 14, 14), (FACTOR*14, FACTOR*14))
CLYDE_UP_2 = scale(SPRITE_SHEET.subsurface(537, 113, 14, 14), (FACTOR*14, FACTOR*14))
CLYDE_DOWN_1 = scale(SPRITE_SHEET.subsurface(553, 113, 14, 14), (FACTOR*14, FACTOR*14))
CLYDE_DOWN_2 = scale(SPRITE_SHEET.subsurface(569, 113, 14, 14), (FACTOR*14, FACTOR*14))
# other
BLUE_1 = scale(SPRITE_SHEET.subsurface(585, 65, 14, 14), (FACTOR*14, FACTOR*14))
BLUE_2 = scale(SPRITE_SHEET.subsurface(601, 65, 14, 14), (FACTOR*14, FACTOR*14))
GREY_1 = scale(SPRITE_SHEET.subsurface(617, 65, 14, 14), (FACTOR*14, FACTOR*14))
GREY_2 = scale(SPRITE_SHEET.subsurface(633, 65, 14, 14), (FACTOR*14, FACTOR*14))
EYES_RIGHT = scale(SPRITE_SHEET.subsurface(585, 81, 14, 14), (FACTOR*14, FACTOR*14))
EYES_LEFT = scale(SPRITE_SHEET.subsurface(601, 81, 14, 14), (FACTOR*14, FACTOR*14))
EYES_UP = scale(SPRITE_SHEET.subsurface(617, 81, 14, 14), (FACTOR*14, FACTOR*14))
EYES_DOWN = scale(SPRITE_SHEET.subsurface(633, 81, 14, 14), (FACTOR*14, FACTOR*14))

# fruit's assets
FRUIT_1 = scale(SPRITE_SHEET.subsurface(490, 49, 14, 14), (FACTOR*14, FACTOR*14))
FRUIT_2 = scale(SPRITE_SHEET.subsurface(506, 49, 14, 14), (FACTOR*14, FACTOR*14))
FRUIT_3 = scale(SPRITE_SHEET.subsurface(522, 49, 14, 14), (FACTOR*14, FACTOR*14))
FRUIT_4 = scale(SPRITE_SHEET.subsurface(538, 49, 14, 14), (FACTOR*14, FACTOR*14))
FRUIT_5 = scale(SPRITE_SHEET.subsurface(555, 49, 14, 14), (FACTOR*14, FACTOR*14))
FRUIT_6 = scale(SPRITE_SHEET.subsurface(570, 49, 14, 14), (FACTOR*14, FACTOR*14))
FRUIT_7 = scale(SPRITE_SHEET.subsurface(586, 49, 14, 14), (FACTOR*14, FACTOR*14))
FRUIT_8 = scale(SPRITE_SHEET.subsurface(604, 49, 14, 14), (FACTOR*14, FACTOR*14))

# fruit's captions
FRUIT_CAPTION_1 = scale(SPRITE_SHEET.subsurface(458, 148, 13, 7), (FACTOR*13, FACTOR*7))
FRUIT_CAPTION_2 = scale(SPRITE_SHEET.subsurface(472, 148, 15, 7), (FACTOR*15, FACTOR*7))
FRUIT_CAPTION_3 = scale(SPRITE_SHEET.subsurface(488, 148, 15, 7), (FACTOR*15, FACTOR*7))
FRUIT_CAPTION_4 = scale(SPRITE_SHEET.subsurface(504, 148, 15, 7), (FACTOR*15, FACTOR*7))
FRUIT_CAPTION_5 = scale(SPRITE_SHEET.subsurface(520, 148, 18, 7), (FACTOR*18, FACTOR*7))
FRUIT_CAPTION_6 = scale(SPRITE_SHEET.subsurface(518, 164, 20, 7), (FACTOR*20, FACTOR*7))
FRUIT_CAPTION_7 = scale(SPRITE_SHEET.subsurface(518, 180, 20, 7), (FACTOR*20, FACTOR*7))
FRUIT_CAPTION_8 = scale(SPRITE_SHEET.subsurface(518, 196, 20, 7), (FACTOR*20, FACTOR*7))

# ghosts' captions
GHOST_CAPTION_1 = scale(SPRITE_SHEET.subsurface(456, 133, 15, 7), (FACTOR*15, FACTOR*7))
GHOST_CAPTION_2 = scale(SPRITE_SHEET.subsurface(472, 133, 15, 7), (FACTOR*15, FACTOR*7))
GHOST_CAPTION_3 = scale(SPRITE_SHEET.subsurface(488, 133, 15, 7), (FACTOR*15, FACTOR*7))
GHOST_CAPTION_4 = scale(SPRITE_SHEET.subsurface(504, 133, 16, 7), (FACTOR*16, FACTOR*7))

# background reference point
BG_X = (WIDTH - BACKGROUND.get_width()) // 2
BG_Y = (HEIGHT - BACKGROUND.get_height()) // 2
