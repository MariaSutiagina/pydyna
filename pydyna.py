import pygame as pg

from models.game import Game
from models.wall import Wall
from models.field import Field
from models.character import Character
from utils.characterstate import CharacterState

import utils.constants as cfg
from utils.types import Direction

class Dyna(Game):
    def __init__(self):
        Game.__init__(self, 'Dyna Blaster', cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT, None, cfg.FRAME_RATE)
        # self.sound_effects = {name: pygame.mixer.Sound(sound) for name, sound in c.sounds_effects.items()}
        # self.reset_effect = None
        # self.effect_start_time = None
        # self.score = 0
        # self.lives = c.initial_lives
        # self.start_level = False
        # self.paddle = None
        # self.bricks = None
        # self.ball = None
        # self.menu_buttons = []
        # self.is_game_running = False
        self.create_objects()
        # self.points_per_brick = 1

    def create_objects(self):
        self.create_wall()
        self.create_field()
        self.create_characters()

    def create_wall(self):
        self.wall = Wall()
        self.objects.append(self.wall)

    def create_field(self):
        self.field = Field()
        self.objects.append(self.field)

    def get_character_image(self):
        color = (0, 255, 255)
        width = cfg.TILE_WIDTH_IN_PIXEL
        height = cfg.TILE_HEIGHT_IN_PIXEL
        surface = pg.Surface((width, height), pg.SRCALPHA)
        surface.fill(color)
        pg.draw.circle(surface, (255, 0, 0), (width // 2, height // 2), width //2, width=5)
        
        return surface

    def create_characters(self):
        state = {
               'cellx': 0,
               'celly': 0,
               'speed': 1,
               'direction': Direction.RIGHT,
               'old_direction': Direction.RIGHT
               }

        character = Character(self, CharacterState(state), self.get_character_image())
        self.objects.append(character)

    def update(self):
        super().update()

def main():
    Dyna().run()


if __name__ == '__main__':
    main()
