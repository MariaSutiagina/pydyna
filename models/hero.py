from typing import Sequence
import pygame as pg
from models.customcharacter import CustomCharacter
from utils.types import Direction
from utils.utils import get_opposite_direction

class Hero(CustomCharacter):
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
        speed = self.compute_speed()
        old_position = (self.state.cellx, self.state.celly)
        position = self.compute_position(speed, self.state.direction)
        limited_position = self.game.field.get_limited_position(old_position, position, self.state)
        if limited_position[0] != position[0] or limited_position[1] != position[1]:
            position = limited_position
        
        direction = Direction.NONE
        new_direction = self.compute_direction()
        if new_direction in self.position_in_tile(*position) or \
              new_direction == Direction.NONE:
            direction = new_direction
            print(f'new direction = {direction}')
        else:
            direction = self.state.old_direction
            print(f'old direction = {direction}')

        

        self.compute_and_update_state(position, speed, direction)


            
