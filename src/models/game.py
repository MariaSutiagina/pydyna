import sys
import pygame

from utils.constants import E_BOMB, E_BRICK, E_EXIT, E_MONSTER, E_TREASURE

# реализует механизм основного цикла обработки событий игры,
#
class Game:
    def __init__(self, frame_rate, statemodel):
        self.frame_rate = frame_rate
        self.statemodel = statemodel
        # self.level = Level(self, 1, 1)

    def get_state(self):
        return None
    
    # реализует обновление состояний всех игровых объектов
    def update(self):
        # каждому объекту текущего игрового экрана говорим обновиться
        for o in self.get_state().objects:
            o.update_state()

    # реализует отрисовку игровых объектов
    def draw(self):
        # каждому объекту текущего игрового экрана говорим нарисовать себя на surface
        for o in self.get_state().objects:
            o.draw(self.surface)

    # реализует диспетчеризацию событий в обработчики событий в игровых объектах   
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: # на событие QUIT - выходим из игры
                self.statemodel.menu_exit()
            elif event.type == pygame.KEYDOWN:
                # передаем нажатие клавиатуры в обработчик на текущем экране игры
                for handler in self.get_state().keydown_handlers[event.key]:
                    handler(event.key, pygame.key.get_pressed())
            elif event.type == pygame.KEYUP:
                # передаем отпускание клавиатуры в обработчик на текущем экране игры
                for handler in self.get_state().keyup_handlers[event.key]:
                    handler(event.key, pygame.key.get_pressed())
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                # передаем событие мыши в обработчик на текущем экране игры
                for handler in self.get_state().mouse_handlers:
                    handler(event.type, event.pos)
            elif event.type == E_BOMB:
                #   передаем события от бомб в обработчики на текущем игровом экране
                for handler in self.get_state().bomb_handlers[event.action]:
                    handler(event)
            elif event.type == E_EXIT:
                #   передаем события от объекта "выход" в обработчики на текущем игровом экране
                for handler in self.get_state().exit_handlers[event.action]:
                    handler(event)
            elif event.type == E_MONSTER:
                #   передаем события от монстров в обработчики на текущем игровом экране
                for handler in self.get_state().monster_handlers[event.action]:
                    handler(event)
            elif event.type == E_TREASURE:
                #   передаем события от сокровищ в обработчики на текущем игровом экране
                for handler in self.get_state().treasure_handlers[event.action]:
                    handler(event)
            elif event.type == E_BRICK:
                #   передаем события от стен в обработчики на текущем игровом экране
                for handler in self.get_state().brick_handlers[event.action]:
                    handler(event)
        if self.get_state().dispatcher:
            # у каждого состояния (экрана) может быть спец. обработчик событий - dispatcher
            # такой обработчик, необходим, чтобы обрабатывать события вне основного цикла pygame_menu
            self.get_state().dispatcher(events)

    def run(self):
        # крутим игровой цикл, пока игра не перешла в состояние "выход" 
        while not self.statemodel.is_game_state_QuitGame():
            self.handle_events() # распределяем события по объектам
            self.update() # обновляем состояние объектов
            self.draw() # отрисовываем объекты

            pygame.display.update() # обновляем изображение на экране
            self.clock.tick(self.frame_rate) # сообщаем pygame, что все операции на этом шаге закончены и надо подождать до очередного тика
