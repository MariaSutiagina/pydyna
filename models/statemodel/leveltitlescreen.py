import pygame as pg
from models.statemodel.gamestate import GameState
from models.leveltitleobject import LevelTitleObject

class LevelTitleScreen(GameState):
    def __init__(self, game, model):
        self.data = None
        super().__init__(game, model, 'LevelTitleScreen')

    def create_objects(self):
        self.menu = LevelTitleObject(self)
        self.objects.append(self.menu)

    def create_handlers(self):
        self.keydown_handlers[pg.K_SPACE].append(self.menu.handle_keydown)
        self.mouse_handlers.append(self.menu.mouse_handler)


