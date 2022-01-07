import random
from models.monster import Monster
from utils.characterstate import CharacterState
from utils.singleton import MetaSingleton
from utils.types import Direction

class MonsterFactory(metaclass=MetaSingleton):
    def __init__(self):
        self.config = {
            1: {'lifes':1, 'speed': 1, 'direction_change_factor':5, 'can_fly': 0, 'is_boss': 0, 'is_chain': 0, 'has_children':0, 'pregnancy_duration':0, 'children_type': 0},
            2: {'lifes':1, 'speed': 1, 'direction_change_factor':3, 'can_fly': 0, 'is_boss': 0, 'is_chain': 0, 'has_children':0, 'pregnancy_duration':0, 'children_type': 0},
            3: {'lifes':1, 'speed': 2, 'direction_change_factor':3, 'can_fly': 0, 'is_boss': 0, 'is_chain': 0, 'has_children':0, 'pregnancy_duration':0, 'children_type': 0},
            100: {'lifes':3, 'speed': 1, 'direction_change_factor':4, 'can_fly': 0, 'is_boss': 1, 'is_chain': 4, 'has_children':0, 'pregnancy_duration':0, 'children_type': 0},
            4: {'lifes':1, 'speed': 1, 'direction_change_factor':6, 'can_fly': 1, 'is_boss': 0, 'is_chain': 0, 'has_children':0, 'pregnancy_duration':0, 'children_type': 0},
            200: {'lifes':3, 'speed': 1, 'direction_change_factor':3, 'can_fly': 0, 'is_boss': 1, 'is_chain': 0, 'has_children':4, 'pregnancy_duration':60, 'children_type': 1},
        }

    def create_monster_state(self, monstertype):
        cfg = self.config[monstertype]
        state = CharacterState()
        state.monstertype = monstertype
        state.speed = cfg['speed']
        state.alive = True
        state.lifes = cfg['lifes']
        state.is_monster = True
        state.is_hero = False
        state.is_bomb = False
        state.direction = random.choice([Direction.RIGHT, Direction.LEFT, Direction.UP, Direction.DOWN])
        state.old_direction = state.direction
        state.capabilities = self.config[monstertype].copy()
        return state


    def __getitem__(self, key):
        return self.create_monster_state(key)
