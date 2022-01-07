import random
from pygame.surface import Surface
from models.customobject import CustomObject
from models.monster import Monster
from models.monsterfactory import MonsterFactory
from utils.characterstate import CharacterState
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH, TILE_SIZE
from utils.utils import tile_pos_to_cell
from utils.types import Direction

class Monsters(CustomObject):
    def __init__(self, game, monsterdata):
        self.monsters = []
        self.game = game
        super().__init__(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.load(monsterdata)

    def load(self, monsterdata):
        for md in monsterdata:
            state = MonsterFactory()[md['type']] 
            pos = md['pos']
            state.cellx = pos[0] * TILE_SIZE
            state.celly = pos[1] * TILE_SIZE
            self.monsters.append(Monster(self.game, state))

    def clear(self):
        self.monsters = []

    def __iter__(self):
        return self.monsters.__iter__()

    def __next__(self):
        return self.monsters.__next__()

    def __getitem__(self, key):
        return self.monsters[key]

    def __setitem__(self, key, value):
        self.monsters[key] = value

    def __len__(self):
        return len(self.monsters)

    def append(self, value):
        self.monsters.append(value)

    def remove(self, value):
        self.monsters.remove(value)

    def get_rects(self):
        rects = []
        for m in self.monsters:
            rects.append(m.state.rect)
        return rects

    def update_state(self):
        for monster in self.monsters:
            monster.update_state()

    def draw(self, surface:Surface):
        for monster in self.monsters:
            monster.draw(surface)

