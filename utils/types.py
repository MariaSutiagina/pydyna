from enum import Enum, unique

@unique
class Direction(int,Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    

@unique
class Side(int, Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Corner(int, Enum):
    NONE = 0
    LEFT_UPPER = 1
    RIGHT_UPPER = 2
    LEFT_BOTTOM = 3
    RIGHT_BOTTOM = 4

class BombAction(int, Enum):
    START_EXPLOSION = 1,
    END_EXPLOSION = 2

class ExitAction(int, Enum):
    SHOW = 1
    ACTIVE = 2
    OPEN = 3
    REPLAY = 4

class MonsterAction(int, Enum):
    CREATE_EXTRA = 1

class TreasureAction(int, Enum):
    SHOW = 1
    OPEN = 2
    HIDE = 3
    INACTIVE = 4
