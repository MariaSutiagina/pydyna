from typing import Sequence
import pygame as pg
from pygame import Surface
from models.customscreenobject import CustomScreenObject
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH

# реализует функциональность заставки уровня
# наследуется от CustomScreenObject
class LevelTitleObject(CustomScreenObject):
    def __init__(self, state):
        super().__init__(state)

    # переход к заставке игрового раунда
    def to_roundscreen(self):
        pg.mixer.music.stop()
        self.state.statemodel.level_round(self.state.statemodel.data)

    # формирует изображение заставки уровня
    def get_image(self) -> Surface:
        color = (0, 0, 128)
        surface = pg.Surface((self.right, self.bottom), pg.SRCALPHA)        
        surface.fill(color)

        return surface

    # обработчик нажатий клавиш на клавиатуре
    # сюда попадают только нажатия на пробел (K_SPACE)
    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.to_roundscreen()

    # обработчик событий от мыши
    def mouse_handler(self, type, pos):
        if type == pg.MOUSEBUTTONDOWN:
            self.to_roundscreen()
