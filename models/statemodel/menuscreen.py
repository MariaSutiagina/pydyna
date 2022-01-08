import pygame as pg
from models.statemodel.gamestate import GameState
from models.menuobject import MenuObject

class MenuScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'MenuScreen')

    def create_objects(self):
        self.menu = MenuObject(self)
        self.objects.append(self.menu)

    def create_handlers(self):
        self.keydown_handlers[pg.K_SPACE].append(self.menu.handle_keydown)
        self.mouse_handlers.append(self.menu.mouse_handler)


