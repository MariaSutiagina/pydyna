import pygame


import pygame as pg
from models.statemodel.gamestate import GameState
from models.gameovermenuobject import GameOverMenuObject

class GameOverScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'GameOverScreen')

    def handle_on_enter(self, eventdata):
        self.init_objects()
        self.init_handlers()

        self.create_objects()
        self.create_handlers()

    def create_objects(self):
        self.menu = GameOverMenuObject(self)
        self.objects.append(self.menu)

    def create_handlers(self):
        self.keydown_handlers[pg.K_SPACE].append(self.menu.handle_keydown)
        self.mouse_handlers.append(self.menu.mouse_handler)
