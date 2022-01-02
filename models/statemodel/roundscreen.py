import pygame as pg
from models.statemodel.gamestate import GameState

from models.roundobject import RoundObject
from utils.characterstate import CharacterState

class RoundScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'RoundScreen')

    def handle_on_enter(self, eventdata):
        self.init_objects()
        self.init_handlers()

        self.create_objects()
        self.create_handlers()

    def create_objects(self):
        self.roundobject = RoundObject(self.game, self)
        self.objects.append(self.roundobject)

    def create_handlers(self):
        self.keydown_handlers[pg.K_ESCAPE].append(self.roundobject.handle_keydown)
        self.keydown_handlers[pg.K_p].append(self.roundobject.handle_keydown)

