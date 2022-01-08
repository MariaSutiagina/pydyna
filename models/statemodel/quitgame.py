import pygame
import sys

from models.statemodel.gamestate import GameState

class QuitGame(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'QuitGame')

    def initialize(self):
        pygame.quit()
        sys.exit()
        


