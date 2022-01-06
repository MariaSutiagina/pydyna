from typing import Sequence
import pygame as pg
import json
import pygame_menu as pgm
from pygame_menu.themes import THEME_ORANGE as menu_theme
from pygame_menu.widgets.core import widget
from pygame_menu.locals import ALIGN_CENTER


from pygame import Surface
from models.customobject import CustomObject
from utils.characterstate import CharacterStateEncoder
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH
from utils.statemanager import StateManager

class GameOverMenuObject(CustomObject):
    def __init__(self, state):
        super().__init__(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.state = state
        state_dict = state.statemodel.data
        self.password = StateManager().save_state_enc(json.dumps(state_dict, cls=CharacterStateEncoder))
        self.init_menu()

    def draw(self, surface:Surface):
        self.menu.mainloop(surface)               

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.state.statemodel.menu_level()

    def mouse_handler(self, type, pos):
        if type == pg.MOUSEBUTTONDOWN:
            self.state.statemodel.menu_level()
    
    def to_roundtitle(self):
        self.menu.disable()
        self.state.statemodel.gameover_continue(data=self.state.statemodel.data)

    def to_menu(self):
        self.menu.disable()
        self.state.statemodel.gameover_end(data=None)

    def init_menu(self):
        theme = pgm.Theme()

        theme.set_background_color_opacity(0)
        theme.background_color = (43, 43, 43)
        theme.title = False
        theme.cursor_selection_color = (255, 0, 0, 64)
        theme.widget_alignment = ALIGN_CENTER
        theme.widget_background_color = None
        theme.widget_font = './resources/fonts/Elfboyclassic.ttf'
        theme.widget_font_color = (0xff, 0xcc, 0x16)
        theme.widget_font_size = 60
        theme.widget_padding = 0
        effect = pgm.widgets.HighlightSelection(0, 0, 0)
        effect.color = (0xff, 0xdd, 0x7c)
        effect.background_color = (33,33,33)
        theme.widget_selection_effect = effect

        self.menu = pgm.Menu(
            width=FIELD_WIDTH * 0.8,
            height=FIELD_HEIGHT * 0.7,
            theme=theme, 
            title='Dyna Blaster'
        )
        retries = self.state.statemodel.data.retries
        if retries > 0:
            self.menu.add.button(f'Continue Play ({retries})',  self.to_roundtitle)

        self.menu.add.button('End Game',  self.to_menu)  

        if retries > 0:
            frame = self.menu.add.frame_h(800, 180, margin=(0, 100))
            widget = frame.pack(self.menu.add.label(title='Password: '+ self.password, font_size=80, selectable=False, padding=(100,0,0,0)), align=ALIGN_CENTER, margin=(0, 0))
