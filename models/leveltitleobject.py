from typing import Sequence
import pygame as pg
from pygame import Surface
from models.customobject import CustomObject
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH

class LevelTitleObject(CustomObject):
    def __init__(self, state):
        super().__init__(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.state = state

    def get_image(self) -> Surface:
        color = (0, 0, 128)
        surface = pg.Surface((self.right, self.bottom), pg.SRCALPHA)        
        surface.fill(color)

        return surface

    def draw(self, surface:Surface):
        surface.blit(self.get_image(), (self.left, self.top))

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.state.statemodel.level_round()

    def mouse_handler(self, type, pos):
        if type == pg.MOUSEBUTTONDOWN:
            self.state.statemodel.level_round()