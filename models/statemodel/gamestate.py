from collections import defaultdict

from transitions import State

class GameState(State):
    def __init__(self, game, model, name):
        super().__init__(name, ignore_invalid_triggers=True, on_enter=['on_enter'], on_exit=['on_exit'])
        self.statemodel = model
        self.game = game
    
    def handle_on_enter(self, eventdata):
        pass

    def handle_on_exit(self, eventdata):
        pass

    def init_objects(self):
        self.objects = []

    def init_handlers(self):
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.dispatcher = None
        self.bomb_handlers = defaultdict(list)
        self.exit_handlers = defaultdict(list)
        self.monster_handlers = defaultdict(list)
        self.treasure_handlers = defaultdict(list)
        

        