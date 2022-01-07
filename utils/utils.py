from typing import Tuple, List

from pygame import Rect

from utils.types import Direction, Side, Corner
from utils.constants import DX, DY, EXIT_TILE_TYPE, TILE_SIZE, WALL_W, FIELD_HEIGHT_INNER, FIELD_WIDTH_INNER, FIELD_TILES_H, FIELD_TILES_W

def make_step(speed:int, direction:Direction) -> Tuple:
    if direction == Direction.LEFT:
        return (- speed * DX, 0)
    elif direction == Direction.RIGHT:
        return (speed * DX, 0)
    elif direction == Direction.UP:
        return (0, -speed * DY)
    elif direction == Direction.DOWN:
        return (0, speed * DY)
    else:
        return (0, 0) 

def cell_size_in_pixel() -> Tuple:
    return (DX, DY)

def tile_size_in_pixel() -> Tuple:
    return (DX * TILE_SIZE, DY * TILE_SIZE)

def tile_size_in_cells() -> Tuple:
    return (TILE_SIZE, TILE_SIZE)

def wall_tile_size_in_pixel(side:Side) -> Tuple:
    if side in (Side.LEFT, Side.RIGHT):
        return (DX * WALL_W, DY * TILE_SIZE)
    elif side in (Side.UP, Side.DOWN):
        return (DX * TILE_SIZE, DX * WALL_W)
    else:
        return (0, 0)        

def wall_tile_size_in_cells(side:Side) -> Tuple:
    if side in (Side.LEFT, Side.RIGHT):
        return (WALL_W, TILE_SIZE)
    elif side in (Side.UP, Side.DOWN):
        return (TILE_SIZE, WALL_W)
    else:
        return (0, 0)        

def wall_corner_tile_size_in_cells() -> Tuple:
    return (WALL_W, WALL_W)

def cell_pos_to_pixel(x:int, y:int) -> Tuple:
    return (x * DX, y * DY)



def tile_pos_to_pixel(x:int, y:int) -> Tuple:
    return (WALL_W * DX + x * DX * TILE_SIZE, WALL_W * DY + y * DY * TILE_SIZE)

def wall_tile_pos_to_pixel(x:int, y:int, side:Side) -> Tuple:
    if side == Side.LEFT:
        return (0, WALL_W * DY + y * DY * TILE_SIZE)
    elif side == Side.RIGHT:
        return (WALL_W * DX + FIELD_WIDTH_INNER, WALL_W * DY + y * DY * TILE_SIZE)
    elif side == Side.UP:
        return (WALL_W * DX + x * DX * TILE_SIZE, 0)
    elif side == Side.DOWN:
        return (WALL_W * DX + x * DX * TILE_SIZE, WALL_W * DY + FIELD_HEIGHT_INNER)
    else:
        return (0, 0)        

def wall_corner_tile_pos_to_pixel(corner:Corner) -> Tuple:
    if corner == Corner.LEFT_UPPER:
        return (0, 0)
    elif corner == Corner.RIGHT_UPPER:
        return (WALL_W * DX + FIELD_WIDTH_INNER, 0)
    elif corner == Corner.LEFT_BOTTOM:
        return (0, WALL_W * DY + FIELD_HEIGHT_INNER)
    elif corner == Corner.RIGHT_BOTTOM:
        return (WALL_W * DX + FIELD_WIDTH_INNER, WALL_W * DY + FIELD_HEIGHT_INNER)
    else:
        return (0, 0)        

def tile_pos_to_cell(x:int, y:int) -> Tuple:
    return (WALL_W + x * TILE_SIZE, WALL_W + y * TILE_SIZE)

