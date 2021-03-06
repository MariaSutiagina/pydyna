from pygame import USEREVENT

FRAME_RATE: float = 30


CELL_W: int = 6 # game cell width in pixels
CELL_H: int = 6  # game cell height in pixels

DX: int = CELL_W # object movement min step on X
DY: int = CELL_H # object movement min step on Y

TILE_SIZE = 12    # tile size in cells
WALL_W = 8       # wall widht in cells

TILE_WIDTH_IN_PIXEL = CELL_W * TILE_SIZE
TILE_HEIGHT_IN_PIXEL = CELL_H * TILE_SIZE

FIELD_TILES_W = 15 # tiles in field on X
FIELD_TILES_H = 11 # tiles in field on Y

FIELD_X_INNER = CELL_W * WALL_W
FIELD_Y_INNER = CELL_H * WALL_W

FIELD_WIDTH_INNER: int = FIELD_TILES_W * TILE_SIZE * CELL_W
FIELD_HEIGHT_INNER: int = FIELD_TILES_H * TILE_SIZE * CELL_H

FIELD_WIDTH:int = 2 * CELL_W * WALL_W + FIELD_WIDTH_INNER
FIELD_HEIGHT:int = 2 * CELL_H * WALL_W + FIELD_HEIGHT_INNER

DIRECTION_CHANGE_FACTOR = 5


KEYBOARD = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

DB_FILENAME = 'resources/data/levels'

ANIMATION_PERIOD = 250
MOVEMENT_TIMEOUT = 300
EXIT_TIMEOUT = 1000

FADE_TIMEOUT = 2000
EXPLOSION_TIMEOUT = 2500
EXPLOSION_DURATION = 1000
TITLESCREEN_TIMEOUT = 50000
ROUND_TIMEOUT = 300000
RANDOM_CHILDREN_COUNT = 5

BRICK_HARDNESS_MAX = 16
BRICK_SOLID_TYPE = 255
EXIT_TILE_TYPE = 127
TREASURE_TILE_TYPE = 128
TREASURE_TYPES_COUNT = 9
TREASURE_TIMEOUT = 60
MAX_SPEED = 4
MAX_BOMB_STRENGTH = 6

BRICK_SCORE = 10
ROUND_SCORE = 50
LEVEL_SCORE = 100
TREASURE_SCORE = 20


GAME_FONT_PATH = 'resources/fonts/Elfboyclassic.ttf'

#user events
E_BOMB = USEREVENT + 1
E_EXIT = USEREVENT + 2
E_MONSTER = USEREVENT + 3
E_TREASURE = USEREVENT + 4
E_BRICK = USEREVENT + 5

