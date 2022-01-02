import pygame as pg
from pygame.surface import Surface
from models.character import Character
from utils.characterstate import CharacterState
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH, TILE_HEIGHT_IN_PIXEL, TILE_WIDTH_IN_PIXEL
from utils.utils import tile_pos_to_cell


class Monster(Character):
    def __init__(self, game, state:CharacterState):
        super().__init__(game, state, self.get_image(state))

    def get_image(self, state):
        if state.monstertype == 1:
            color = (0xf4, 0x00, 0xa1)
        elif state.monstertype == 2:
            color = (0xff, 0x75, 0x18)
        elif state.monstertype == 3:
            color = (0xcc, 0x77, 0x22)
        elif state.monstertype == 4:
            color = (0x99, 0x11, 0x99)
        else:
            color = (0x00, 0x00, 0x00)

        width = TILE_WIDTH_IN_PIXEL
        height = TILE_HEIGHT_IN_PIXEL
        surface = pg.Surface((width, height), pg.SRCALPHA, 32)        
        surface = surface.convert_alpha()
        pg.draw.circle(surface, color, (width // 2, height // 2), width //2, width=5)
        
        return surface
