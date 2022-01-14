from typing import Sequence
import pygame as pg
from pygame.event import Event
from pygame.surface import Surface
from models.customcharacter import CustomCharacter
from models.treasurefactory import TreasureFactory
from utils.characterstate import CharacterState
from utils.constants import E_EXIT, E_TREASURE, MAX_BOMB_STRENGTH, MAX_SPEED, MOVEMENT_TIMEOUT, TILE_SIZE
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

    def get_resource_ids(self):
        return ['hero-front-up', 'hero-front-dn', 
                'hero-side-up-lt', 'hero-side-dn-lt', 
                'hero-kick', 'hero-dead',
                'hero-side-dn-rt', 'hero-side-up-rt']

    def add_resource(self, id, resource):
        parts = id.split('-')
        if parts[1] == 'front':
            self.state.resources.up[parts[2]] = resource
            self.state.resources.down[parts[2]] = resource
        elif parts[1] == 'side':
            if parts[3] == 'lt':
                self.state.resources.left[parts[2]] = resource
            elif parts[3] == 'rt':
                self.state.resources.right[parts[2]] = resource
        elif parts[1] == 'kick':
            self.state.resources.kick = resource
        elif parts[1] == 'dead':
            self.state.resources.dead = resource
        

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
            self.switch_movement_on()
        elif key == pg.K_RIGHT:
            direction = Direction.RIGHT
            self.switch_movement_on()
        elif key == pg.K_UP:
            direction = Direction.UP
            self.switch_movement_on()
        elif key == pg.K_DOWN:
            direction = Direction.DOWN
            self.switch_movement_on()
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
            elif 'can-exit' in treasure_state:
                self.state.can_use_exit = True

    def get_level(self):
        return self.game.get_state().roundobject.level

    def get_sort_key(self):
        return 100

    def switch_movement_on(self):
        self.movement_stopped = False
        self.move_timeout = pg.time.get_ticks() + MOVEMENT_TIMEOUT

    def update_state(self):
        if self.state.alive == True:
            speed = self.compute_speed()
            old_position = (self.state.cellx, self.state.celly)
            position = self.compute_position(speed, self.state.direction)
            new_position = position
            if not self.state.can_fly:
                new_position = tile_position_collided(old_position, position, self.get_level())
            limited_position = wall_position_collided(new_position, self.get_level())
            if limited_position[0] != position[0] or limited_position[1] != position[1]:
                position = limited_position
            
            direction = Direction.NONE
            new_direction = self.compute_direction()
            if new_direction != Direction.NONE:
                self.state.saved_direction = new_direction
            if new_direction in position_in_tile(*position) or \
                new_direction == Direction.NONE:
                direction = new_direction
            else:
                direction = self.state.old_direction
            
            if self.state.can_exit or self.state.can_use_exit:
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

        super().update_state()


            
