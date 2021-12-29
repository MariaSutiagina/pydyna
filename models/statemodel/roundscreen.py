import pygame as pg
from models.statemodel.gamestate import GameState

from models.roundobject import RoundObject

class RoundScreen(GameState):
    def __init__(self, model):
        super().__init__(model, 'RoundScreen')
        self.create_objects()
        self.create_handlers()

    def create_objects(self):
        self.roundobject = RoundObject(self)
        self.objects.append(self.roundobject)

    def create_handlers(self):
        self.keydown_handlers[pg.K_ESCAPE].append(self.roundobject.handle_keydown)
        self.keydown_handlers[pg.K_p].append(self.roundobject.handle_keydown)

