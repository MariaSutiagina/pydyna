import random
import json
from typing import Sequence
import pygame as pg
from pygame import Rect, Surface
from pygame.event import Event
from models.bomb import Bomb, BombRect
from models.customobject import CustomObject
from models.hero import Hero
from models.level import Level
from models.wall import Wall
from models.field import Field
from models.monsters import Monsters
from utils.characterstate import CharacterState

import utils.constants as cfg
from utils.statemanager import StateManager
from utils.types import BombAction, Direction, ExitAction
from utils.utils import collision_rect, exit_position_collided


class RoundObject(CustomObject):
    def __init__(self, game, state):
        super().__init__(0, 0, cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT)
        self.state = state
        self.game = game
        self.paused = False
        self.create_objects()

    def mouse_handler(self, type, pos):
        pass

    def create_objects(self):
        self.objects = []
        self.create_level()
        self.create_wall()
        self.create_field()
        self.create_characters()
        self.create_hero(self.state.statemodel.data)

    def create_level(self):
        level = '01'
        round = '01'
        if self.state.statemodel.data:
            level = self.state.statemodel.data.level
            round = self.state.statemodel.data.round
        self.level = Level(self.game, int(level), int(round))

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

    def create_new_hero(self):
        state = {
               'cellx': 0,
               'celly': 0,
               'alive': True,
               'gone': False,
               'lives': 3,
               'retries': 3,
               'round': '01',
               'level': '01', 
               'is_monster': False,
               'is_hero': True,
               'is_bomb': False,
               'bombs_capacity': 3,
               'can_exit': False,
               'speed': 1,
               'direction': Direction.NONE,
               'old_direction': Direction.NONE
               }
        return CharacterState(state)


    def create_hero(self, hero_state=None):
        free_floor = set(self.level.floor.items()) - set(self.level.monster_bricks)
        hero_pos = random.choice(list(free_floor))

        if hero_state is None:
            hero_state = self.create_new_hero()

        hero_state.cellx = cfg.TILE_SIZE * hero_pos[0][0]
        hero_state.celly = cfg.TILE_SIZE * hero_pos[0][1]
        hero_state.alive = True
        hero_state.time_to_hide = None

        character = Hero(self.game, hero_state, self.get_hero_image())
        
        self.state.keydown_handlers[pg.K_DOWN].append(character.handle_keydown)
        self.state.keydown_handlers[pg.K_RIGHT].append(character.handle_keydown)
        self.state.keydown_handlers[pg.K_LEFT].append(character.handle_keydown)
        self.state.keydown_handlers[pg.K_UP].append(character.handle_keydown)

        self.state.keyup_handlers[pg.K_DOWN].append(character.handle_keyup)
        self.state.keyup_handlers[pg.K_RIGHT].append(character.handle_keyup)
        self.state.keyup_handlers[pg.K_LEFT].append(character.handle_keyup)
        self.state.keyup_handlers[pg.K_UP].append(character.handle_keyup)

        self.state.bomb_handlers[BombAction.START_EXPLOSION].append(self.start_bomb_explosion)
        self.state.bomb_handlers[BombAction.END_EXPLOSION].append(self.end_bomb_explosion)

        self.objects.append(character)
        self.hero = character


    def set_bomb(self):
        hr = self.hero.state.rect
        rect = BombRect(None, round(hr.left / cfg.TILE_SIZE) * cfg.TILE_SIZE, round(hr.top / cfg.TILE_SIZE) * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE)
        state = {
               'cellx': rect.left,
               'celly': rect.top,
               'rect': rect, 
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

        self.hero.state.bombs_count -= 1

    def start_bomb_explosion(self, eventdata):
        bomb = eventdata.bomb
        bomb.state.explosion = True
        cells = self.level.get_neighbour_free_tiles(bomb.state.cellx, bomb.state.celly)
        bomb.state.explosion_end_timeout = pg.time.get_ticks() + cfg.EXPLOSION_DURATION
        bomb.make_explosion_rects(cells)
        self.level.remove_obstacles(cells)

    def end_bomb_explosion(self, eventdata):
        bomb = eventdata.bomb
        bomb.state.explosion = False
        self.remove_bomb(bomb)

    def remove_bomb(self, bomb):
        self.objects.remove(bomb)
        self.level.bombs.remove(bomb)
        self.hero.state.bombs_count += 1

    def handle_exit_show(self, eventdata):
        pass

    def handle_exit_active(self, eventdata):
        self.hero.state.can_exit = True

    def handle_exit_open(self, eventdata):
        new_round = int(self.hero.state.round) + 1
        new_level = int(self.hero.state.level)
        if new_round > 8:
            new_round = 1
            new_level = new_level + 1

        self.hero.state.round = f'{new_round:02}'
        self.hero.state.level = f'{new_level:02}'
        self.hero.state.time_to_hide = 0
        self.hero.state.command.key = None
        self.hero.state.rect = None
        self.hero.state.can_exit = False
        self.hero.state.direction = Direction.NONE
        self.hero.state.old_direction = Direction.NONE
        # self.hero.state.password = StateManager().save_state_enc(json.dumps(self.hero.state.to_dict()))
        self.game.statemodel.play_next_round(data=self.hero.state)

    def handle_exit_replay(self, eventdata):
        lives = self.hero.state.lives
        if lives > 0:
            self.hero.state.lives = lives - 1
            self.game.statemodel.play_next_round(data=self.hero.state)            
        else:
            retries = self.hero.state.retries
            self.hero.state.time_to_hide = 0
            self.hero.state.command.key = None
            self.hero.state.rect = None
            self.hero.state.can_exit = False
            self.hero.state.direction = Direction.NONE
            self.hero.state.old_direction = Direction.NONE
            if retries > 0:
                self.hero.state.lives = 3
                self.hero.state.retries = retries - 1
                self.game.statemodel.play_gameover(data=self.hero.state)
            else:
                self.hero.state.round = '01'
                self.hero.state.level = '01'
                self.hero.state.lives = -1
                self.hero.state.retries = -1
                self.game.statemodel.play_gameover(data=self.hero.state)
                

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

    def process_hero_collisions(self, monster_rects):
        hero_rect = self.hero.state.rect
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

    def process_bomb_collisions(self, monster_rects):
        rects = self.level.bombs.get_rects()
        monsters_to_remove = []
        for i, r in enumerate(monster_rects):
            collisions = r.collidelist(rects)
            if isinstance(collisions, list) and len(collisions) > 0:
                for c in collisions:
                    if rects[c].bomb.state.explosion:
                        monsters_to_remove.append(self.level.monsters[i])
            else:     
                if collisions >= 0 and rects[collisions].bomb.state.explosion:
                    monsters_to_remove.append(self.level.monsters[i])
        
        for m in monsters_to_remove:
            self.level.monsters.remove(m)

        if len(self.level.monsters) <= 0:
            pg.event.post(Event(cfg.E_EXIT, action=ExitAction.ACTIVE))


    def process_collisions(self):
        monster_rects = self.level.monsters.get_rects()
        if monster_rects:
            self.process_hero_collisions(monster_rects)
            self.process_bomb_collisions(monster_rects)

    def update_state(self):
        if not self.paused:
            for o in self.objects:
                o.update_state()

            self.process_collisions()

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        if key == pg.K_ESCAPE:
            self.state.statemodel.play_menu(data=None)
        elif key == pg.K_p:
            self.paused = not self.paused
        elif key == pg.K_SPACE:
            if self.hero.state.bombs_count > 0:
                self.set_bomb()

