from typing import Tuple
import pygame as pg
import io
from pygame import Surface
from utils.resourcemanager import ResourceManager

from utils.utils import cell_pos_to_pixel, cell_size_in_pixel, tile_size_in_pixel
from utils.constants import ANIMATION_PERIOD, FADE_TIMEOUT, GAME_FONT_PATH, MOVEMENT_TIMEOUT, WALL_W, DIRECTION_CHANGE_FACTOR, TILE_SIZE
from utils.types import Direction
from utils.characterstate import CharacterState

from models.customobject import CustomObject
# from models.game import Game


class CustomCharacter(CustomObject):
    def __init__(self, game, state:CharacterState=None, image:Surface=None):
        self.font = pg.font.Font(GAME_FONT_PATH, 30)
        self.state = state
        self.game = game
        self.image = image

        pos = cell_pos_to_pixel(WALL_W + state.cellx, WALL_W + state.celly)
        sz = tile_size_in_pixel()
        super().__init__(*pos, *sz)
        self.init_resources()

    def get_resource_ids(self):
        return []

    def add_resource(self, id, resource):
        pass

    def init_resources(self):
        resource_ids = self.get_resource_ids()
        
        self.move_timeout = None
        self.movement_stopped = True
        self.animation_timeout = None
        self.animation_stage = 1
        self.animation_stages_count = 2

        self.images = dict()
        self.resources = dict()
        for id in resource_ids:
            self.add_resource(id, ResourceManager()[id])

    def select_image(self):
        resource = self.state.resources.up.dn.image['N001']
        if self.movement_stopped:
            if self.state.saved_direction == Direction.UP:
                resource = self.state.resources.up.up.image['N001']
            elif self.state.saved_direction == Direction.DOWN:
                resource = self.state.resources.down.up.image['N001']
            elif self.state.saved_direction == Direction.LEFT:
                resource = self.state.resources.left.up.image['N001']
            elif self.state.saved_direction == Direction.RIGHT:
                resource = self.state.resources.right.up.image['N001']
        else:
            if self.state.saved_direction == Direction.UP:
                resource = self.state.resources.up.dn.image[f'N{self.animation_stage:003}']
            elif self.state.saved_direction == Direction.DOWN:
                resource = self.state.resources.down.dn.image[f'N{self.animation_stage:003}']
            elif self.state.saved_direction == Direction.LEFT:
                resource = self.state.resources.left.dn.image[f'N{self.animation_stage:003}']
            elif self.state.saved_direction == Direction.RIGHT:
                resource = self.state.resources.right.dn.image[f'N{self.animation_stage:003}']
        
        return resource

    # создание фонового изображения
    def create_surface(self, resource) -> Surface:
        ts = tile_size_in_pixel()
        if resource:
            # достаем текущую картинку из ресурсов
            # и загружаем ее как поверхность pygame
            surface = pg.transform.scale(pg.image.load(io.BytesIO(resource)).convert_alpha(), ts)
        else:    
            color = (128, 128, 128)
            surface = pg.Surface(ts, pg.SRCALPHA)        
            surface.fill(color)

        return surface

    def draw(self, surface:Surface):
        resource = self.select_image()
        if resource:
            sfc = self.create_surface(resource.resource)
        else:
            sfc = self.image

        if not self.state.alive:
            if self.state.time_to_hide:
                share = (self.state.time_to_hide - pg.time.get_ticks()) / FADE_TIMEOUT
                sfc.set_alpha(int(255 * share))

        pos = cell_pos_to_pixel(WALL_W + self.state.cellx, WALL_W + self.state.celly)
        surface.blit(sfc, pos)
        


    def compute_position(self, speed:int, direction:Direction) -> Tuple:
        cellx = self.state.cellx
        celly = self.state.celly
        new_cellx = cellx
        new_celly = celly
        if direction == Direction.LEFT:
            new_cellx = cellx - speed
        elif direction == Direction.RIGHT:
            new_cellx = cellx + speed
        elif direction == Direction.UP:
            new_celly = celly - speed
        elif direction == Direction.DOWN:
            new_celly = celly + speed

        return (new_cellx, new_celly)
        
    def compute_speed(self) -> int:
        speed = self.state.speed
        if not speed:
            speed = 1
        return speed
    
    def compute_direction(self) -> Direction:
        return Direction.NONE

    def update_animation(self):
        if self.animation_timeout is None:
            self.animation_timeout = pg.time.get_ticks() + ANIMATION_PERIOD
        if pg.time.get_ticks() >= self.animation_timeout:
            self.animation_stage = self.animation_stage % self.animation_stages_count + 1
            self.animation_timeout = pg.time.get_ticks() + ANIMATION_PERIOD

    def update_movement(self):
        if self.move_timeout is None:
            self.move_timeout = pg.time.get_ticks() + MOVEMENT_TIMEOUT
        if pg.time.get_ticks() >= self.move_timeout:
            self.movement_stopped = True
        

    def update_state(self):
        self.update_animation()
        self.update_movement()

    def compute_and_update_state(self, position:Tuple, speed:int, direction:Direction):
        self.state.cellx = position[0]
        self.state.celly = position[1]
        self.state.speed = speed
        self.state.rect = pg.Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)

        # if direction != self.state.old_direction or direction == Direction.NONE:
        #     self.state.old_direction = self.state.direction
        if self.state.direction != Direction.NONE:
            self.state.old_direction = self.state.direction
        
        self.state.direction = direction

