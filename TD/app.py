import pygame

from TD.scenes.test_scene import TestScene

from .assetmanager import asset_manager
from .debuging import game_debugger
from .scenes.main_menu.main_menu import MainMenu
from .config import SCREEN_SIZE
# from .scenes.levels.level_000 import Level_000
# from .scenes.levels.level_001 import Level_001
from .scenes.level.level import Level 
from .mixer import Mixer
from .savedata import SaveData

from .globals import current_app, current_scene


class App:
    """
    Total Destruction Main Game Loop
    """

    def __init__(self, debug_filename=None, debug_start=None):
        current_app.__wrapped__ = self
        self.size = SCREEN_SIZE
        self.debug_filename = debug_filename
        self.debug_start = debug_start

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.save_data = SaveData()
        asset_manager.load()
        self.mixer = Mixer()

        game_debugger.load()
        self.running = True

    def exit(self):
        """
        Stop the main game loop
        """
        self.running = False

    def change_scene(self, data):
        """
        Transition to a new scene. 
        data
        """
        self.scene.on_delete()
        del self.scene
        if data["scene"] == "play":
            if data["level"] == 0:
                self._set_scene(Level_000())
            if data["level"] == 1:
                self._set_scene(Level_001())
            self.scene.background.offset = data["sky_offset"]
        if data["scene"] == "main_menu":
            if "return_from_level" in data:
                self._set_scene(MainMenu(return_from_level=data["return_from_level"], level_data=data["level_data"]))
            else:
                self._set_scene(MainMenu())
            self.scene.background.offset = data["sky_offset"]

    def _set_scene(self, scene):
        """
        Set the scene and start it. ALso set the singleton proxy
        """
        self.scene = scene
        current_scene.__wrapped__ = self.scene 
        self.scene.on_start()

    def run(self):

        if self.debug_filename:
            print("DEBUG LEVEL FILENAME:", self.debug_filename)
            self.save_data.index = -1
            self._set_scene(Level(-1, self.debug_filename, debug_start=self.debug_start))
        else:
            pass 
            self.save_data.index = 0
            self._set_scene(MainMenu())
        # self._set_scene(TestScene())
        
        self.clock.tick()
        self.running = True

        while 1:
            game_debugger.timeit_start("app.loop")
            elapsed = self.clock.tick()
            elapsed = elapsed * game_debugger.speed

            # --------------------
            # Event Handling 
            game_debugger.timeit_start("app.on_event")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                self.scene.on_event(event, elapsed)
                game_debugger.on_event(event, elapsed)
            game_debugger.timeit_end("app.on_event")
            
            game_debugger.timeit_start("app.pressed")
            pressed = pygame.key.get_pressed()
            self.scene.pressed(pressed, elapsed)
            game_debugger.timeit_end("app.pressed")

            if self.running:
                # --------------------
                # Tick            
                game_debugger.timeit_start("app.scene.tick")
                # print("----")
                self.scene.tick(elapsed)
                game_debugger.timeit_end("app.scene.tick")
                game_debugger.timeit_start("app.debugger.tick")
                game_debugger.tick(elapsed)
                game_debugger.timeit_end("app.debugger.tick")

                # --------------------
                # Draw            
                game_debugger.timeit_start("app.scene.draw")
                self.scene.draw(elapsed)
                game_debugger.timeit_end("app.scene.draw")
                game_debugger.timeit_start("app.debugger.draw")
                game_debugger.draw(elapsed)
                game_debugger.timeit_end("app.debugger.draw")

                # --------------------
                # BLit to Screen     
                game_debugger.timeit_start("app.flip")
                self.screen.blit(self.scene.surface, (0,0))
                self.screen.blit(game_debugger.surface, (10,40))
                pygame.display.flip()
                game_debugger.timeit_end("app.flip")

            else:
                break

            game_debugger.timeit_end("app.loop")
        
        #Be Friendly 
        print("Thank you, come again!")