def cell_pos_to_tile(x:int, y:int) -> Tuple:
    return ((x - WALL_W) // TILE_SIZE, (y - WALL_W) // TILE_SIZE)

def pixel_pos_to_tile(x:int, y:int) -> Tuple:
    return ((x - DX * WALL_W) // (DX * TILE_SIZE), (y - DY * WALL_W) // (DY * TILE_SIZE))

def pixel_pos_to_cell(x:int, y:int) -> Tuple:
    return (x // DX, y // DY)

def get_opposite_direction(direction:Direction):
    if direction == Direction.UP:
        return Direction.DOWN
    elif direction == Direction.DOWN:
        return Direction.UP
    elif direction == Direction.LEFT:
        return Direction.RIGHT
    elif direction == Direction.RIGHT:
        return Direction.LEFT
    return Direction.NONE

def is_position_in_tile(cellx:int, celly:int, mode:int=0):
    if mode == 0:
        return cellx % TILE_SIZE == 0 and celly % TILE_SIZE == 0
    elif mode == 1:
        return cellx % TILE_SIZE == 0
    elif mode == 2:
        return celly % TILE_SIZE == 0
    else:
        raise Exception('mode should be in [0, 1, 2]')


def position_in_tile(cellx:int, celly:int):
    if is_position_in_tile(cellx, celly): 
        return (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)
    elif is_position_in_tile(cellx, celly, 1):
        return (Direction.UP, Direction.DOWN)
    elif is_position_in_tile(cellx, celly, 2):
        return (Direction.LEFT, Direction.RIGHT)
    else:
        return Direction.NONE


def collision_rect(rect1:Rect, rect2:Rect):
    left = max(rect1.left, rect2.left)
    right = min(rect1.right, rect2.right)
    top = max(rect1.top, rect2.top)
    bottom = min(rect1.bottom, rect2.bottom)
    if left < right and top < bottom:
        return Rect(left, top, right - left, bottom - top)
    else:
         return None

def get_tiles_collision(cellx, celly, o_cellx, o_celly) -> Side:
    if cellx + TILE_SIZE > o_cellx and cellx < o_cellx and celly == o_celly:
        return Side.RIGHT
    elif cellx < o_cellx + TILE_SIZE and cellx + TILE_SIZE > o_cellx + TILE_SIZE and celly == o_celly:
        return Side.LEFT
    elif celly + TILE_SIZE > o_celly and celly < o_celly and cellx == o_cellx:
        return Side.DOWN
    elif celly < o_celly + TILE_SIZE and celly + TILE_SIZE > o_celly + TILE_SIZE and cellx == o_cellx: 
        return Side.UP
    elif cellx == o_cellx and celly == o_celly:
        return Side.LEFT # 
    else: 
        return Side.NONE 

def get_collided_tiles(cellx:int, celly:int, obstacles:List):
    collided = []
    for o in obstacles:
        side = get_tiles_collision(cellx, celly, o[0] * TILE_SIZE, o[1] * TILE_SIZE)
        if side != Side.NONE:
            collided.append((o, side))
    return collided

def tile_position_collided(old_position:Tuple[int], new_position:Tuple[int], level) -> Tuple[int]:
    posx  = new_position[0]
    posy = new_position[1]

    oldposx = old_position[0]
    oldposy = old_position[1]
    if is_position_in_tile(oldposx, oldposy):
        collided = get_collided_tiles(posx, posy, level.get_neighbour_obstacle_tiles(oldposx, oldposy))
        if len(collided) > 0:
            pos = collided[0][0]
            side = collided[0][1]
            if side == Side.RIGHT:
                posx = (pos[0] - 1) * TILE_SIZE
            elif side == Side.LEFT:
                posx = (pos[0] + 1) * TILE_SIZE
            elif side == Side.DOWN:
                posy = (pos[1] - 1) * TILE_SIZE
            elif side == Side.UP:
                posy = (pos[1] + 1) * TILE_SIZE
    return (posx, posy)


def wall_position_collided(new_position:Tuple[int], level) -> Tuple[int]:
    posx  = new_position[0]
    posy = new_position[1]

    if posx < 0:
        posx = 0
    if posy < 0:
        posy = 0

    limitx = (FIELD_TILES_W - 1)* TILE_SIZE
    if posx > limitx:
        posx = limitx

    limity = (FIELD_TILES_H - 1) * TILE_SIZE
    if posy > limity:
        posy = limity
    
    
    return (posx, posy)


def exit_position_collided(position:Tuple[int], level) -> Tuple[int]:
    posx  = round(position[0] / TILE_SIZE) * TILE_SIZE
    posy = round(position[1] / TILE_SIZE) * TILE_SIZE
    # if is_position_in_tile(posx, posy):
    exit_tile = level.exit
    collided = get_collided_tiles(posx, posy, [exit_tile[0]])
    return  len(collided) > 0 and level.floor[exit_tile[0]] == EXIT_TILE_TYPE

    return False

