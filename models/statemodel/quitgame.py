from models.statemodel.gamestate import GameState

class QuitGame(GameState):
    def __init__(self, model):
        super().__init__(model, 'QuitGame')
