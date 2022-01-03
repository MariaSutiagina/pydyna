import random
from typing import Sequence
import pygame as pg
from pygame import Rect, Surface
from models.bomb import Bomb
from models.customobject import CustomObject
from models.hero import Hero
from models.level import Level
from models.wall import Wall
from models.field import Field
from models.monsters import Monsters
from utils.characterstate import CharacterState

import utils.constants as cfg
from utils.types import Direction
from utils.utils import collision_rect


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

    def get_bomb_image(self):
        width = cfg.TILE_WIDTH_IN_PIXEL
        height = cfg.TILE_HEIGHT_IN_PIXEL
        surface = pg.Surface((width, height), pg.SRCALPHA, 32)        
        surface = surface.convert_alpha()
        pg.draw.circle(surface, (0x1d, 0x1c, 0xd6), (width // 2, height // 2), width //2, width=0)
        
        return surface

    def create_characters(self):
        self.objects.append(self.level.monsters)

    def create_hero(self):
        free_floor = set(self.level.floor.items()) - set(self.level.monster_bricks)
        hero_pos = random.choice(list(free_floor))
        state = {
               'cellx': cfg.TILE_SIZE * hero_pos[0][0],
               'celly': cfg.TILE_SIZE * hero_pos[0][1],
               'alive': True,
               'lives': 3,
               'is_monster': False,
               'is_hero': True,
               'is_bomb': False,
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
        self.hero = character


    def set_bomb(self):
        hr = self.hero.state.rect
        rect = pg.Rect((hr.left // cfg.TILE_SIZE) * cfg.TILE_SIZE, (hr.top // cfg.TILE_SIZE) * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE)
        state = {
               'cellx': rect.left,
               'celly': rect.top,
               'lives': 3,
               'is_monster': False,
               'is_hero': False,
               'is_bomb': True,
               'explosion_timeout': pg.time.get_ticks() + cfg.EXPLOSION_TIMEOUT,
               'explosion_size': 1,
               'explosion': False,
               'speed': 0,
               'direction': Direction.NONE,
               'old_direction': Direction.NONE
               }

        bomb = Bomb(self.game, CharacterState(state), self.get_bomb_image())
        self.level.bombs.append(bomb)
        self.objects.append(bomb)

    def draw(self, surface:Surface):
        if not self.paused:
            for o in self.objects:
                o.draw(surface)

    def check_collision(self, r1:Rect, r2:Rect):
        rect = collision_rect(r1, r2)
        if rect:
            return cfg.TILE_SIZE * cfg.TILE_SIZE / rect.width * rect.height >= 10
        else:
            return False

    def process_collisions(self):
        hero_rect = self.hero.state.rect
        monster_rects = self.level.monsters.get_rects()
        if monster_rects:
            collisions = hero_rect.collidelist(monster_rects)
            if isinstance(collisions,list):
                for c in collisions:
                    if self.check_collision(hero_rect, monster_rects[c]):
                        self.hero.state.alive = False
                        self.hero.state.time_to_hide = pg.time.get_ticks() + cfg.FADE_TIMEOUT
                        break
            else:
                if collisions >= 0 and self.check_collision(hero_rect, monster_rects[collisions]):
                    self.hero.state.alive = False
                    if not self.hero.state.time_to_hide:
                        self.hero.state.time_to_hide = pg.time.get_ticks() + cfg.FADE_TIMEOUT


    def update_state(self):
        if not self.paused:
            for o in self.objects:
                o.update_state()

            self.process_collisions()

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        if key == pg.K_ESCAPE:
            self.state.statemodel.play_menu()
        elif key == pg.K_p:
            self.paused = not self.paused
        elif key == pg.K_SPACE:
            self.set_bomb()

