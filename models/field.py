from addict import Dict

from utils.resourcemanager import ResourceManager()
import pygame as pg
from pygame import Surface
from models.customobject import CustomObject
from models.level import Level
from utils.constants import BRICK_HARDNESS_MAX, EXIT_TILE_TYPE, GAME_FONT_PATH, TREASURE_TILE_TYPE, TREASURE_TYPES_COUNT, WALL_W, CELL_W, CELL_H, FIELD_WIDTH_INNER, FIELD_HEIGHT_INNER, FIELD_TILES_W, FIELD_TILES_H, TILE_SIZE
from models.tiles import Tile
from utils.utils import cell_pos_to_pixel

class Field(CustomObject):
    def __init__(self, level:Level):
        self.font = pg.font.Font(GAME_FONT_PATH, 30)
        self.level = level
        self.x = WALL_W * CELL_W
        self.y = WALL_W * CELL_H
        self.w = FIELD_WIDTH_INNER
        self.h = FIELD_HEIGHT_INNER
        self.tiles_w = FIELD_TILES_W
        self.tiles_h = FIELD_TILES_H

        super().__init__(self.x, self.y, self.w, self.h)
        self.get_resources()

    def get_resources(self):
        # level = self.level.level
        level = 1
        resources = dict()
        resources['floor'] = ResourceManager()[f'tile-road-{level:02}']
        resources['bricks'] = ResourceManager()[f'tile-brick-{level:02}']
        resources['solid'] = ResourceManager()[f'tile-solid-{level:02}']

    def get_sort_key(self):
        return 20

    def get_image(self, tx, ty):
        treasure = False
        if (tx, ty) in self.level.bricks:
            brick_type = self.level.bricks[(tx, ty)]
            if brick_type <= BRICK_HARDNESS_MAX or brick_type >= TREASURE_TILE_TYPE and brick_type < TREASURE_TILE_TYPE + TREASURE_TYPES_COUNT:
                color = (0xb0 - brick_type + 1, 0xc4 - brick_type + 1 , 0xde - brick_type + 1)
            else:
                color = (0, 255, 255)
        elif (tx, ty) in self.level.solid:
            color = (0x88, 0x45, 0x35)
        elif (tx, ty) == self.level.exit[0] and self.level.floor[(tx, ty)] == EXIT_TILE_TYPE:
            color = (0x99, 0x11, 0x99)
        elif self.level.treasure and (tx, ty) == self.level.treasure[0] and self.level.floor[(tx, ty)] >= TREASURE_TILE_TYPE and self.level.floor[(tx, ty)]<TREASURE_TILE_TYPE + TREASURE_TYPES_COUNT:
            color = (0x0, 0x0, 0x0)
            treasure = True
        else:
            color = (0, 255, 255)

        width = CELL_W * TILE_SIZE
        height = CELL_H * TILE_SIZE
        surface = pg.Surface((width, height), pg.SRCALPHA)
        surface.fill(color)
        pg.draw.rect(surface, (0, 0, 0), (0, 0, width, height), 1)

        if treasure:
            treasure_type = self.level.treasure[1]
            text_surface = self.font.render(str(treasure_type), True, (255, 255, 255))
            ts = (text_surface.get_width() // CELL_W, text_surface.get_height() // CELL_H)
            text_surface.convert_alpha()
            pos_text = cell_pos_to_pixel(TILE_SIZE // 2 - ts[0] // 2, 
                                         TILE_SIZE // 2 - ts[1] // 2)
            surface.blit(text_surface, pos_text)


        
        return surface

    def draw(self, surface:Surface):
        for ty in range(self.tiles_h):
            for tx in range(self.tiles_w):
                tile = Tile(self.level, tx, ty, self.get_image(tx, ty))
                tile.draw(surface)

