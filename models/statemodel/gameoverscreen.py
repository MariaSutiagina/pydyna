import pygame


import pygame as pg
from models.statemodel.gamestate import GameState
from models.gameovermenuobject import GameOverMenuObject


# реализует состояние меню окончания игры (с демонстрацией пароля)
class GameOverScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'GameOverScreen')

    # заставку отрисовывает и обрабатывает события объект GameOverScreen
    def create_objects(self):
        self.menu = GameOverMenuObject(self)
        self.objects.append(self.menu)

    def create_handlers(self):
        # обрабатываеются только события нажатия на пробел и клика мышью
        self.keydown_handlers[pg.K_SPACE].append(self.menu.handle_keydown)
        self.mouse_handlers.append(self.menu.mouse_handler)
