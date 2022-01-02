from typing import Tuple
import pygame as pg
from pygame import Surface

from utils.utils import cell_pos_to_pixel, tile_size_in_pixel
from utils.constants import WALL_W, DIRECTION_CHANGE_FACTOR, TILE_SIZE
from utils.types import Direction
from utils.characterstate import CharacterState

from models.customobject import CustomObject
# from models.game import Game


class CustomCharacter(CustomObject):
    def __init__(self, game, state:CharacterState=None, image:Surface=None):
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
    
    def compute_direction(self) -> Direction:
        return Direction.NONE

    def compute_and_update_state(self, position:Tuple, speed:int, direction:Direction):
        self.state.cellx = position[0]
        self.state.celly = position[1]
        self.state.speed = speed

        # if direction != self.state.old_direction or direction == Direction.NONE:
        #     self.state.old_direction = self.state.direction
        if self.state.direction != Direction.NONE:
            self.state.old_direction = self.state.direction
        
        self.state.direction = direction

