from typing import Sequence
import pygame as pg
from pygame import Surface
from models.customscreenobject import CustomScreenObject
from utils.constants import GAME_FONT_PATH
from utils.environment import Environment

# реализует функциональность  финального экрана
# наследуется от CustomScreenObject
class GameWinObject(CustomScreenObject):
    def __init__(self, state):
        super().__init__(state)
        self.font = pg.font.Font(Environment().get_path(GAME_FONT_PATH), 190)

    # переход в меню
    def to_menu(self):
        pg.mixer.music.stop()
        self.state.statemodel.gamewin_menu()

    # формирует изображение заставки раунда
    def get_image(self) -> Surface:
        round_text = f'YOU WIN'
        color = (128, 0, 128)
        surface = pg.Surface((self.right, self.bottom), pg.SRCALPHA)        
        surface.fill(color)

        text_surface = self.font.render(round_text, True, (0xff, 0xcc, 0x16))
        ts = (text_surface.get_width(), text_surface.get_height())
        pos_text = (self.width // 2 - ts[0] // 2, self.height // 2 - ts[1] // 2)
        text_surface.convert_alpha()
        surface.blit(text_surface, pos_text)

        return surface

    # обработчик нажатий клавиш на клавиатуре
    # сюда попадают только нажатия на пробел (K_SPACE)
    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.to_menu()

    # обработчик событий от мыши
    def mouse_handler(self, type, pos):
        if type == pg.MOUSEBUTTONDOWN:
            self.to_menu()