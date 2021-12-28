from typing import Tuple
import random

from models.customcharacter import CustomCharacter
from utils.types import Direction
from utils.constants import DIRECTION_CHANGE_FACTOR
from utils.utils import get_opposite_direction

class Character(CustomCharacter):

    def select_new_direction(self, direction):
        return random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])

    def compute_direction(self) -> Direction:
        save_direction = random.choice([*DIRECTION_CHANGE_FACTOR*[True], False])
        direction = self.state.direction
        if not save_direction or not direction or direction == Direction.NONE:
            direction = self.select_new_direction(direction)
        return direction

    def update_state(self):
        speed = self.compute_speed()
        old_position = (self.state.cellx, self.state.celly)
        position = self.compute_position(speed, self.state.direction)
        limited_position = self.game.field.get_limited_position(old_position, position, self.state)
        direction = self.state.direction
        if limited_position[0] != position[0] or limited_position[1] != position[1]:
            position = limited_position
            new_direction = self.select_new_direction(direction)
            if new_direction in self.position_in_tile(*position): # or new_direction == get_opposite_direction(direction):
                direction = new_direction
        else:
            new_direction = self.compute_direction()
            if new_direction in self.position_in_tile(*position): # or new_direction == get_opposite_direction(direction):
                direction = new_direction

        self.compute_and_update_state(position, speed, direction)


        return super().update_state()
