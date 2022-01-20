from utils.environment import Environment
import pygame as pg

# поставили pygame-menu - чтоб нарисовать меню и прочие элементы управления
import pygame_menu as pgm

from pygame_menu.themes import THEME_ORANGE as menu_theme

from pygame import Surface
from models.customscreenobject import CustomScreenObject
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH, GAME_FONT_PATH

# экран меню тоже наследуем от CustomScreenObject
class MenuObject(CustomScreenObject):
    def __init__(self, state):
        super().__init__(state)
        self.init_menu()

    # метод отрисовки экрана, который вызывается на каждом тике часов
    def draw(self, surface:Surface):
        # меню само себя отрисует (здесь отрисовка и обработка событий меню)
        self.menu.mainloop(surface)               
    
    # переход к игре - к заставке уровня
    def to_leveltitle(self):
        pg.mixer.music.stop()
        self.menu.disable()
        self.state.statemodel.menu_level()

    # переход к экрану ввода пароля
    def to_password(self):
        pg.mixer.music.stop()
        self.menu.disable()
        self.state.statemodel.menu_password()

    # выход из игры
    def to_exit(self):
        pg.mixer.music.stop()
        self.menu.disable()
        self.state.statemodel.menu_exit()

    # создание объекта меню
    def init_menu(self):
        # настраиваем тему исходя из стандартной темы ORANGE
        menu_theme.set_background_color_opacity(0.1)
        menu_theme.widget_font = Environment().get_path(GAME_FONT_PATH)
        menu_theme.widget_font_size = 60
        menu_theme.widget_selection_effect = pgm.widgets.HighlightSelection(1, 0, 0).set_color((0xff, 0xdd, 0x7c))
        menu_theme.widget_font_color = (0xff, 0xcc, 0x16)

        self.menu = pgm.Menu(
            width=FIELD_WIDTH * 0.8,
            height=FIELD_HEIGHT * 0.7,
            theme=menu_theme, 
            title='Dyna Blaster'
        )
        # три пунка меню - играть, войти с паролем, выход из игры
        self.menu.add.button('Go Play',  self.to_leveltitle)            
        self.menu.add.button('Password',  self.to_password)                            
        self.menu.add.button('Quit',  self.to_exit)     

