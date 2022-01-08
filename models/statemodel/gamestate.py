from collections import defaultdict

from transitions import State

from utils.resourcemanager import ResourceManager

# общий предок для всех состояний (игровых экранов)
# реализует функциональность по умолчанию
class GameState(State):
    # инициализируется экземпляром игры, модели состояний и именем экрана
    def __init__(self, game, model, name):
        super().__init__(name, ignore_invalid_triggers=True, on_enter=['on_enter'], on_exit=['on_exit'])
        self.statemodel = model
        self.game = game
    
    def initialize(self):
        self.init_resources()
        self.init_objects()
        self.init_handlers()

        self.create_objects()
        self.create_handlers()

    # обработчик входа в состояние
    def handle_on_enter(self, eventdata):
        self.initialize()

    # обработчик выхода из состояния
    def handle_on_exit(self, eventdata):
        pass

    # инициализация списка объектов данного состояния
    def init_objects(self):
        self.objects = []

    # инициализация списков обрабочиков событий данного состояния
    def init_handlers(self):
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.dispatcher = None
        self.bomb_handlers = defaultdict(list)
        self.exit_handlers = defaultdict(list)
        self.monster_handlers = defaultdict(list)
        self.treasure_handlers = defaultdict(list)
        

    def init_resources(self):
        self.resources = ResourceManager()[self.name.lower()]
