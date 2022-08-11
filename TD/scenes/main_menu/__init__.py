import pygame 
from pygame import Vector2
from blinker import signal 

from TD.config import SCREEN_RECT, SCREEN_SIZE
from TD import gui
from TD.scenes.scene import Scene 

from .confirm_delete import ConfirmDeletePlayer
from .enter_name import EnterPlayerName
from .start import StartScreen
from .select_player import SelectPlayerScreen
from .level_select import StartLevelScreen, LevelSelectScreen

class MainMenu(Scene):
    def __init__(self):

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
            "start_level": StartLevelScreen(),
        }

        signal("menu_screen.start_transition").connect(self.start_transition)
        signal("scene.play_level").connect(self.play_level)
        
        #Initial Screen
        self.screen = self.menu_screens["start_screen"]
        self.screen = self.menu_screens["select_player"]
        self.screen.activate()
        self.screen.pos = Vector2(0,0)

    def play_level(self, data):
        #
        #self.background.offset
        signal("game.change_scene").send({"scene":"play", "level": data["level"], "sky_offset": self.background.offset})

    def start_transition(self, sender, screen_name, direction, data=None):
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
