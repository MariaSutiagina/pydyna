import pygame as pg
from models.statemodel.gamestate import GameState
from models.titleobject import TitleObject

class TitleScreen(GameState):
    def __init__(self, model):
        super().__init__(model, 'TitleScreen')
        self.create_objects()
        self.create_handlers()

    def create_objects(self):
        self.titleobject = TitleObject(self)
        self.objects.append(self.titleobject)

    def create_handlers(self):
        self.keydown_handlers[pg.K_SPACE].append(self.titleobject.handle_keydown)
        self.mouse_handlers.append(self.titleobject.mouse_handler)



