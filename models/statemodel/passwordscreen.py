from models.statemodel.gamestate import GameState

class PasswordScreen(GameState):
    def __init__(self, model):
        super().__init__(model, 'PasswordScreen')
