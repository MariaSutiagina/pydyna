from models.statemodel.gamestate import GameState

class GameOverScreen(GameState):
    def __init__(self, game, model):
        super().__init__(game, model, 'GameOverScreen')
