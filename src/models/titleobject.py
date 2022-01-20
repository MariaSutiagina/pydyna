from typing import Sequence
import pygame as pg

from models.customscreenobject import CustomScreenObject
from utils.constants import TITLESCREEN_TIMEOUT

# реализует функциональность игровой заставки
# наследуется от CustomScreenObject
class TitleObject(CustomScreenObject):
    def __init__(self, state):
        super().__init__(state)
        # инициализация таймаута заставки
        self.title_timeout = pg.time.get_ticks() + TITLESCREEN_TIMEOUT

    #  генерируем переход в меню игры
    def to_menu(self):
        pg.mixer.music.stop()
        self.state.statemodel.title_menu()

    # по таймауту - переходим к меню игры
    def update_state(self):
        # вызов метода обновления состояния предка - 
        # там вся магия отображения/смены фоновой заставки и старта/смены музыкальной темы
        super().update_state()

        if pg.time.get_ticks() > self.title_timeout:
            self.to_menu()            

    # при нажатии на пробел во время заставки - переход к меню
    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.to_menu()

    # при клике во время заставки - переход к меню
    def mouse_handler(self, type, pos):
        if type == pg.MOUSEBUTTONDOWN:
            self.to_menu()

