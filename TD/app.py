import pygame
from blinker import signal

from .assetmanager import asset_manager
from .debuging import debug_display
from .scenes import NeverEndingLevel


class App:

    def __init__(self):
        # self.size = (640, 480)
        self.size = (1024, 600)

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 24)
        asset_manager.load()

        debug_display.load()

    def run(self):

        scene = NeverEndingLevel(self.size)
        self.clock.tick()
        running = True

        while running:
            elapsed = self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                scene.on_event(event, elapsed)
                debug_display.on_event(event, elapsed)
            
            pressed = pygame.key.get_pressed()
            scene.pressed(pressed, elapsed)

            if running:
                scene.tick(elapsed)
                debug_display.tick(elapsed)
            
                scene.draw(elapsed)
                debug_display.draw(elapsed)
                
                self.screen.blit(scene.surface, (0,0))
                self.screen.blit(debug_display.surface, (10,10))
                pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
