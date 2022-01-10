import pygame as pg
from models.statemodel.gamestate import GameState
from models.gamewinobject import GameWinObject

# реализует состояние финального экрана
class  GameWinScreen(GameState):
    def __init__(self, game, model):
        self.data = None
        super().__init__(game, model, 'GameWinScreen')

    # заставку отрисовывает и обрабатывает события объект GameWinObject
    def create_objects(self):
        self.gamewinobject = GameWinObject(self)
        self.objects.append(self.gamewinobject)

    def create_handlers(self):
        # обрабатываеются только события нажатия на пробел и клика мышью
        self.keydown_handlers[pg.K_SPACE].append(self.gamewinobject.handle_keydown)
        self.mouse_handlers.append(self.gamewinobject.mouse_handler)


