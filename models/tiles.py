from typing import Tuple
import pygame as pg
from pygame import Surface
from utils.types import Side, Corner
from models.customobject import CustomObject
from utils.utils import (tile_pos_to_pixel, tile_size_in_cells, wall_tile_size_in_cells, 
                         wall_tile_pos_to_pixel, wall_corner_tile_pos_to_pixel, 
                         wall_corner_tile_size_in_cells)

class CustomTile(CustomObject):
    def __init__(self, x:int, y:int, image:Surface=None):
        self.fx = x
        self.fy = y
        self.image = image

        tile_pos = self.get_tile_pos(x, y)
        tile_size = self.get_tile_size()

        super().__init__(*tile_pos, *tile_size)

    def get_tile_pos(self, x:int, y:int) -> Tuple:
        return (0, 0)

    def get_tile_size(self) -> Tuple:
        return (0, 0)

    def draw(self, surface:Surface):
        surface.blit(self.image, (self.left, self.top))

class Tile(CustomTile):
    def get_tile_pos(self, x:int, y:int) -> Tuple:
        return tile_pos_to_pixel(x, y)

    def get_tile_size(self) -> Tuple:
        return tile_size_in_cells()
    

class WallTile(CustomTile):
    def __init__(self, n:int, side:Side, image:Surface=None):
        self.side = side
        if side in (Side.LEFT, Side.RIGHT):
            super().__init__(0, n, image)
        elif side in (Side.UP, Side.DOWN):
            super().__init__(n, 0, image)
        else:
            super().__init__(0, 0, None)

    def get_tile_pos(self, x:int, y:int) -> Tuple:
        return wall_tile_pos_to_pixel(x, y, self.side)

    def get_tile_size(self):
        return wall_tile_size_in_cells(self.side)
    
    def draw(self, surface:Surface):
        surface.blit(self.image, (self.left, self.top))

class WallCornerTile(CustomTile):        
    def __init__(self, corner:Corner, image:Surface=None):
        self.corner = corner
        if corner == Corner.LEFT_UPPER:
            super().__init__(0, 0, image)
        elif corner == Corner.LEFT_BOTTOM:
            super().__init__(0, 0, image)
        elif corner == Corner.RIGHT_UPPER:
            super().__init__(0, 0, image)
        elif corner == Corner.RIGHT_BOTTOM:
            super().__init__(0, 0, image)
        else:
            super().__init__(0, 0, None)

    def get_tile_pos(self, x:int, y:int) -> Tuple:
        return wall_corner_tile_pos_to_pixel(self.corner)

    def get_tile_size(self) -> Tuple:
        return wall_corner_tile_size_in_cells()
    
