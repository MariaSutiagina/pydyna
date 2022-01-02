import random
from typing import Sequence
import pygame as pg
from pygame import Surface
from models.customobject import CustomObject
from models.hero import Hero
from models.level import Level
from models.wall import Wall
from models.field import Field
from models.monsters import Monsters
from utils.characterstate import CharacterState

import utils.constants as cfg
from utils.types import Direction


class RoundObject(CustomObject):
    def __init__(self, game, state):
        super().__init__(0, 0, cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT)
        self.state = state
        self.game = game
        self.paused = False
        self.create_objects()

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        pass

    def mouse_handler(self, type, pos):
        pass

    def create_objects(self):
        self.objects = []
        self.create_level()
        self.create_wall()
        self.create_field()
        self.create_characters()
        self.create_hero()

    def create_level(self):
        self.level = Level(self.game, 1, 1)

    def create_wall(self):
        self.wall = Wall(self.level)
        self.objects.append(self.wall)

    def create_field(self):
        self.field = Field(self.level)
        self.objects.append(self.field)

    def get_hero_image(self):
        color = (0, 255, 255)
        width = cfg.TILE_WIDTH_IN_PIXEL
        height = cfg.TILE_HEIGHT_IN_PIXEL
        surface = pg.Surface((width, height), pg.SRCALPHA, 32)        
        surface = surface.convert_alpha()
        pg.draw.circle(surface, (0, 0, 255), (width // 2, height // 2), width //2, width=5)
        
        return surface

    def create_characters(self):
        self.objects.append(self.game.level.monsters)

    def create_hero(self):
        free_floor = set(self.game.level.floor.items()) - set(self.game.level.monster_bricks)
        hero_pos = random.choice(list(free_floor))
        state = {
               'cellx': cfg.TILE_SIZE * hero_pos[0][0],
               'celly': cfg.TILE_SIZE * hero_pos[0][1],
               'speed': 1,
               'direction': Direction.NONE,
               'old_direction': Direction.NONE
               }

        character = Hero(self.game, CharacterState(state), self.get_hero_image())
        
        self.state.keydown_handlers[pg.K_DOWN].append(character.handle_keydown)
        self.state.keydown_handlers[pg.K_RIGHT].append(character.handle_keydown)
        self.state.keydown_handlers[pg.K_LEFT].append(character.handle_keydown)
        self.state.keydown_handlers[pg.K_UP].append(character.handle_keydown)

        self.state.keyup_handlers[pg.K_DOWN].append(character.handle_keyup)
        self.state.keyup_handlers[pg.K_RIGHT].append(character.handle_keyup)
        self.state.keyup_handlers[pg.K_LEFT].append(character.handle_keyup)
        self.state.keyup_handlers[pg.K_UP].append(character.handle_keyup)

        self.objects.append(character)


    def draw(self, surface:Surface):
        if not self.paused:
            for o in self.objects:
                o.draw(surface)

    def update_state(self):
        if not self.paused:
            for o in self.objects:
                o.update_state()

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        if key == pg.K_ESCAPE:
            self.state.statemodel.play_menu()
        elif key == pg.K_p:
            self.paused = not self.paused

