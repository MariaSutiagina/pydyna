from typing import Sequence
import pygame as pg
from pygame.event import Event
from pygame.surface import Surface
from models.customcharacter import CustomCharacter
from models.treasurefactory import TreasureFactory
from utils.characterstate import CharacterState
from utils.constants import E_EXIT, E_TREASURE, MAX_BOMB_STRENGTH, MAX_SPEED, TILE_SIZE
from utils.types import Direction, ExitAction, TreasureAction
from utils.utils import exit_position_collided, position_in_tile, tile_position_collided, treasure_position_collided, wall_position_collided

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

    def apply_treasure(self, treasure_type):
        if treasure_type > 0:
            treasure_state = TreasureFactory()[treasure_type]
            if 'life' in treasure_state:
                self.state.lifes += treasure_state['life']
            elif 'speed' in treasure_state:
                self.state.speed = min(MAX_SPEED, self.state.speed + treasure_state['speed'])
            elif 'decspeed' in treasure_state:
                self.state.speed = max(1, self.state.speed - treasure_state['decspeed'])
            elif 'bomb' in treasure_state:
                self.state.bomb_capacity += treasure_state['bomb']
            elif 'explosion' in treasure_state:
                self.state.bombs_strength = min(MAX_BOMB_STRENGTH,  self.state.bombs_strength + treasure_state['explosion'])
            elif 'fly' in treasure_state:
                self.state.can_fly = True
                self.state.treasure_timeout =  pg.time.get_ticks() + treasure_state['timeout'] * 1000
            elif 'remote' in treasure_state:
                self.state.can_remote = True
                self.state.treasure_timeout =  pg.time.get_ticks() + treasure_state['timeout'] * 1000
            elif 'killer' in treasure_state:
                self.state.is_killer = True
                self.state.treasure_timeout =  pg.time.get_ticks() + treasure_state['timeout'] * 1000
            elif 'can_exit' in treasure_state:
                self.state.can_use_exit = True
                self.state.treasure_timeout =  pg.time.get_ticks() + treasure_state['timeout'] * 1000

    def get_level(self):
        return self.game.get_state().roundobject.level

    def update_state(self):
        if self.state.alive == True:
            speed = self.compute_speed()
            old_position = (self.state.cellx, self.state.celly)
            position = self.compute_position(speed, self.state.direction)
            new_position = position
            new_position = tile_position_collided(old_position, position, self.get_level())
            limited_position = wall_position_collided(new_position, self.get_level())
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
                if exit_position_collided(position, self.get_level()):
                    pg.event.post(Event(E_EXIT, action=ExitAction.OPEN))


            if self.get_level().treasure and treasure_position_collided(position, self.get_level()):
                pg.event.post(Event(E_TREASURE, action=TreasureAction.OPEN))

            self.compute_and_update_state(position, speed, direction)
            self.state.rect = HeroRect(self, position[0], position[1], TILE_SIZE, TILE_SIZE)

            if self.state.treasure_timeout:
                if pg.time.get_ticks() >= self.state.treasure_timeout:
                    pg.event.post(Event(E_TREASURE, action=TreasureAction.INACTIVE))
        else:
            if pg.time.get_ticks() >= self.state.time_to_hide:
                pg.event.post(Event(E_EXIT, action=ExitAction.REPLAY))


            
