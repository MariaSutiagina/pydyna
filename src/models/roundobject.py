import random
from typing import Sequence
import pygame as pg
from pygame import Rect, Surface
from pygame.event import Event
from models.bomb import Bomb, BombRect
from models.customscreenobject import CustomScreenObject
from models.hero import Hero
from models.level import Level
from models.monster import Monster
from models.monsterfactory import MonsterFactory
from models.stateobject import StateObject
from models.wall import Wall
from models.field import Field
from utils.characterstate import CharacterState

import utils.constants as cfg
from utils.statemanager import StateManager
from utils.types import BombAction, Direction, ExitAction, MonsterAction, TreasureAction
from utils.utils import collision_rect


# при входе в раунд создаетс объек RoundObject
# Наследуется от CustomScreenObject
class RoundObject(CustomScreenObject):
    def __init__(self, game, state):
        super().__init__(state)
        self.game = game
        self.paused = False
        self.exited = False
        self.exit_timeout = None
        self.create_objects()
            
    # инициализирует все объекты раунда
    def create_objects(self):
        # создаем список объектов
        # которые потом будем опрашивать на предмет изменения состояния и 
        # обработки событий от клавиатуры и др игровых событий
        self.objects = []

        # инициализируем уровень
        # вытаскиваем его из базы по параметрам level и round  
        self.create_level(self.state.statemodel.data)
        # инициализируем границы поля
        self.create_wall()
        # инициализируем поле
        self.create_field()
        # инициализируем монстров
        self.create_characters()
        # инициализируем героя
        self.create_hero(self.state.statemodel.data)
        # инициализируем объект отображения состояния
        self.create_state_object()

        self.objects.sort(key=lambda x: x.get_sort_key())

    # инициализируем объект отображения состояния
    def create_state_object(self):
        # создаем объект StateObject
        # и добаввляем его в списой объектов
        self.stateobject = StateObject(self.game, self.hero.state)
        self.objects.append(self.stateobject)
    
    # инициализируем уровень
    # вытаскиваем его из базы по параметрам level и round  
    def create_level(self, hero_state):
        level = '01'
        round = '01'
        if hero_state:
            level = hero_state.level
            round = hero_state.round
        # создаем объект Level
        self.level = Level(self.game, int(level), int(round))

    
    # инициализируем границы поля
    def create_wall(self):
        # создаем объект Wall и добавляем в список объектов
        self.wall = Wall(self.level)
        self.objects.append(self.wall)

    # инициализируем поле
    def create_field(self):
        # создаем объект  Field и добавляем в список объектов
        self.field = Field(self.level)
        self.objects.append(self.field)

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
               'score': 0,
               'lifes': 3,
               'retries': 3,
               'round': '01',
               'level': '01', 
               'is_monster': False,
               'is_hero': True,
               'is_bomb': False,
               'bombs_capacity': 3,
               'bombs_strength': 1,
               'can_exit': False,
               'can_fly': False,
               'can_remote': False,
               'can_use_exit': False,
               'is_killer': False,
               'speed': 1,
               'treasure_timeout': None,
               'direction': Direction.NONE,
               'old_direction': Direction.NONE,
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
        hero_state.round_timeout = pg.time.get_ticks() + cfg.ROUND_TIMEOUT

        character = Hero(self.game, hero_state)
        
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
        if  self.level.is_tile_free(rect.left, rect.top):
            state = {
                'cellx': rect.left,
                'celly': rect.top,
                'rect': rect, 
                'lifes': 3,
                'is_monster': False,
                'is_hero': False,
                'is_bomb': True,
                'is_exited': False, 
                'is_remote': self.hero.state.can_remote,
                'explosion_timeout': pg.time.get_ticks() + cfg.EXPLOSION_TIMEOUT,
                'explosion_size': self.hero.state.bombs_strength,
                'explosion': False,
                'speed': 0,
                'direction': Direction.NONE,
                'old_direction': Direction.NONE
                }
            bomb = Bomb(self.game, CharacterState(state))
            self.level.bombs.append(bomb)
            self.objects.append(bomb)

            self.objects.sort(key=lambda x: x.get_sort_key())
    
            self.state.treasure_handlers[TreasureAction.INACTIVE].append(bomb.handle_inactive_treasure)
            self.hero.state.bombs_count -= 1

    def start_bomb_explosion(self, eventdata):
        bomb = eventdata.bomb
        bomb.state.explosion = True
        cells = self.level.get_neighbour_free_tiles(bomb.state.cellx, bomb.state.celly, bomb.state.explosion_size)
        bomb.state.explosion_end_timeout = pg.time.get_ticks() + cfg.EXPLOSION_DURATION
        bomb.make_explosion_rects(cells)
        self.level.remove_obstacles(cells)

    def end_bomb_explosion(self, eventdata):
        bomb = eventdata.bomb
        bomb.state.explosion = False
        self.remove_bomb(bomb)

    def remove_bomb(self, bomb):
        self.state.treasure_handlers[TreasureAction.INACTIVE].remove(bomb.handle_inactive_treasure)
        self.objects.remove(bomb)
        self.level.bombs.remove(bomb)
        self.hero.state.bombs_count += 1

    def handle_exit_show(self, eventdata):
        pass

    def handle_exit_active(self, eventdata):
        self.hero.state.can_exit = True

    def handle_exit_open(self, eventdata):
        if self.exit_timeout is None:
            self.exit_timeout = pg.time.get_ticks() + cfg.EXIT_TIMEOUT
        if pg.time.get_ticks() >= self.exit_timeout:
            self.exit_timeout =  0
            self.exited = False

            new_round = int(self.hero.state.round) + 1
            old_level = new_level = int(self.hero.state.level)

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
            self.hero.state.can_fly = False
            self.hero.state.can_remote = False
            self.hero.state.is_killer = False
            self.hero.state.is_exited = False
            self.hero.state.can_use_exit = False
            self.hero.state.treasure_timeout = None
            self.hero.state.round_timeout = None

            if StateManager().check_state(self.hero.state):
                if new_level > old_level:
                    pg.mixer.music.stop()
                    self.hero.state.score += cfg.LEVEL_SCORE
                    self.game.statemodel.play_next_level(data=self.hero.state)
                else:
                    pg.mixer.music.stop()
                    self.hero.state.score += cfg.ROUND_SCORE
                    self.game.statemodel.play_next_round(data=self.hero.state)
            else:
                pg.mixer.music.stop()
                self.game.statemodel.play_win()
        else:
            self.hero.state.is_exited = True
            self.exited = True
            pg.time.set_timer(event=Event(cfg.E_EXIT, action=ExitAction.OPEN), millis=cfg.EXIT_TIMEOUT, loops=1)

    def handle_exit_replay(self, eventdata):
        lifes = self.hero.state.lifes
        if lifes > 0:
            self.hero.state.lifes = lifes - 1
            self.game.statemodel.play_next_round(data=self.hero.state)            
        else:
            retries = self.hero.state.retries
            self.hero.state.time_to_hide = 0
            self.hero.state.command.key = None
            self.hero.state.rect = None
            self.hero.state.can_exit = False
            self.hero.state.direction = Direction.NONE
            self.hero.state.old_direction = Direction.NONE
            self.hero.state.bombs_strength = 1
            self.hero.state.bombs_capacity = 3
            self.hero.state.speed = 1
            self.hero.state.score = 0

            self.hero.state.treasure_timeout = None
            self.hero.state.round_timeout = None
            if retries > 0:
                self.hero.state.lifes = 3
                self.hero.state.retries = retries - 1
                self.game.statemodel.play_gameover(data=self.hero.state)
            else:
                self.hero.state.round = '01'
                self.hero.state.level = '01'
                self.hero.state.lifes = -1
                self.hero.state.retries = -1
                self.game.statemodel.play_gameover(data=self.hero.state)
                
    def handle_create_extra_monsters(self, eventdata):
        monster = eventdata.monster
        if monster:
            children_count = monster.get_has_children()
            if children_count > 0:
                caps = monster.get_capabilities()
                child_type = caps['children_type']
                for c in range(children_count):
                    state = MonsterFactory()[child_type] 
                    state.cellx = monster.state.cellx
                    state.celly = monster.state.celly
                    self.level.monsters.append(Monster(self.game, state))
        else:
            for c in range(cfg.RANDOM_CHILDREN_COUNT):
                state = MonsterFactory()[-1] 
                cell = random.choice(list(self.level.floor.items()))
                state.cellx = cell[0][0] * cfg.TILE_SIZE
                state.celly = cell[0][1] * cfg.TILE_SIZE
                self.level.monsters.append(Monster(self.game, state))

    def handle_show_treasure(self, eventdata):
        if eventdata.treasure[1][0] > 0:
            res = self.level.treasure_resources
            stage = eventdata.treasure_stage % len(res)
            self.level.treasure = (eventdata.treasure[0], (eventdata.treasure[1][0], res[stage]))

            pg.time.set_timer(Event(cfg.E_TREASURE, 
                                    action=TreasureAction.SHOW, 
                                    treasure=self.level.treasure, 
                                    treasure_stage=stage + 1), 
                              millis = cfg.ANIMATION_PERIOD, loops=1)
    
    def handle_open_treasure(self, eventdata):
        self.hero.apply_treasure(self.level.treasure[1][0])
        self.hero.state.score += cfg.TREASURE_SCORE
        pg.event.post(Event(cfg.E_TREASURE, action=TreasureAction.HIDE))
    
    def handle_hide_treasure(self, eventdata):
        self.level.remove_treasure()

    def handle_inactive_treasure(self, eventdata):
        self.hero.state.can_fly = False
        self.hero.state.can_remote = False
        self.hero.state.is_killer = False
        self.hero.state.can_use_exit = False

    def handle_remove_brick(self, eventdata):
        self.hero.state.score += cfg.BRICK_SCORE

    
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
        monsters_to_remove = set() 
        if isinstance(collisions,list):
            for c in collisions:
                if self.check_collision(hero_rect, monster_rects[c]):
                    if not self.hero.state.is_killer:
                        self.hero.state.alive = False
                        self.hero.state.time_to_hide = pg.time.get_ticks() + cfg.FADE_TIMEOUT
                        break
                    else:
                        if c.character.state.lifes > 1:
                            c.character.state.lifes -= 1
                        else:
                            monsters_to_remove.add(c.character)
        else:
            if collisions >= 0 and self.check_collision(hero_rect, monster_rects[collisions]):
                if not self.hero.state.is_killer:
                    self.hero.state.alive = False
                    if not self.hero.state.time_to_hide:
                        self.hero.state.time_to_hide = pg.time.get_ticks() + cfg.FADE_TIMEOUT
                else:
                    c = monster_rects[collisions]
                    if c.character.state.lifes > 1:
                        c.character.state.lifes -= 1
                    else:
                        monsters_to_remove.add(c.character)

        for m in monsters_to_remove:
            self.level.monsters.remove(m)
            self.hero.state.score += m.state.score

        if len(self.level.monsters) <= 0:
            pg.event.post(Event(cfg.E_EXIT, action=ExitAction.ACTIVE))

    def process_bomb_collisions(self, monster_rects):
        rects = self.level.bombs.get_rects()
        monsters_to_remove = set() 
        for i, r in enumerate(monster_rects):
            collisions = r.collidelist(rects)
            if isinstance(collisions, list) and len(collisions) > 0:
                for c in collisions:
                    if rects[c].bomb.state.explosion and \
                           (r.character.state.blowed_by is None or r.character.state.blowed_by != rects[c].bomb):
                        if r.character.state.lifes > 1:
                            r.character.state.lifes -= 1
                            r.character.state.blowed_by = rects[c].bomb
                        else:
                            monsters_to_remove.add(r.character)
            else:     
                if collisions >= 0 and rects[collisions].bomb.state.explosion and \
                           (r.character.state.blowed_by is None or r.character.state.blowed_by != rects[collisions].bomb):
                    if r.character.state.lifes > 1:
                        r.character.state.lifes -= 1
                        r.character.state.blowed_by = rects[collisions].bomb
                    else:
                        monsters_to_remove.add(r.character)
        
        for m in monsters_to_remove:
            self.level.monsters.remove(m)
            self.hero.state.score += m.state.score

        if len(self.level.monsters) <= 0:
            pg.event.post(Event(cfg.E_EXIT, action=ExitAction.ACTIVE))


    def process_collisions(self):
        monster_rects = self.level.monsters.get_rects()
        if monster_rects:
            self.process_hero_collisions(monster_rects)
            self.process_bomb_collisions(monster_rects)

        if pg.time.get_ticks() > self.hero.state.round_timeout:
            pg.event.post(Event(cfg.E_MONSTER, action=MonsterAction.CREATE_EXTRA, monster=None))
            self.hero.state.round_timeout = pg.time.get_ticks() + cfg.ROUND_TIMEOUT


    def update_state(self):
        super().update_state()
        if not self.paused and not self.exited:
            for o in self.objects:
                o.update_state()

            self.process_collisions()

    def handle_keydown(self, key:int, keys_pressed:Sequence[bool]):
        if key == pg.K_ESCAPE:
            self.state.statemodel.play_menu(data=None)
        elif key == pg.K_p:
            self.paused = not self.paused
            if self.paused:
                self.pause_start_time = pg.time.get_ticks()
            else:
                self.hero.state.round_timeout += pg.time.get_ticks() - self.pause_start_time
        elif key == pg.K_SPACE:
            if self.hero.state.bombs_count > 0:
                self.set_bomb()
        elif key == pg.K_RETURN:
            if self.hero.state.can_remote and len(self.level.bombs) > 0:
                for bomb in self.level.bombs:
                    if not bomb.state.explosion:
                        pg.event.post(Event(cfg.E_BOMB , action=BombAction.START_EXPLOSION, bomb=bomb))
                        break


