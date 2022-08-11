import pygame 

from TD.config import SCREEN_SIZE
from TD.assetmanager import asset_manager
from TD.entity import EntityManager

class MenuScreen:
    def __init__(self) -> None:
        self.em = EntityManager()
        self.transitioning = False
        self.surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        self.font_s = asset_manager.fonts["Game 1 24"]
        self.font_m = asset_manager.fonts["Game 1 48"]
        self.font_l = asset_manager.fonts["Game 1 96"]

        self.render()

    def draw(self, elapsed):
        self.surface.fill((0,0,0,0))
        self.em.draw(elapsed, self.surface)

    def tick(self, elapsed):
        self.em.tick(elapsed)

    def render(self):
        pass

    def pressed(self, pressed, elapsed):
        pass

    def on_event(self, event, elapsed):
        pass

    def set_data(self, data):
        pass

    def activate(self):
        pass
    
    def deactivate(self):
        pass
