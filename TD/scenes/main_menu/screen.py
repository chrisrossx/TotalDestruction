import pygame 

from TD.config import SCREEN_SIZE
from TD.assetmanager import asset_manager
from TD.entity import EntityManager, EntityType

class MenuScreen:
    def __init__(self) -> None:
        self.em = EntityManager()
        self.transitioning = False
        self.surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)


        self.font_xs = asset_manager.fonts["xs"]
        self.font_s = asset_manager.fonts["sm"]
        self.font_m = asset_manager.fonts["md"]
        self.font_l = asset_manager.fonts["lg"]

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
        self.em.on_event(event, elapsed, EntityType.GUI)

    def set_data(self, data):
        pass

    def activate(self):
        pass
    
    def deactivate(self):
        pass
