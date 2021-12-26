from typing import Tuple
import random

import pygame as pg
from pygame import Surface

from models.customobject import CustomObject
from utils.characterstate import CharacterState
from utils.utils import cell_pos_to_pixel, tile_size_in_pixel
from utils.types import Direction
from models.game import Game
from models.field import Field
from utils.constants import WALL_W, DIRECTION_CHANGE_FACTOR, TILE_SIZE

class Character(CustomObject):
    def __init__(self, game:Game, state:CharacterState=None, image:Surface=None):
        self.state = state
        self.game = game
        self.image = image

        pos = cell_pos_to_pixel(WALL_W + state.cellx, WALL_W + state.celly)
        sz = tile_size_in_pixel()
        super().__init__(*pos, *sz)

    def draw(self, surface:Surface):
        pos = cell_pos_to_pixel(WALL_W + self.state.cellx, WALL_W + self.state.celly)
        surface.blit(self.image, pos)
    
    def compute_position(self, speed:int, direction:Direction) -> Tuple:
        cellx = self.state.cellx
        celly = self.state.celly
        new_cellx = cellx
        new_celly = celly
        if direction == Direction.LEFT:
            new_cellx = cellx - speed
        elif direction == Direction.RIGHT:
            new_cellx = cellx + speed
        elif direction == Direction.UP:
            new_celly = celly - speed
        elif direction == Direction.DOWN:
            new_celly = celly + speed

        return (new_cellx, new_celly)
        

    def compute_speed(self) -> int:
        speed = self.state.speed
        if not speed:
            speed = 1
        return speed
    
    def select_new_direction(self, direction):
        return random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])

    def compute_direction(self) -> Direction:
        save_direction = random.choice([*DIRECTION_CHANGE_FACTOR*[True], False])
        direction = self.state.direction
        if not save_direction or not direction or direction == Direction.NONE:
            direction = self.select_new_direction(direction)
        return direction

            

    def compute_and_update_state(self, position:Tuple, speed:int, direction:Direction):
        old_position = (self.state.cellx, self.state.celly)

        self.state.cellx = position[0]
        self.state.celly = position[1]
        self.state.speed = speed

        if direction != self.state.old_direction:
            self.state.old_direction = self.state.direction
            self.state.direction = direction

    def position_in_tile(self, cellx:int, celly:int):
        return cellx % TILE_SIZE == 0 and celly % TILE_SIZE == 0 

    def update_state(self):
        speed = self.compute_speed()
        old_position = (self.state.cellx, self.state.celly)
        position = self.compute_position(speed, self.state.direction)
        limited_position = self.game.field.get_limited_position(old_position, position, self.state)
        direction = self.state.direction
        if limited_position[0] != position[0] or limited_position[1] != position[1]:
            position = limited_position
            if self.position_in_tile(*position):
                direction = self.select_new_direction(direction)
        else:
            if self.position_in_tile(*position):
                direction = self.compute_direction()

        self.compute_and_update_state(position, speed, direction)


        return super().update_state()
