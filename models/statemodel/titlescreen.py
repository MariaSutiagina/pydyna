import pygame as pg
from models.statemodel.gamestate import GameState
from models.titleobject import TitleObject
import utils.constants as cfg

# реализует состояние игровой заставки
class TitleScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'TitleScreen')
        self.initialize()

    # заставку отрисовывает и обрабатывает события объект TitleObject
    def create_objects(self):
        self.titleobject = TitleObject(self)
        self.objects.append(self.titleobject)

    def create_handlers(self):
        # обрабатываеются только события нажатия на пробел и клика мышью
        self.keydown_handlers[pg.K_SPACE].append(self.titleobject.handle_keydown)
        self.mouse_handlers.append(self.titleobject.mouse_handler)



