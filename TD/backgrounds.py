import math 

from blinker import signal 
import pygame 

from TD.assetmanager import asset_manager
from TD.debuging import game_debugger


class Sky:
    def __init__(self, size, velocity=[-0.1, 0.0]):
        """
        Background Object, Create Parallax Scrolling Clouds
        """
        self.size = size

        self.sky = asset_manager.sprites["sky layered"]
        self.rect = self.sky.get_rect()
        self.offset = [0, 0]
        self.velocity = velocity

    def draw(self, elapsed, surface):
        if game_debugger.show_sky:
            x_count = math.ceil((self.size[0] - self.offset[0]) / self.rect.w)
            y_count = math.ceil((self.size[1] - self.offset[1]) / self.rect.h)
            for x in range(x_count):
                for y in range(y_count):
                    x_px = (x * self.rect.w) + self.offset[0]
                    y_px = (y * self.rect.h) + self.offset[1]
                    surface.blit(self.sky, (x_px, y_px))
        else:
            surface.fill((0,0,0))

    def tick(self, elapsed):
        for i in range(2):
            self.offset[i] += elapsed * self.velocity[i]
            if self.offset[i] > 0:
                self.offset[i] -= self.rect[i+2]
            if self.offset[i] < -self.rect[i+2]:
                self.offset[i] += self.rect[i+2]
