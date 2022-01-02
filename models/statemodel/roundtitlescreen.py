import pygame as pg
from models.statemodel.gamestate import GameState
from models.roundtitleobject import RoundTitleObject

class RoundTitleScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'RoundTitleScreen')

    def handle_on_enter(self, eventdata):
        self.init_objects()
        self.init_handlers()

        self.create_objects()
        self.create_handlers()

    def create_objects(self):
        self.roundtitleobject = RoundTitleObject(self)
        self.objects.append(self.roundtitleobject)

    def create_handlers(self):
        self.keydown_handlers[pg.K_SPACE].append(self.roundtitleobject.handle_keydown)
        self.mouse_handlers.append(self.roundtitleobject.mouse_handler)


