import pygame as pg
from typing import Tuple

from pygame.surface import Surface
from models.level import Level
from models.tiles import WallCornerTile, WallTile
from models.customobject import CustomObject
from utils.types import Side, Corner
from utils.constants import TILE_SIZE, WALL_W, FIELD_TILES_W, FIELD_TILES_H, CELL_W, CELL_H
from utils.utils import wall_tile_size_in_cells, wall_corner_tile_size_in_cells

class WallSide(CustomObject):
    def __init__(self, level:Level, side:Side=Side.NONE):
        self.side = side
        self.level = level
        self.init_geometry()
        super().__init__(self.x, self.y, self.w, self.h)

    def init_geometry(self):
        if self.side == Side.LEFT:
            self.x = 0
            self.y = WALL_W * CELL_H
            self.w = WALL_W * CELL_W
            self.h = FIELD_TILES_H * CELL_H
            self.tiles = FIELD_TILES_H

        elif self.side == Side.RIGHT:
            self.x = CELL_W * WALL_W + CELL_W * TILE_SIZE * FIELD_TILES_W 
            self.y = WALL_W * CELL_H
            self.w = WALL_W * CELL_W
            self.h = FIELD_TILES_H * CELL_H
            self.tiles = FIELD_TILES_H

        elif self.side == Side.UP:
            self.x = WALL_W * CELL_W
            self.y = 0
            self.w = FIELD_TILES_W * CELL_W
            self.h = WALL_W * CELL_H
            self.tiles = FIELD_TILES_W
            
        elif self.side == Side.DOWN:
            self.x = WALL_W * CELL_W
            self.y = CELL_H * WALL_W + CELL_H * TILE_SIZE * FIELD_TILES_H 
            self.w = FIELD_TILES_W * CELL_W
            self.h = WALL_W * CELL_H
            self.tiles = FIELD_TILES_W

    def draw(self, surface:Surface):
        for t in range(self.tiles):
            tile = WallTile(self.level, t, self.side)
            tile.draw(surface)

class WallCorners(CustomObject):
    def __init__(self, level:Level):
        self.level = level
        super().__init__(0, 0, 0, 0)

    def draw(self, surface:Surface):
        WallCornerTile(self.level, Corner.LEFT_UPPER).draw(surface)
        WallCornerTile(self.level, Corner.LEFT_BOTTOM).draw(surface)
        WallCornerTile(self.level, Corner.RIGHT_UPPER).draw(surface)
        WallCornerTile(self.level, Corner.RIGHT_BOTTOM).draw(surface)

class Wall(CustomObject):
    def __init__(self, level:Level):
        self.walls = [
            WallSide(level, Side.LEFT),
            WallSide(level, Side.RIGHT),
            WallSide(level, Side.UP),
            WallSide(level, Side.DOWN),
            WallCorners(level),
        ]

        super().__init__(0,0,0,0)

    def get_sort_key(self):
        return 10

    def draw(self, surface:Surface):
        for side in self.walls:
            side.draw(surface)
    

