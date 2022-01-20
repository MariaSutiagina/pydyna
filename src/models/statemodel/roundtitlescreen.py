import pygame as pg
from models.statemodel.gamestate import GameState
from models.roundtitleobject import RoundTitleObject

# реализует состояние заставки уровня
class RoundTitleScreen(GameState):
    def __init__(self, game, model):
        self.data = None
        super().__init__(game, model, 'RoundTitleScreen')

    # заставку отрисовывает и обрабатывает события объект RoundTitleObject
    def create_objects(self):
        self.roundtitleobject = RoundTitleObject(self)
        self.objects.append(self.roundtitleobject)

    def create_handlers(self):
        # обрабатываеются только события нажатия на пробел и клика мышью
        self.keydown_handlers[pg.K_SPACE].append(self.roundtitleobject.handle_keydown)
        self.mouse_handlers.append(self.roundtitleobject.mouse_handler)


