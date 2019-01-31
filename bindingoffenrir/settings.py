# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
# WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
# HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
WIDTH = 256 * 4
HEIGHT = 240 * 4
SCALE = (WIDTH, HEIGHT)
FPS = 60
TITLE = 'G L E I P N I R :: Binding of Fenrir'
BGCOLOR = WHITE

TILESIZE = 16 * 4
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Images
PLAYER_IMAGE = 'player_sprite.png'
ENEMY_IMAGE = 'baddie_sprite.png'

# Levels
SAMPLE_LEVEL = 'sample_level.tmx'
