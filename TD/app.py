import pygame

from .assetmanager import asset_manager
from .debuging import game_debugger
from .scenes.main_menu.main_menu import MainMenu
from .config import SCREEN_SIZE
from .scenes.levels.level_001 import Level_001
from .mixer import Mixer
from .savedata import SaveData

from .globals import current_app, current_scene


class App:

    def __init__(self):
        current_app.__wrapped__ = self
        # self.size = (640, 480)
        self.size = SCREEN_SIZE

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        # self.font = pygame.font.SysFont(None, 24)
        self.save_data = SaveData()
        asset_manager.load()
        self.mixer = Mixer()

        game_debugger.load()
        self.running = True

    def exit(self):
        print("Thank you, come again!")
        self.running = False

    def change_scene(self, data):
        self.scene.on_delete()
        del self.scene
        if data["scene"] == "play":
            self._set_scene(Level_001())
            self.scene.background.offset = data["sky_offset"]
        if data["scene"] == "main_menu":
            if "return_from_level" in data:
                self._set_scene(MainMenu(return_from_level=data["return_from_level"], level_data=data["level_data"]))
            else:
                self._set_scene(MainMenu())
            self.scene.background.offset = data["sky_offset"]

    def _set_scene(self, scene):
        self.scene = scene
        current_scene.__wrapped__ = self.scene 
        self.scene.on_start()

    def run(self):

        self._set_scene(Level_001())
        # self._set_scene(MainMenu())
        
        self.clock.tick()
        self.running = True

        while 1:
            game_debugger.timeit_start("app.loop")

            elapsed = self.clock.tick()

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
                game_debugger.timeit_start("app.scene.tick")
                self.scene.tick(elapsed)
                game_debugger.timeit_end("app.scene.tick")
                game_debugger.timeit_start("app.debugger.tick")
                game_debugger.tick(elapsed)
                game_debugger.timeit_end("app.debugger.tick")
            
                game_debugger.timeit_start("app.scene.draw")
                self.scene.draw(elapsed)
                game_debugger.timeit_end("app.scene.draw")
                game_debugger.timeit_start("app.debugger.draw")
                game_debugger.draw(elapsed)
                game_debugger.timeit_end("app.debugger.draw")

                game_debugger.timeit_start("app.flip")
                self.screen.blit(self.scene.surface, (0,0))
                self.screen.blit(game_debugger.surface, (10,40))
                pygame.display.flip()
                game_debugger.timeit_end("app.flip")

            else:
                break

            game_debugger.timeit_end("app.loop")

if __name__ == "__main__":
    app = App()
    app.run()
