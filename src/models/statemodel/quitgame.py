import pygame
import sys

from models.statemodel.gamestate import GameState

# реализует состояние выхода из игры
class QuitGame(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'QuitGame')

    def initialize(self):
        # закрываем pygame
        pygame.quit()
        # выходим
        sys.exit()
        


