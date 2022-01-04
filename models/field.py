from typing import Tuple
import pygame as pg
from pygame import Surface
from models.customobject import CustomObject
from models.level import Level
from utils.characterstate import CharacterState
from utils.constants import BRICK_HARDNESS_MAX, EXIT_TILE_TYPE, WALL_W, CELL_W, CELL_H, FIELD_WIDTH_INNER, FIELD_HEIGHT_INNER, FIELD_TILES_W, FIELD_TILES_H, TILE_SIZE
from models.tiles import Tile

class Field(CustomObject):
    def __init__(self, level:Level):
        self.level = level
        self.x = WALL_W * CELL_W
        self.y = WALL_W * CELL_H
        self.w = FIELD_WIDTH_INNER
        self.h = FIELD_HEIGHT_INNER
        self.tiles_w = FIELD_TILES_W
        self.tiles_h = FIELD_TILES_H

        super().__init__(self.x, self.y, self.w, self.h)

    def get_image(self, tx, ty):
        if (tx, ty) in self.level.bricks:
            brick_type = self.level.bricks[(tx, ty)]
            if brick_type <= BRICK_HARDNESS_MAX:
                color = (0xb0 - brick_type + 1, 0xc4 - brick_type + 1 , 0xde - brick_type + 1)
            elif brick_type == EXIT_TILE_TYPE:
                color = (0x99, 0x11, 0x99)
            else:
                color = (0, 255, 255)
        elif (tx, ty) in self.level.solid:
            color = (0x88, 0x45, 0x35)
        elif (tx, ty) == self.level.exit[0] and self.level.floor[(tx, ty)] == EXIT_TILE_TYPE:
            color = (0x99, 0x11, 0x99)
        else:
            color = (0, 255, 255)
        width = CELL_W * TILE_SIZE
        height = CELL_H * TILE_SIZE
        surface = pg.Surface((width, height), pg.SRCALPHA)
        surface.fill(color)
        pg.draw.rect(surface, (0, 0, 0), (0, 0, width, height), 1)
        
        return surface

    def draw(self, surface:Surface):
        for ty in range(self.tiles_h):
            for tx in range(self.tiles_w):
                tile = Tile(self.level, tx, ty, self.get_image(tx, ty))
                tile.draw(surface)

