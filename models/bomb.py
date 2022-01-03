from typing import Sequence
import pygame as pg
from pygame.surface import Surface
from models.customcharacter import CustomCharacter
from utils.constants import CELL_H, CELL_W, EXPLOSION_DURATION, FADE_TIMEOUT, TILE_SIZE, WALL_W
from utils.types import Direction
from utils.utils import cell_pos_to_pixel, position_in_tile, position_collided

class Bomb(CustomCharacter):
    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.state.command.key = key

    def handle_keyup(self, key:int, keys_pressed:Sequence[bool]):
        if key in [pg.K_RETURN]:
            self.state.command.key = None

    def draw(self, surface:Surface):
        # if self.state.explosion:
        #     if self.state.time_to_hide:
        #         share = (self.state.time_to_hide - pg.time.get_ticks()) / FADE_TIMEOUT
        #         self.image.set_alpha(int(255 * share))
        if not self.state.explosion:
            time_text = f'{(self.state.explosion_timeout - pg.time.get_ticks()) / 1000 :2.1f}'
        else:
            time_text = ''

        text_surface = self.font.render(time_text, True, (255, 255, 255))
        ts = (text_surface.get_width() // CELL_W, text_surface.get_height() // CELL_H)
        text_surface.convert_alpha()
        pos = cell_pos_to_pixel(WALL_W + self.state.cellx, WALL_W + self.state.celly)
        pos_text = cell_pos_to_pixel(WALL_W + self.state.cellx + TILE_SIZE // 2 - ts[0] // 2, 
                                     WALL_W + self.state.celly + TILE_SIZE // 2 - ts[1] // 2)
        surface.blit(self.image, pos)
        surface.blit(text_surface, pos_text)

    def make_explosion_rects(self):
        pass

    def update_state(self):
        if self.state.explosion == True:
            pass            
        else:
            if pg.time.get_ticks() >= self.state.explosion_timeout:
                self.state.explosion = True
                self.state.explosion_end_timeout = pg.time.get_ticks() + EXPLOSION_DURATION
                self.make_explosion_rects()


            
