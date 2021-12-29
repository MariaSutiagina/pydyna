from collections import defaultdict

from transitions import State

class GameState(State):
    def __init__(self, model, name):
        super().__init__(name, ignore_invalid_triggers=True)
        self.statemodel = model
        self.init_objects()
        self.init_handlers()

    def init_objects(self):
        self.objects = []

    def init_handlers(self):
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

        

        