from typing import Sequence, List, Tuple
import pygame as pg
from pygame.event import Event
from pygame.rect import Rect
from pygame.surface import Surface
from models.customcharacter import CustomCharacter
from utils.constants import CELL_H, CELL_W, E_BOMB, EXPLOSION_DURATION, TILE_HEIGHT_IN_PIXEL, TILE_SIZE, TILE_WIDTH_IN_PIXEL, WALL_W
from utils.types import BombAction, Direction
from utils.utils import cell_pos_to_pixel

class BombRect(Rect):
    def __init__(self, bomb, left:float, top:float, width:float, height:float):
        self.bomb = bomb
        super().__init__(left, top, width, height)

    # def __init__(self, bomb, left_top:List[float], width_height:List[float]):
    #     self.bomb = bomb
    #     super().__init__(left_top, width_height)

    # def __init__(self, bomb, rect:Rect):
    #     self.bomb = bomb
    #     super().__init__(rect)


class Bomb(CustomCharacter):
    def __init__(self, game, state, image):
        state.rect.bomb = self
        super().__init__(game, state, image)

    def get_level(self):
        return self.game.get_state().roundobject.level
    
    def get_round(self):
        return getattr(self.game.get_state(), 'roundobject', None)


    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.state.command.key = key

    def handle_keyup(self, key:int, keys_pressed:Sequence[bool]):
        if key in [pg.K_RETURN]:
            self.state.command.key = None
    
    def get_vert_image(self):
        width = TILE_WIDTH_IN_PIXEL
        height = TILE_HEIGHT_IN_PIXEL
        sfc = pg.Surface((width, height), pg.SRCALPHA, 32)        
        sfc = sfc.convert_alpha()
        pg.draw.line(sfc, (0x1d, 0x1c, 0xd6), (width // 2, 0), (width //2, height), width=21)
        return sfc

    def get_horz_image(self):
        width = TILE_WIDTH_IN_PIXEL
        height = TILE_HEIGHT_IN_PIXEL
        sfc = pg.Surface((width, height), pg.SRCALPHA, 32)        
        sfc = sfc.convert_alpha()
        pg.draw.line(sfc, (0x1d, 0x1c, 0xd6), (0, height // 2), (width, height // 2), width=21)
        return sfc


    def draw_vert_rect(self, surface, rect):
        pos = cell_pos_to_pixel(WALL_W + rect.left, WALL_W + rect.top)
        surface.blit(self.get_vert_image(), pos)

    def draw_horz_rect(self, surface, rect):
        pos = cell_pos_to_pixel(WALL_W + rect.left, WALL_W + rect.top)
        surface.blit(self.get_horz_image(), pos)

    def draw_rects(self, surface):
        br = self.state.rect
        for r in self.state.rects:
            if r.top < br.top or r.top >= br.top + TILE_SIZE:
                self.draw_vert_rect(surface, r)
            else:
                self.draw_horz_rect(surface, r)


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
        self.draw_rects(surface)

    def make_explosion_rects(self, cells):
        rects = []
        for c in cells:
            rect = BombRect(self, c[0] * TILE_SIZE, c[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            rects.append(rect)
        self.state.rects = rects

    def update_state(self):
        if self.state.explosion:
            if pg.time.get_ticks() >= self.state.explosion_end_timeout:
                pg.event.post(Event(E_BOMB, action=BombAction.END_EXPLOSION, bomb=self))
        else:
            if (not self.state.is_remote) and pg.time.get_ticks() >= self.state.explosion_timeout:
                pg.event.post(Event(E_BOMB, action=BombAction.START_EXPLOSION, bomb=self))


            
