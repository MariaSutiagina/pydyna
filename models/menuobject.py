from typing import Sequence
import pygame as pg

import pygame_menu as pgm
from pygame_menu.themes import THEME_ORANGE as menu_theme
from pygame_menu.widgets.core import widget


from pygame import Surface
from models.customobject import CustomObject
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH

class MenuObject(CustomObject):
    def __init__(self, state):
        super().__init__(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.state = state
        self.init_menu()

    def draw(self, surface:Surface):
        self.menu.mainloop(surface)               

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.state.statemodel.menu_level()

    def mouse_handler(self, type, pos):
        if type == pg.MOUSEBUTTONDOWN:
            self.state.statemodel.menu_level()
    
    def to_leveltitle(self):
        self.menu.disable()
        self.state.statemodel.menu_level()

    def to_password(self):
        self.menu.disable()
        self.state.statemodel.menu_password()

    def init_menu(self):
        menu_theme.set_background_color_opacity(0.1)
        menu_theme.widget_font = './resources/fonts/Elfboyclassic.ttf'
        menu_theme.widget_font_size = 60
        menu_theme.widget_selection_effect = pgm.widgets.HighlightSelection(1, 0, 0).set_color((0xff, 0xdd, 0x7c))
        menu_theme.widget_font_color = (0xff, 0xcc, 0x16)

        self.menu = pgm.Menu(
            width=FIELD_WIDTH * 0.8,
            height=FIELD_HEIGHT * 0.7,
            theme=menu_theme, 
            title='Dyna Blaster'
        )

        self.menu.add.button('Go Play',  self.to_leveltitle)            
        self.menu.add.button('Password',  self.to_password)                            
        self.menu.add.button('Quit',  lambda: self.state.statemodel.menu_exit())     

