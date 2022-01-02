import pygame
import sys

from models.statemodel.gamestate import GameState

class QuitGame(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'QuitGame')

    def handle_on_enter(self, eventdata):
        pygame.quit()
        sys.exit()
        


