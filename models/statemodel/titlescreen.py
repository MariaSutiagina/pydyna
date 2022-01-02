import pygame as pg
from models.statemodel.gamestate import GameState
from models.titleobject import TitleObject
import utils.constants as cfg

class TitleScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'TitleScreen')
        self.initialize()

    def initialize(self):

        self.init_objects()
        self.init_handlers()

        self.create_objects()
        self.create_handlers()

    def handle_on_enter(self, eventdata):
        self.initialize()

    def create_objects(self):
        self.titleobject = TitleObject(self)
        self.objects.append(self.titleobject)

    def create_handlers(self):
        self.keydown_handlers[pg.K_SPACE].append(self.titleobject.handle_keydown)
        self.mouse_handlers.append(self.titleobject.mouse_handler)



