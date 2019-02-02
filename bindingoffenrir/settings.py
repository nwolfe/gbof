# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
CYAN = (0, 255, 255)

# game settings
# WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
# HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
SCALE_FACTOR = 4
WIDTH = 256 * SCALE_FACTOR
HEIGHT = 240 * SCALE_FACTOR
FPS = 60
TITLE = 'G L E I P N I R :: Binding of Fenrir'
BGCOLOR = BLACK

TILESIZE = 16 * SCALE_FACTOR
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Images
PLAYER_IMAGE = 'player_sprite.png'
ENEMY_IMAGE = 'baddie_sprite.png'

# Levels
SAMPLE_LEVEL = 'sample_level.tmx'

# Player settings
PLAYER_SPEED = 5
PLAYER_STAIR_SPEED = PLAYER_SPEED / 2
