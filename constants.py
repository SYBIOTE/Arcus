# constants
import pygame
pygame.init()
dimensions = pygame.display.Info()
WIDTH = dimensions.current_w
HEIGHT = dimensions.current_h-20
FPS = 60
GRAVITY = 0.01
PI = 3.142

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BRIGHT_GREEN = (0, 255, 0)
SKY_BLUE = (0, 255, 255)
BLUE = (0, 0, 255)
GREEN_YELLOW=(181,255,98)
BROWN=(204,102,0)
DARK_BROWN=(204,76,0)

HIGHSCORE_FILE="highscore.txt"
ARROW_IMAGE = "assets/laser.png"
BACKGROUND_IMAGE = "assets/back.png"
TITLE_SCREEN="assets/lasertitle.png"
EXPLOSION_SOUND = "assets/boom.wav"
CLICK_SOUND = "assets/select.wav"
MUSIC_FILE = "assets/tgfcoder-FrozenJam-SeamlessLoop.ogg"
VOLUME = 0.2

ARROW_SIZE = (16, 150)
BALOON_SIZE = (100, 100)
HIT_RADIUS = 15
MISSES = 15