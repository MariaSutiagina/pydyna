from models.statemodel.gamewinscreen import GameWinScreen
from models.statemodel.titlescreen import TitleScreen
from models.statemodel.menuscreen import MenuScreen
from models.statemodel.passwordscreen import PasswordScreen
from models.statemodel.gameoverscreen import GameOverScreen
from models.statemodel.leveltitlescreen import LevelTitleScreen
from models.statemodel.roundtitlescreen import RoundTitleScreen
from models.statemodel.roundscreen import RoundScreen
from models.statemodel.quitgame import QuitGame

# модель состояний для переходов между игровыми экранами
class StateModel:
    def __init__(self, game):
        self.data = None
        self.init_states(game)
        self.init_transitions()
    
    # инициализируем состояния
    def init_states(self, game):
        self.states_list = [
            TitleScreen(game, self),         # экран игровой заставки
            MenuScreen(game, self),          # экран меню
            PasswordScreen(game, self),      # экран ввода пароля для возобновления игры с прежнего уровня после неудачного окончания
            GameOverScreen(game, self),      # экран неудачного окончания игры менюшкой и демонстрацией пароля для возврата на прежний раун
            LevelTitleScreen(game, self),    # заставка уровня
            RoundTitleScreen(game, self),    # заставка раунда
            RoundScreen(game, self),         # игровой уровень
            GameWinScreen(game, self),       #  финальный экран
            QuitGame(game, self)             # техническое состояние - выход из игры
        ]

    # инициализируем переходы между состояниями
    def init_transitions(self):
        self.transitions_list = [
            # из экрана игровой заставки TitleScreen попадаем в экран меню MenuScreen сгенерировав событие title_menu
            {'trigger': 'title_menu', 'source': 'TitleScreen', 'dest': 'MenuScreen'},
            # из экрана MenuScreen попадаем в состояние выхода из игры QuitGame сгенерировав событие menu_exit
            {'trigger': 'menu_exit', 'source': '*', 'dest': 'QuitGame'},
            # из экрана MenuScreen попадаем  на экран заставки уровня LevelTitleScreen сгенерировав событие menu_level
            {'trigger': 'menu_level', 'source': 'MenuScreen', 'dest': 'LevelTitleScreen'},
            # из экрана MenuScreen попадаем  на экран ввода пароля для возобновления игры с прежнего раунда PasswordScreen сгенерировав событие menu_password
            {'trigger': 'menu_password', 'source': 'MenuScreen', 'dest': 'PasswordScreen'},
            # из экрана LevelTitleScreen попадаем в экран заставки раунда RoundTitleScreen сгенерировав событие level_round
            {'trigger': 'level_round', 'source': 'LevelTitleScreen', 'dest': 'RoundTitleScreen'},
            # из экрана RoundTitleScreen попадаем в экран игрового раунда RoundScreen сгенерировав событие round_ play
            {'trigger': 'round_play', 'source': 'RoundTitleScreen', 'dest': 'RoundScreen', 'before': 'set_environment'},
            # из экрана RoundScreen попадаем в экран меню MenuScreen сгенерировав событие play_exit
            {'trigger': 'play_exit', 'source': 'RoundScreen', 'dest': 'MenuScreen', 'before': 'set_environment'},
            # из экрана RoundScreen попадаем в экран заставки нового раунда RoundTitleScreen сгенерировав событие play_next_round
            {'trigger': 'play_next_round', 'source': 'RoundScreen', 'dest': 'RoundTitleScreen', 'before': 'set_environment'},
            # из экрана RoundScreen попадаем в экран заставки нового уровня RoundTitleScreen сгенерировав событие play_next_level
            {'trigger': 'play_next_level', 'source': 'RoundScreen', 'dest': 'LevelTitleScreen', 'before': 'set_environment'},
            # из экрана RoundScreen попадаем в экран меню окончания игры GameOverScreen сгенерировав событие play_gameover
            {'trigger': 'play_gameover', 'source': 'RoundScreen', 'dest': 'GameOverScreen', 'before': 'set_environment'},
            # из экрана RoundScreen попадаем в экран окончания игры GameWinScreen сгенерировав событие play_win
            {'trigger': 'play_win', 'source': 'RoundScreen', 'dest': 'GameWinScreen', 'before': 'set_environment'},
            # из экрана RoundScreen попадаем в экран меню игры MenuScreen сгенерировав событие play_menu
            {'trigger': 'play_menu', 'source': 'RoundScreen', 'dest': 'MenuScreen'},
            # из экрана GameOverScreen попадаем в экран заставки раунда RoundTitleScreen для продолжения игры сгенерировав событие gameover_continue
            {'trigger': 'gameover_continue', 'source': 'GameOverScreen', 'dest': 'RoundTitleScreen', 'before': 'set_environment'},
            # из экрана GameWinScreen попадаем в экран меню MenuScreen сгенерировав событие gamewin_menu
            {'trigger': 'gamewin_menu', 'source': 'GameWinScreen', 'dest': 'MenuScreen'},
            # из экрана GameOverScreen попадаем в экран меню MenuScreen сгенерировав событие gameover_end
            {'trigger': 'gameover_end', 'source': 'GameOverScreen', 'dest': 'MenuScreen', 'before': 'set_environment'},
            # из экрана PasswordScreen попадаем в экран заставки раунда RoundTitleScreen сгенерировав событие password_play
            {'trigger': 'password_play', 'source': 'PasswordScreen', 'dest': 'RoundTitleScreen'},
            # из экрана PasswordScreen попадаем в экран заставки  меню MenuScreen сгенерировав событие password_menu
            {'trigger': 'password_menu', 'source': 'PasswordScreen', 'dest': 'MenuScreen'},

        ]

    #   при входе в каждое состояние вызываем обработчик входа у объекта состояния
    def on_enter(self, eventdata):
        eventdata.state.handle_on_enter(eventdata)

    #   при выходе из каждого состояния вызываем обработчик выхода у объекта состояния
    def on_exit(self, eventdata):
        eventdata.state.handle_on_exit(eventdata)

    #  обработчик перехода из состояния в состояние 
    # (сохраняем в модели данные, которые переходят из одного состояния в другое)
    def set_environment(self, eventdata):
        if 'data' in eventdata.kwargs:
            self.data = eventdata.kwargs['data']
        else:
            self.data = None    

    @property
    # возвращает список состояний
    def states(self):
        return self.states_list

    @property
    # возвращает список переходов
    def transitions(self):
        return self.transitions_list
