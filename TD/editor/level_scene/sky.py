import pygame

from TD.assetmanager import asset_manager

from TD.config import SCREEN_SIZE, SKY_VELOCITY
from TD.editor.globals import scene_level

class Sky:

    def draw(self, elapsed, surface, time):
        pixels = time * SKY_VELOCITY
        while pixels > 1024:
            pixels -= 1024
        area = pygame.Rect(pixels,0,1024-pixels,600)
        surface.blit(asset_manager.sprites["sky layered"], (100, 100), area)

        area = pygame.Rect(0,0,pixels,600)
        surface.blit(asset_manager.sprites["sky layered"], (100+(1024-pixels), 100), area)

        # pygame.draw.circle(surface, (255,255,0), (100+(1024-pixels), 100), 5, 1)
