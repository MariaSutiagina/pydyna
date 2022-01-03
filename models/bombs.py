import random
from pygame.surface import Surface
from models.customobject import CustomObject
from models.monster import Monster
from utils.characterstate import CharacterState
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH, TILE_SIZE
from utils.utils import tile_pos_to_cell
from utils.types import Direction

class Bombs(CustomObject):
    def __init__(self, game):
        self.bombs = []
        self.game = game
        super().__init__(0, 0, FIELD_WIDTH, FIELD_HEIGHT)

    def clear(self):
        self.bombs = []

    def __iter__(self):
        return self.bombs.__iter__()

    def __next__(self):
        return self.bombs.__next__()

    def __getitem__(self, key):
        return self.bombs[key]

    def __setitem__(self, key, value):
        self.monsters[key] = value

    def append(self, value):
        self.bombs.append(value)

    def remove(self, value):
        self.bombs.remove(value)

    def get_rects(self):
        rects = []
        for m in self.bombs:
            if m.state.rects:
                rects.extend(m.state.rects)
            else:
                rects.append(m.state.rect)
        return rects

    def update_state(self):
        for bomb in self.bombs:
            bomb.update_state()

    def draw(self, surface:Surface):
        for bombs in self.bombs:
            bombs.draw(surface)

