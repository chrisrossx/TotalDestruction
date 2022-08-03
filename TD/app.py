import pygame
from blinker import signal

from .assetmanager import asset_manager
from .debuging import game_debugger
from .scenes import NeverEndingLevel, StartScene


class App:

    def __init__(self):
        # self.size = (640, 480)
        self.size = (1024, 600)

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 24)
        asset_manager.load()

        sig = signal("game.change_scene")
        sig.connect(self.on_change_scene)

        game_debugger.load()

    def on_change_scene(self, data):
        if data["scene"] == "play":
            self.scene = NeverEndingLevel(self.size)
            self.scene.sky.offset = data["sky_offset"]

    def run(self):

        self.scene = NeverEndingLevel(self.size)
        # self.scene = StartScene(self.size)
        self.clock.tick()
        running = True

        while running:
            elapsed = self.clock.tick()
            signal("on_d").send(elapsed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                self.scene.on_event(event, elapsed)
                game_debugger.on_event(event, elapsed)
            
            pressed = pygame.key.get_pressed()
            self.scene.pressed(pressed, elapsed)

            if running:
                self.scene.tick(elapsed)
                game_debugger.tick(elapsed)
            
                self.scene.draw(elapsed)
                game_debugger.draw(elapsed)
                
                self.screen.blit(self.scene.surface, (0,0))
                self.screen.blit(game_debugger.surface, (10,10))
                pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
