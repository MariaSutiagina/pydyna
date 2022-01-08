import pygame as pg
from models.statemodel.gamestate import GameState
from models.passwordobject import PasswordObject

class PasswordScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'PasswordScreen')

    def create_objects(self):
        self.password_object = PasswordObject(self)
        self.objects.append(self.password_object)

    def create_handlers(self):
        self.keydown_handlers[pg.K_SPACE].append(self.password_object.handle_keydown)
        self.mouse_handlers.append(self.password_object.mouse_handler)
        self.dispatcher = self.password_object.dispatcher


