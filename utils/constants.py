FRAME_RATE: float = 30


CELL_W: int = 6 # game cell width in pixels
CELL_H: int = 6  # game cell height in pixels

DX: int = CELL_W # object movement min step on X
DY: int = CELL_H # object movement min step on Y

TILE_SIZE = 12    # tile size in cells
WALL_W = 8       # wall widht in cells

TILE_WIDTH_IN_PIXEL = CELL_W * TILE_SIZE
TILE_HEIGHT_IN_PIXEL = CELL_H * TILE_SIZE

FIELD_TILES_W = 16 # tiles in field on X
FIELD_TILES_H = 12 # tiles in field on Y

FIELD_X_INNER = CELL_W * WALL_W
FIELD_Y_INNER = CELL_H * WALL_W

FIELD_WIDTH_INNER: int = FIELD_TILES_W * TILE_SIZE * CELL_W
FIELD_HEIGHT_INNER: int = FIELD_TILES_H * TILE_SIZE * CELL_H

FIELD_WIDTH:int = 2 * CELL_W * WALL_W + FIELD_WIDTH_INNER
FIELD_HEIGHT:int = 2 * CELL_H * WALL_W + FIELD_HEIGHT_INNER

DIRECTION_CHANGE_FACTOR = 2