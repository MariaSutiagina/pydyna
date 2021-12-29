from models.statemodel.titlescreen import TitleScreen
from models.statemodel.menuscreen import MenuScreen
from models.statemodel.exitscreen import ExitScreen
from models.statemodel.passwordscreen import PasswordScreen
from models.statemodel.gameoverscreen import GameOverScreen
from models.statemodel.leveltitlescreen import LevelTitleScreen
from models.statemodel.roundtitlescreen import RoundTitleScreen
from models.statemodel.roundscreen import RoundScreen
from models.statemodel.quitgame import QuitGame

class StateModel:
    def __init__(self):
        self.init_states()
        self.init_transitions()

    def init_states(self):
        self.states_list = [
            TitleScreen(self),
            MenuScreen(self),
            ExitScreen(self),
            PasswordScreen(self),
            GameOverScreen(self),
            LevelTitleScreen(self),
            RoundTitleScreen(self),
            RoundScreen(self),
            QuitGame(self)
        ]

    def init_transitions(self):
        self.transitions_list = [
            {'trigger': 'title_menu', 'source': 'TitleScreen', 'dest': 'MenuScreen'},
            {'trigger': 'menu_exit', 'source': 'MenuScreen', 'dest': 'ExitScreen'},
            {'trigger': 'exit_quit', 'source': 'ExitScreen', 'dest': 'QuitGame'},
            {'trigger': 'menu_level', 'source': 'MenuScreen', 'dest': 'LevelTitleScreen'},
            {'trigger': 'menu_password', 'source': 'MenuScreen', 'dest': 'PasswordScreen'},
            {'trigger': 'level_round', 'source': 'LevelTitleScreen', 'dest': 'RoundTitleScreen'},
            {'trigger': 'round_play', 'source': 'RoundTitleScreen', 'dest': 'RoundScreen'},
            {'trigger': 'play_exit', 'source': 'RoundScreen', 'dest': 'MenuScreen'},
            {'trigger': 'play_next_round', 'source': 'RoundScreen', 'dest': 'RoundTitleScreen'},
            {'trigger': 'play_next_level', 'source': 'RoundScreen', 'dest': 'LevelTitleScreen'},
            {'trigger': 'play_gameover', 'source': 'RoundScreen', 'dest': 'GameOverScreen'},
            {'trigger': 'gameover_continue', 'source': 'GameOverScreen', 'dest': 'RoundTitleScreen'},
            {'trigger': 'gameover_end', 'source': 'GameOverScreen', 'dest': 'MenuScreen'},
            {'trigger': 'password_play', 'source': 'PasswordScreen', 'dest': 'RoundScreen'},

        ]
        pass

    @property
    def states(self):
        return self.states_list

    @property
    def transitions(self):
        return self.transitions_list
