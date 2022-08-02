from enum import Enum 

class State(Enum):
    NOT_STARTED = 0
    STARTING = 1
    PLAYING = 2
    ENDING = 3
    ENDED = 4
    PAUSED = 10
