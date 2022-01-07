from utils.constants import TREASURE_TILE_TYPE, TREASURE_TIMEOUT
from utils.singleton import MetaSingleton

class TreasureFactory(metaclass=MetaSingleton):
    def __init__(self):
        self.config = {
            1: {'title': 'life', 'life': 1},
            2: {'title': 'speed', 'speed': 1},
            3: {'title': 'bomb', 'bomb': 1},
            4: {'title': 'explosion', 'explosion': 1},
            5: {'title': 'fly', 'fly': 1, 'timeout': TREASURE_TIMEOUT},
            6: {'title': 'remote', 'remote': 1, 'timeout': TREASURE_TIMEOUT},
            7: {'title': 'killer', 'killer': 1, 'timeout': TREASURE_TIMEOUT},
            8: {'title': 'can-exit', 'can-exit': 1},
            9: {'title': 'decspeed', 'decspeed': 1},
        }

    def create_treasure_state(self, treasuretype):
        return self.config[treasuretype - TREASURE_TILE_TYPE + 1].copy()


    def __getitem__(self, key):
        return self.create_treasure_state(key)
