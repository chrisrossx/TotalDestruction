from pygame import Vector2
import pygame

from TD.assetmanager import asset_manager

from TD.config import SCREEN_SIZE, SKY_VELOCITY
from TD.editor.globals import scene_level
from TD.editor.globals import current_scene

class Sky:

    def draw(self, elapsed, surface, time):
        if not current_scene.hide_sky:
            pixels = time * SKY_VELOCITY
            while pixels > 1024:
                pixels -= 1024
            area = pygame.Rect(pixels,0,1024-pixels,600)
            surface.blit(asset_manager.sprites["sky layered"], (100, 100), area)

            area = pygame.Rect(0,0,pixels,600)
            surface.blit(asset_manager.sprites["sky layered"], (100+(1024-pixels), 100), area)

            # pygame.draw.circle(surface, (255,255,0), (100+(1024-pixels), 100), 5, 1)
        pixels = time * SKY_VELOCITY
        while pixels > 150:
            pixels -= 150
        if current_scene.hide_sky:
            c = (80,60,60)
        else:
            c = (143, 137, 99)
        for y in range(100+150, 700, 150):
            p0 = Vector2(100, y)
            p1 = Vector2(1124, y)
            pygame.draw.line(surface, c, p0, p1, 1)
        for x in range(100+150, 1124+150, 150):
            if (x - pixels) <= 1124:
                p0 = Vector2(x-pixels, 100)
                p1 = Vector2(x-pixels, 700)
                pygame.draw.line(surface, c, p0, p1, 1)

