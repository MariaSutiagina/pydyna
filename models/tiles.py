import io
from typing import Tuple
import pygame as pg
from pygame import Surface
from models.level import Level
from utils.constants import EXIT_TILE_TYPE, TREASURE_TILE_TYPE, TREASURE_TYPES_COUNT
from utils.types import Side, Corner
from models.customobject import CustomObject
from utils.utils import (tile_pos_to_pixel, tile_size_in_cells, tile_size_in_pixel, wall_corner_tile_size_in_pixel, wall_tile_size_in_cells, 
                         wall_tile_pos_to_pixel, wall_corner_tile_pos_to_pixel, 
                         wall_corner_tile_size_in_cells, wall_tile_size_in_pixel)

class CustomTile(CustomObject):
    def __init__(self, level:Level, x:int, y:int):
        self.fx = x
        self.fy = y
        self.level = level

        tile_pos = self.get_tile_pos(x, y)
        tile_size = self.get_tile_size()

        super().__init__(*tile_pos, *tile_size)

    def get_tile_pos(self, x:int, y:int) -> Tuple:
        return (0, 0)

    def get_tile_size(self) -> Tuple:
        return (0, 0)

    def select_resource(self):
        pass

    def draw(self, surface:Surface):        
        sfc = self.create_surface(self.select_resource())
        surface.blit(sfc, (self.left, self.top))

class Tile(CustomTile):
    def __init__(self, level:Level, x:int, y:int):
        super().__init__(level, x, y)

    def get_tile_pos(self, x:int, y:int) -> Tuple:
        return tile_pos_to_pixel(x, y)

    def get_tile_size(self) -> Tuple:
        return tile_size_in_cells()
    
    def create_surface(self, resource) -> Surface:
        ts = tile_size_in_pixel()
        
        if resource:
            # достаем текущую картинку из ресурсов
            # и загружаем ее как поверхность pygame
            surface = pg.transform.scale(resource, ts)
            # surface.set_colorkey((0,0,0))
            # surface.set_alpha(10)
        else:    
            color = (128, 128, 128)
            surface = pg.Surface(ts, pg.SRCALPHA)        
            surface.fill(color)

        return surface

    def select_resource(self):
        cx = (self.fx, self.fy)
        if cx in self.level.bricks:
            resource = self.level.bricks[cx][1]
        elif cx in self.level.solid:
            resource = self.level.solid[cx][1]
        elif cx == self.level.exit[0] and self.level.floor[cx][0] == EXIT_TILE_TYPE:
            resource = self.level.exit_resource
        elif self.level.treasure and cx == self.level.treasure[0] and self.level.floor[cx][0] >= TREASURE_TILE_TYPE and self.level.floor[cx][0] < TREASURE_TILE_TYPE + TREASURE_TYPES_COUNT:
            resource = self.level.treasure[1][1]
        else:
            resource = self.level.floor[cx][1]
        
        return resource


class WallTile(CustomTile):
    def __init__(self, level:Level, n:int, side:Side):
        self.side = side
        if side in (Side.LEFT, Side.RIGHT):
            super().__init__(level, 0, n)
        elif side in (Side.UP, Side.DOWN):
            super().__init__(level, n, 0)
        else:
            super().__init__(level, 0, 0)

    def get_tile_pos(self, x:int, y:int) -> Tuple:
        return wall_tile_pos_to_pixel(x, y, self.side)

    def get_tile_size(self):
        return wall_tile_size_in_cells(self.side)

    def create_surface(self, resource) -> Surface:
        ts = wall_tile_size_in_pixel(self.side)
        
        if resource:
            # достаем текущую картинку из ресурсов
            # и загружаем ее как поверхность pygame
            surface = pg.transform.scale(resource, ts)
            # surface.set_colorkey((0,0,0))
            # surface.set_alpha(10)
        else:    
            color = (128, 128, 128)
            surface = pg.Surface(ts, pg.SRCALPHA)        
            surface.fill(color)

        return surface

    def select_resource(self):
        if self.side in (Side.LEFT, Side.RIGHT):
            resource = self.level.wall_vert[self.fy]
        elif self.side in (Side.UP, Side.DOWN):
            resource = self.level.wall_horz[self.fx]
        else:
            resource = None
        
        return resource


class WallCornerTile(CustomTile):        
    def __init__(self, level:Level, corner:Corner):
        self.corner = corner
        if corner == Corner.LEFT_UPPER:
            super().__init__(level, 0, 0)
        elif corner == Corner.LEFT_BOTTOM:
            super().__init__(level, 0, 0)
        elif corner == Corner.RIGHT_UPPER:
            super().__init__(level, 0, 0)
        elif corner == Corner.RIGHT_BOTTOM:
            super().__init__(level, 0, 0)
        else:
            super().__init__(level, 0, 0)

    def get_tile_pos(self, x:int, y:int) -> Tuple:
        return wall_corner_tile_pos_to_pixel(self.corner)

    def get_tile_size(self) -> Tuple:
        return wall_corner_tile_size_in_cells()
    
    def create_surface(self, resource) -> Surface:
        ts = wall_corner_tile_size_in_pixel()
        
        if resource:
            # достаем текущую картинку из ресурсов
            # и загружаем ее как поверхность pygame
            surface = pg.transform.scale(resource, ts)
            # surface.set_colorkey((0,0,0))
            # surface.set_alpha(10)
        else:    
            color = (128, 128, 128)
            surface = pg.Surface(ts, pg.SRCALPHA)        
            surface.fill(color)

        return surface

    def select_resource(self):
        if self.corner == Corner.LEFT_UPPER:
            resource = self.level.corner_lt
        elif self.corner == Corner.RIGHT_UPPER:
            resource = self.level.corner_rt
        elif self.corner == Corner.LEFT_BOTTOM:
            resource = self.level.corner_lb
        elif self.corner == Corner.RIGHT_BOTTOM:
            resource = self.level.corner_rb
        else:
            resource = None
        
        return resource
