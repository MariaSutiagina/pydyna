import pygame as pg
from pygame.rect import Rect
from pygame.surface import Surface
from models.character import Character
from utils.characterstate import CharacterState
from utils.constants import FIELD_HEIGHT, FIELD_WIDTH, TILE_HEIGHT_IN_PIXEL, TILE_WIDTH_IN_PIXEL
from utils.types import Direction
from utils.utils import tile_pos_to_cell

class Monster(Character):
    def __init__(self, game, state:CharacterState):
        super().__init__(game, state)

    def get_resource_ids(self):
        rt = self.state.monstertype
        return [f'vampire{rt:02}-front', 
                f'vampire{rt:02}-side-lt', f'vampire{rt:02}-side-rt', 
                ]

    def add_resource(self, id, resource):
        parts = id.split('-')
        if parts[1] == 'front':
            self.state.resources.front = resource
        elif parts[1] == 'side':
            if parts[2] == 'lt':
                self.state.resources.left = resource
            elif parts[2] == 'rt':
                self.state.resources.right = resource

    def select_image(self):
        resource = self.state.resources.front.image['N001']
        if self.state.direction == Direction.UP:
            resource = self.state.resources.front.image[f'N{self.animation_stage:003}']
        elif self.state.direction == Direction.DOWN:
            resource = self.state.resources.front.image[f'N{self.animation_stage:003}']
        elif self.state.direction == Direction.LEFT:
            resource = self.state.resources.left.image[f'N{self.animation_stage:003}']
        elif self.state.direction == Direction.RIGHT:
            resource = self.state.resources.right.image[f'N{self.animation_stage:003}']
        
        return resource
