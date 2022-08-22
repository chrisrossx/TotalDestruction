import pygame
from blinker import signal

from .assetmanager import asset_manager
from .debuging import game_debugger
from .scenes.main_menu import MainMenu
from .config import SCREEN_SIZE
from .savedata import save_data
from .scenes.levels.level_001 import Level_001
from .mixer import Mixer

class App:

    def __init__(self):
        # self.size = (640, 480)
        self.size = SCREEN_SIZE

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 24)
        asset_manager.load()
        self.mixer = Mixer()

        signal("game.change_scene").connect(self.on_change_scene)
        signal("game.exit").connect(self.on_exit)

        game_debugger.load()
        self.running = True

    def on_exit(self, sender):
        self.running = False

    def on_change_scene(self, data):
        self.scene.delete()
        if data["scene"] == "play":
            self.scene = Level_001()
            self.scene.background.offset = data["sky_offset"]
        if data["scene"] == "main_menu":
            if "return_to_level_select" in data:
                self.scene = MainMenu(return_to_level_select=data["return_to_level_select"])
            else:
                self.scene = MainMenu()
            self.scene.background.offset = data["sky_offset"]

    def run(self):

        # self.scene = MainMenu()
        self.scene = Level_001()
        
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
