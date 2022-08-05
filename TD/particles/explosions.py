import pygame
from blinker import signal

from TD.assetmanager import asset_manager
from TD.paths import PathFollowerOld
from TD.debuging import game_debugger
# from TD.bullets import Bullet
from TD.utils import fast_round_point


class ExplosionMedium:
    def __init__(self, pos):
        self.frames = asset_manager.sprites["Explosion Medium"]
        self.frame_index = 0
        self.frame_elapsed = 0
        self.frame_count = len(self.frames)
        self.frame_duration = 75
        self.pos = pos
        self.velocity = -0.1
        self.total_elapsed = 0.0

        self.deleted = False

        self.offset = [-32, -32]

    def draw(self, elapsed, surface):
        self.frame_elapsed += elapsed
        if self.frame_elapsed >= self.frame_duration:
            self.frame_elapsed = 0
            self.frame_index += 1
            if self.frame_duration != 50 and self.frame_index > 2:
                self.frame_duration=50
            if self.frame_index == self.frame_count:
                self.frame_index = 2
        
        x, y = fast_round_point(self.pos)
        surface.blit(self.frames[self.frame_index], (x+self.offset[0], y+self.offset[1]))

    def tick(self, elapsed):
        self.total_elapsed += elapsed

        self.pos[0] += elapsed * self.velocity
       
        if self.total_elapsed > (75*6)+(55*0):
            self.delete()

        if self.pos[0] < 20:
            self.delete()

    def delete(self):
        self.deleted = True 
        signal("scene.delete_particle").send(self)

    def on_end_of_path(self, sender):
        self.delete()

