from typing import Tuple
import pygame as pg
from pygame import Surface
from models.customobject import CustomObject
from utils.characterstate import CharacterState
from utils.constants import WALL_W, CELL_W, CELL_H, FIELD_WIDTH_INNER, FIELD_HEIGHT_INNER, FIELD_TILES_W, FIELD_TILES_H, TILE_SIZE
from models.tiles import Tile

class Field(CustomObject):
    def __init__(self):
        self.x = WALL_W * CELL_W
        self.y = WALL_W * CELL_H
        self.w = FIELD_WIDTH_INNER
        self.h = FIELD_HEIGHT_INNER
        self.tiles_w = FIELD_TILES_W
        self.tiles_h = FIELD_TILES_H

        super().__init__(self.x, self.y, self.w, self.h)

    def get_image(self):
        color = (0, 255, 255)
        width = CELL_W * TILE_SIZE
        height = CELL_H * TILE_SIZE
        surface = pg.Surface((width, height), pg.SRCALPHA)
        surface.fill(color)
        pg.draw.rect(surface, (0, 0, 0), (0, 0, width, height), 1)
        
        return surface

    def get_limited_position(self, old_position:Tuple, new_position:Tuple, character_state:CharacterState) -> Tuple:
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




    def draw(self, surface:Surface):
        for ty in range(self.tiles_h):
            for tx in range(self.tiles_w):
                tile = Tile(tx, ty, self.get_image())
                tile.draw(surface)

