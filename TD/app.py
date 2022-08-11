import pygame
from blinker import signal

from .assetmanager import asset_manager
from .debuging import game_debugger
from .scenes import NeverEndingLevel, StartScene
from .scenes.main_menu import MainMenu
from .config import SCREEN_SIZE
from .savedata import save_data


class App:

    def __init__(self):
        # self.size = (640, 480)
        self.size = SCREEN_SIZE

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 24)
        asset_manager.load()

        sig = signal("game.change_scene")
        sig.connect(self.on_change_scene)
        signal("game.exit").connect(self.on_exit)

        game_debugger.load()
        self.running = True

    def on_exit(self, sender):
        self.running = False

    def on_change_scene(self, data):
        if data["scene"] == "start":
            self.scene = StartScene(SCREEN_SIZE)
            self.scene.sky.offset = data["sky_offset"]
        if data["scene"] == "play":
            self.scene = NeverEndingLevel()
            self.scene.background.offset = data["sky_offset"]
        if data["scene"] == "select_player":
            self.scene = MainMenu()
            self.scene.background.offset = data["sky_offset"]

    def run(self):

        # self.scene = NeverEndingLevel()
        self.scene = MainMenu()
        # self.scene = StartScene(SCREEN_SIZE)
        self.clock.tick()
        self.running = True

        while 1:
            elapsed = self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                self.scene.on_event(event, elapsed)
                game_debugger.on_event(event, elapsed)
            
            pressed = pygame.key.get_pressed()
            self.scene.pressed(pressed, elapsed)

            if self.running:
                self.scene.tick(elapsed)
                game_debugger.tick(elapsed)
            
                self.scene.draw(elapsed)
                game_debugger.draw(elapsed)
                
                self.screen.blit(self.scene.surface, (0,0))
                self.screen.blit(game_debugger.surface, (10,10))
                pygame.display.flip()
            else:
                break


if __name__ == "__main__":
    app = App()
    app.run()
