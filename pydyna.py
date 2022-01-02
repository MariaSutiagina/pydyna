import pygame as pg
from transitions import Machine
from models.statemodel.statemodel import StateModel
import utils.constants as cfg


from models.game import Game

# класс игры Dyna Blaster
# наследуется от Game
class Dyna(Game):
    def __init__(self):
        self.init_pygame()
        Game.__init__(self, cfg.FRAME_RATE, self.init_states())
    
    def init_pygame(self):
        pg.mixer.init(44100, -16, 2, 4096)
        pg.init()
        pg.font.init()
        self.surface = pg.display.set_mode((cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT))
        pg.display.set_caption('Dyna Blaster')
        self.clock = pg.time.Clock()

    # инициализация машины состояний (экраны игры - заставки меню, заставки уровней, заставки раундов, раунды и т.д.)
    def init_states(self) -> StateModel:
        # инициализация модели состояний
        statemodel = StateModel(self) 
        # инициализация машины состояний в привязке к модели
        # statemodel - объект модели, который будет содержать граф состояний-переходов
        # statemode.states - список состояний модели
        # statemodel.transitions - список переходов из одного состояния в другое
        self.state_machine = Machine(statemodel, 
                                     states=statemodel.states, 
                                     transitions=statemodel.transitions, 
                                     send_event=True, 
                                     queued=True,
                                     model_attribute='game_state', initial='TitleScreen')
        return statemodel
    
    def get_state(self):
        return self.state_machine.get_state(self.statemodel.game_state)

def main():
    Dyna().run()


if __name__ == '__main__':
    main()
