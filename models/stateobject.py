import pygame


import pygame as pg
from pygame import Surface
from models.customobject import CustomObject
from utils.constants import CELL_H, GAME_FONT_PATH, WALL_W


class StateObject(CustomObject):
    def __init__(self, game, state):
        self.font = pg.font.Font(GAME_FONT_PATH, 30)
        self.state = state
        self.state_text = ''
        self.game = game
        self.init_geometry()
        super().__init__(self.x, self.y, self.w, self.h)

    def init_geometry(self):
            self.x = 0
            self.y = 0
            self.w = 400
            self.h = CELL_H * WALL_W

    def draw(self, surface:Surface):
        text_surface = self.font.render(self.state_text, True, (0x2c, 0x75, 0xff))
        ts = (text_surface.get_width(), text_surface.get_height())
        pos_text = (10, self.h // 2 - ts[1] // 2)
        text_surface.convert_alpha()
        surface.blit(text_surface, pos_text)

    def update_state(self):
        rm = ['','R']
        fps = round(self.game.clock.get_fps())
        text = []
        text.append(f'FPS:{fps}')
        text.append(f'R:{self.state.level}/{self.state.round}')
        text.append(f'S:{self.state.speed}')
        text.append(f'L:{self.state.retries}/{self.state.lifes}')
        text.append(f'B{rm[int(self.state.can_remote)]}:{self.state.bombs_capacity}/{self.state.bombs_count}/{self.state.bombs_strength}')
        if self.state.can_fly:
            text.append('F')
        if self.state.is_killer:
            text.append('K')
        if self.state.can_exit or self.state.can_use_exit:
            text.append('X')
        
        time = (self.state.round_timeout - pg.time.get_ticks()) // 1000
        time_mins = time // 60
        time_secs = time % 60
        self.state_text = f'TIME: {time_mins:02}:{time_secs:02}  SCORE: {self.state.score:08}    ' + ', '.join(text)
    
