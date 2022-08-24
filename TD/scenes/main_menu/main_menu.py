from pygame import Vector2

from TD.config import SCREEN_RECT, SCREEN_SIZE
from TD.scenes.scene import Scene 

# Scenes
from .confirm_delete import ConfirmDeletePlayer
from .enter_name import EnterPlayerName
from .start import StartScreen
from .select_player import SelectPlayerScreen
from .level_select import StartLevelScreen, LevelSelectScreen
from .level_return import LevelScoreScreen, ReturnLevelScreen
from .confirm_exit import ConfirmExit
from .credits import CreditScreen
from TD.debuging import game_debugger

from TD.globals import current_app

class MainMenu(Scene):
    def __init__(self, return_from_level=False, level_data=None):

        super().__init__()

        self.screen = None

        self.transitioning = False 
        self.transition_screen = None
        self.transition_startpos = None
        self.transition_d = 0.0
        self.transition_elapsed = 0

        self.menu_screens = {
            "select_player": SelectPlayerScreen(),
            "start_screen": StartScreen(),
            "confirm_delete_player": ConfirmDeletePlayer(),
            "enter_player_name": EnterPlayerName(),
            "level_select": LevelSelectScreen(),
            "level_return": ReturnLevelScreen(),
            "level_score": LevelScoreScreen(),
            "start_level": StartLevelScreen(),
            "confirm_exit": ConfirmExit(),
            "credits_screen": CreditScreen(),
        }

        #Initial Screen
        if return_from_level:
            if level_data["condition"] == "exit":
                self.screen = self.menu_screens["level_select"]
                self.screen.set_data(level_data)
            else:
                self.screen = self.menu_screens["level_return"]
                self.screen.set_data(level_data)
        else:
            self.screen = self.menu_screens["start_screen"]
        self.screen.pos = Vector2(0,0)

        current_app.mixer.play_music("menu")
        game_debugger.clear_lines()
    
    def on_start(self):
        self.screen.activate()

    def play_level(self, data):
        current_app.change_scene({"scene":"play", "level": data["level"], "sky_offset": self.background.offset})

    def start_transition(self, screen_name, direction, data=None):
        self.transition_screen = self.menu_screens[screen_name]
        self.transition_screen.set_data(data)

        if direction == "right":
            self.transition_startpos = Vector2(SCREEN_SIZE[0], 0)
        elif direction == "left":
            self.transition_startpos = Vector2(-SCREEN_SIZE[0], 0)
        elif direction == "top":
            self.transition_startpos = Vector2(0, -SCREEN_SIZE[1])
        elif direction == "bottom":
            self.transition_startpos = Vector2(0, SCREEN_SIZE[1])

        self.transition_endpos = Vector2(0,0)
        self.transition_screen.pos = self.transition_startpos.copy()
        self.transitioning = True 
        self.screen.transitioning = True
        self.transition_screen.transitioning = True 

    def end_transition(self):
        self.screen.transitioning = False
        self.screen.deactivate()
        self.transition_d = 0.0
        self.transitioning = False
        self.screen = self.transition_screen
        self.screen.transitioning = False
        self.screen.pos = Vector2(0,0)
        self.screen.activate()

    def draw(self, elapsed):
        super().draw(elapsed)
        self.screen.draw(elapsed)
        self.surface.blit(self.screen.surface, self.screen.pos)

        if self.transitioning:
            self.transition_screen.draw(elapsed)
            self.surface.blit(self.transition_screen.surface, self.transition_screen.pos)

    def tick(self, elapsed):
        super().tick(elapsed)
    
        self.screen.tick(elapsed)

        if self.transitioning:
            self.transition_screen.tick(elapsed)
            
            self.transition_d += 0.002 * elapsed
            if self.transition_d > 1:
                self.transition_d = 1.0
            p = self.transition_startpos.lerp(self.transition_endpos, self.transition_d)
            self.transition_screen.pos = p
            self.screen.pos = p - self.transition_startpos 
            if self.transition_d == 1.0:
                self.end_transition()

    def on_event(self, event, elapsed):
        super().on_event(event, elapsed)
        self.screen.on_event(event, elapsed)
    
    def pressed(self, pressed, elapsed):
        super().pressed(pressed, elapsed)
