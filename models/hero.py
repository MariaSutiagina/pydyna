from typing import Sequence
import pygame as pg
from pygame.event import Event
from pygame.surface import Surface
from models.customcharacter import CustomCharacter
from utils.characterstate import CharacterState
from utils.constants import E_EXIT, TILE_SIZE
from utils.types import Direction, ExitAction
from utils.utils import exit_position_collided, position_in_tile, tile_position_collided, wall_position_collided
import json

class HeroRect(pg.Rect):
    def __init__(self, hero, left:float, top:float, width:float, height:float):
        self.hero = hero
        super().__init__(left, top, width, height)

    def to_json(self):
        return {'left': self.left, 'top': self.top, 'width': self.width, 'height': self.height}

class Hero(CustomCharacter):
    def __init__(self, game, state:CharacterState=None, image:Surface=None):
        state.bombs_count = state.bombs_capacity
        state.rect = HeroRect(self, state.cellx, state.celly, TILE_SIZE, TILE_SIZE)
        super().__init__(game, state, image)

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        self.state.command.key = key

    def handle_keyup(self, key:int, keys_pressed:Sequence[bool]):
        if key in [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN] and \
                not keys_pressed[pg.K_LEFT] and \
                not keys_pressed[pg.K_DOWN] and \
                not keys_pressed[pg.K_UP] and \
                not keys_pressed[pg.K_RIGHT]:
            self.state.command.key = None

    def key_to_direction(self, key:int):
        direction = Direction.NONE
        if key == pg.K_LEFT:
            direction = Direction.LEFT
        elif key == pg.K_RIGHT:
            direction = Direction.RIGHT
        elif key == pg.K_UP:
            direction = Direction.UP
        elif key == pg.K_DOWN:
            direction = Direction.DOWN
        return direction

    def compute_direction(self) -> Direction:
        return self.key_to_direction(self.state.command.key)

    def update_state(self):
        if self.state.alive == True:
            speed = self.compute_speed()
            old_position = (self.state.cellx, self.state.celly)
            position = self.compute_position(speed, self.state.direction)
            new_position = position
            new_position = tile_position_collided(old_position, position, self.game.get_state().roundobject.level)
            limited_position = wall_position_collided(new_position, self.game.get_state().roundobject.level)
            if limited_position[0] != position[0] or limited_position[1] != position[1]:
                position = limited_position
            
            direction = Direction.NONE
            new_direction = self.compute_direction()
            if new_direction in position_in_tile(*position) or \
                new_direction == Direction.NONE:
                direction = new_direction
                print(f'new direction = {direction}')
            else:
                direction = self.state.old_direction
                print(f'old direction = {direction}')        
            
            if self.state.can_exit:
                if exit_position_collided(position, self.game.get_state().roundobject.level):
                    pg.event.post(Event(E_EXIT, action=ExitAction.OPEN))

            self.compute_and_update_state(position, speed, direction)
            self.state.rect = HeroRect(self, position[0], position[1], TILE_SIZE, TILE_SIZE)
        else:
            if pg.time.get_ticks() >= self.state.time_to_hide:
                pg.event.post(Event(E_EXIT, action=ExitAction.REPLAY))


            
