from typing import Sequence
import pygame as pg
from pygame import Surface
from models.customscreenobject import CustomScreenObject
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH

class LevelTitleObject(CustomScreenObject):
    def __init__(self, state):
        super().__init__(state)

    def to_roundscreen(self):
        pg.mixer.music.stop()
        self.state.statemodel.level_round(self.state.statemodel.data)

    def get_image(self) -> Surface:
        color = (0, 0, 128)
        surface = pg.Surface((self.right, self.bottom), pg.SRCALPHA)        
        surface.fill(color)

        return surface

    def draw(self, surface:Surface):
        surface.blit(self.get_image(), (self.left, self.top))

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.to_roundscreen()

    def mouse_handler(self, type, pos):
        if type == pg.MOUSEBUTTONDOWN:
            self.to_roundscreen()
