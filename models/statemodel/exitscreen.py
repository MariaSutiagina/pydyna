from models.statemodel.gamestate import GameState

class ExitScreen(GameState):
    def __init__(self, model):
        super().__init__(model, 'ExitScreen')
