from enum import Enum 
# import weakref

class LevelState(Enum):
    # NOT_STARTED = 0
    STARTING = 0
    PLAYING = 1
    DEAD = 2
    WON = 3
    # ENDING = 3
    # ENDED = 4
    # PAUSED = 10

class LevelStateMachine:
    def __init__(self, level) -> None:
        self.step = 0
        self.step_elapsed = 0
        self.total_elapsed = 0
        self.level = level 

    @property
    def em(self):
        return self.level.em

    @property
    def player(self):
        return self.level.player

    @property
    def hud(self):
        return self.level.hud

    def start(self):
        self._set_tick_step(0)
        self.step_elapsed = 0 
        self.total_elapsed = 0

    def stop(self):
        pass

    def next_step(self):
        self.step_elapsed = 0
        self._set_tick_step(self.step + 1)

    def _set_tick_step(self, step):
        self.step = step 
        name = "tick_step_{:>03d}".format(self.step)
        if hasattr(self, name):
            self.tick_step = getattr(self, name)
        else:
            self.tick_step = lambda elapsed: None

    def tick(self, elapsed):
        self.step_elapsed += elapsed
        self.total_elapsed += elapsed
        self.tick_step(elapsed)

    def on_event(self, event, elapsed):
        pass

    def pressed(self, pressed, elapsed):
        pass

