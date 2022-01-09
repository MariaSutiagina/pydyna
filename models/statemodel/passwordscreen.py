import pygame as pg
from models.statemodel.gamestate import GameState
from models.passwordobject import PasswordObject


# реализует состояние входа в иргу с паролем
class PasswordScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'PasswordScreen')

    def create_objects(self):
        # отрисовку и обработку событий этого экрана реализует объек PasswordObject
        self.password_object = PasswordObject(self)
        self.objects.append(self.password_object)

    def create_handlers(self):
        # подключаем обработчики событий PasswordObject
        self.keydown_handlers[pg.K_SPACE].append(self.password_object.handle_keydown)
        self.mouse_handlers.append(self.password_object.mouse_handler)

        # у каждого состояния (экрана) может быть спец. обработчик событий - dispatcher
        # такой обработчик, необходим, чтобы обрабатывать события вне основного цикла pygame_menu
        # настраиваем у данного экрана такой обработчик (реальный обработчик будет в PasswordObject)
        self.dispatcher = self.password_object.dispatcher


