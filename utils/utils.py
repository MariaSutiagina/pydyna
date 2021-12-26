from typing import Tuple

from utils.types import Direction, Side, Corner
from utils.constants import DX, DY, TILE_SIZE, WALL_W, FIELD_HEIGHT_INNER, FIELD_WIDTH_INNER

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

