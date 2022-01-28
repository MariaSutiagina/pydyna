import pygame as pg
import random
from typing import Tuple, overload
from collections import deque
from pygame.event import Event
from pygame.rect import Rect

from pygame.surface import Surface

from models.customcharacter import CustomCharacter
from utils.types import Direction, MonsterAction
from utils.constants import DIRECTION_CHANGE_FACTOR, E_MONSTER, TILE_HEIGHT_IN_PIXEL, TILE_SIZE, TILE_WIDTH_IN_PIXEL, WALL_W
from utils.utils import cell_pos_to_pixel, position_in_tile, tile_position_collided, wall_position_collided

class CharacterRect(Rect):
    def __init__(self, character, left:float, top:float, width:float, height:float) -> None:
        self.character = character
        super().__init__(left, top, width, height)

class Character(CustomCharacter):
    def __init__(self, game, state):
        state.rect = CharacterRect(self, state.cellx, state.celly, TILE_SIZE, TILE_SIZE)
        super().__init__(game, state)
        chain_length = self.get_chain()
        self.chain = deque(maxlen=chain_length)

    def select_new_direction(self, direction):
        return random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])

    def get_capabilities(self):
        if 'capabilities' in self.state:
            return self.state.capabilities
        
        return None

    def get_direction_change_factor(self):
        caps = self.get_capabilities()
        if  caps and 'direction_change_factor' in caps:
            return caps['direction_change_factor']
        else:
            return DIRECTION_CHANGE_FACTOR

    def get_can_fly(self):
        caps = self.get_capabilities()
        if  caps and 'can_fly' in caps:
            return caps['can_fly']
        else:
            return 0

    def get_chain(self):
        caps = self.get_capabilities()
        if  caps and 'is_chain' in caps:
            return caps['is_chain']
        else:
            return 0

    def get_has_children(self):
        caps = self.get_capabilities()
        if  caps and 'has_children' in caps:
            return caps['has_children']
        else:
            return 0
    
    def compute_direction(self) -> Direction:
        save_direction = random.choice([* self.get_direction_change_factor()*[True], False],)
        direction = self.state.direction
        if not save_direction or not direction or direction == Direction.NONE:
            direction = self.select_new_direction(direction)
        return direction
    
    def compute_and_update_chain(self, old_position):
        if len(self.chain) > 0:
            c = self.chain[0]
            if abs(c.left - old_position[0]) >= 7 * TILE_SIZE // 12 or abs(c.top - old_position[1]) >= 7 * TILE_SIZE // 12:
                self.chain.appendleft(CharacterRect(self, old_position[0], old_position[1], TILE_SIZE, TILE_SIZE))
        else:
            self.chain.appendleft(CharacterRect(self, old_position[0], old_position[1], TILE_SIZE, TILE_SIZE))
 
    def compute_and_update_children(self):
        if self.get_has_children():
            if self.state.children_make_timeout:
                if pg.time.get_ticks() >= self.state.children_make_timeout:
                    pg.event.post(Event(E_MONSTER, action=MonsterAction.CREATE_EXTRA, monster=self))
                    self.state.children_make_timeout = pg.time.get_ticks() + self.get_capabilities()['pregnancy_duration'] * 1000
            else:
                self.state.children_make_timeout = pg.time.get_ticks() + self.get_capabilities()['pregnancy_duration'] * 1000

    def update_state(self):
        speed = self.compute_speed()
        old_position = (self.state.cellx, self.state.celly)
        position = self.compute_position(speed, self.state.direction)

        new_position = position
        if self.get_can_fly() == 0:
            new_position = tile_position_collided(old_position, position, self.game.get_state().roundobject.level)

        limited_position = wall_position_collided(new_position, self.game.get_state().roundobject.level)
        direction = self.state.direction
        if limited_position[0] != position[0] or limited_position[1] != position[1]:
            position = limited_position
            new_direction = self.select_new_direction(direction)
            if new_direction in position_in_tile(*position): # or new_direction == get_opposite_direction(direction):
                direction = new_direction
        else:
            new_direction = self.compute_direction()
            if new_direction in position_in_tile(*position): # or new_direction == get_opposite_direction(direction):
                direction = new_direction

        self.compute_and_update_state(position, speed, direction)
        self.compute_and_update_chain(old_position)
        self.compute_and_update_children()

    def compute_and_update_state(self, position: Tuple, speed: int, direction: Direction):
        super().compute_and_update_state(position, speed, direction)
        r = self.state.rect
        self.state.rect = CharacterRect(self, r.left, r.top, r.width, r.height)
