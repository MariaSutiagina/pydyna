import pygame as pg
from models.statemodel.gamestate import GameState
from models.leveltitleobject import LevelTitleObject

# реализует состояние заставки уровня
class LevelTitleScreen(GameState):
    def __init__(self, game, model):
        self.data = None
        super().__init__(game, model, 'LevelTitleScreen')

    # заставку отрисовывает и обрабатывает события объект LevelTitleObject
    def create_objects(self):
        self.menu = LevelTitleObject(self)
        self.objects.append(self.menu)

    def create_handlers(self):
        # обрабатываеются только события нажатия на пробел и клика мышью
        self.keydown_handlers[pg.K_SPACE].append(self.menu.handle_keydown)
        self.mouse_handlers.append(self.menu.mouse_handler)


