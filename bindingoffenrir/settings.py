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
# TRANSPARENT = (215, 123, 186) #Hot Pink (alpha 255)
TRANSPARENT = BLACK

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

# Render ordering layers
LAYER_PLAYER = 2
LAYER_BADDIE = 1

# Images
PLAYER_SPRITESHEET = 'player_sheet.png'
PLAYER_MOVE_IMAGES = [
    'step1',
    'step2',
    'step3'
]
PLAYER_IDLE_IMAGES = [
    'idle'
]
ENEMY_IMAGE = 'baddie_sprite.png'

# Levels
SAMPLE_LEVEL = ['sample', 'sample_level.tmx']
LEVELS = [
    ['level1', [
        'level1_stage1.tmx',
        'level1_stage2.tmx'
    ]]
]

# Player settings
PLAYER_ACC = 1  # 0.5
PLAYER_FRICTION = 0.2  # 0.12
PLAYER_GRAVITY = 0.5
PLAYER_STAIR_SPEED = 2.5
PLAYER_JUMP_HEIGHT = 12
PLAYER_JUMP_COOLDOWN = 900
