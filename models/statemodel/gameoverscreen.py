from models.statemodel.gamestate import GameState

class GameOverScreen(GameState):
    def __init__(self, model):
        super().__init__(model, 'GameOverScreen')
