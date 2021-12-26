from enum import Enum

class Direction(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    

class Side(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Corner(Enum):
    NONE = 0
    LEFT_UPPER = 1
    RIGHT_UPPER = 2
    LEFT_BOTTOM = 3
    RIGHT_BOTTOM = 4

