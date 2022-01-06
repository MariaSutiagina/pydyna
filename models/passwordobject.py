from typing import Sequence, List
import pygame as pg
import json

import pygame_menu as pgm
from pygame_menu.locals import ALIGN_CENTER, ALIGN_LEFT

from pygame import Surface
from models.customobject import CustomObject
from utils.characterstate import CharacterState
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH, KEYBOARD
from utils.statemanager import StateManager

class PasswordObject(CustomObject):
    def __init__(self, state):
        super().__init__(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.state = state
        self.password = 'ABCDEFGH'
        self.current_position = 7
        self.init_menu()

    def draw(self, surface:Surface):
        if self.menu.is_enabled():
            self.menu.draw(surface)

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        pass

    def mouse_handler(self, type, pos):
        pass
    
    def dispatcher(self, events):
        if self.menu.is_enabled():
            self.menu.update(events)
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if not self.password_wgt.active:
                            self.to_menu()

    def on_password_return(self, value):
        json_data = StateManager().load_state(value.upper())
        self.state.statemodel.data = CharacterState(json.loads(json_data))
        self.to_leveltitle()

    def to_leveltitle(self):
        self.menu.disable()
        self.state.statemodel.password_play()

    def to_menu(self):
        self.menu.disable()
        self.state.statemodel.password_menu()


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
        theme.widget_font_size = 72
        theme.widget_padding = 0
        effect = pgm.widgets.HighlightSelection(0, 0, 0)
        effect.color = (0xff, 0xdd, 0x7c)
        effect.background_color = (33,33,33)
        theme.widget_selection_effect = pgm.widgets.NoneSelection()


        self.menu = pgm.Menu(
            center_content=False,
            mouse_motion_selection=False,
            overflow=False,
            width=FIELD_WIDTH * 0.8,
            height=FIELD_HEIGHT * 0.7,
            theme=theme, 
            title='Enter Round Password'
        )

        frame = self.menu.add.frame_h(800, 80, margin=(1, 0))
        widget = frame.pack(self.menu.add.label(title='Enter round password:', selectable=False), align=ALIGN_LEFT, margin=(35, 0))
        font_color = (0xff, 0xf1, 0xc9)
        self.password_wgt = self.menu.add.text_input(title='', 
                                                     default=self.password, 
                                                     maxchar=8, 
                                                     font_color=font_color,
                                                     font_size=90,
                                                     valid_chars=list(KEYBOARD)+list(KEYBOARD.lower()),
                                                     cursor_selection_enable=False,
                                                     onreturn=self.on_password_return)
        self.menu.center_content()

