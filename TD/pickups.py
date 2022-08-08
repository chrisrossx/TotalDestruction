import pygame
from blinker import signal

from TD.assetmanager import asset_manager
from TD.paths import PathFollowerOld
from TD.debuging import game_debugger
# from TD.bullets import Bullet
from TD.utils import fast_round_point


class PickupHeart:
    def __init__(self, pos):
        self.frames = asset_manager.sprites["powerup heart"]
        self.frame_index = 0
        self.frame_elapsed = 0
        self.frame_count = len(self.frames)
        self.pos = pos
        self.offset = [-32, -32]
        self.velocity = -0.1

        self.deleted = False

        self.hitboxs = [
            pygame.Rect(0, 0, 40, 20),
        ]
        self.hitbox_offsets = [
            [0, 20],
        ]

    def draw(self, elapsed, surface):
        self.frame_elapsed += elapsed
        if self.frame_elapsed >= 125:
            self.frame_elapsed = 0
            self.frame_index += 1
            if self.frame_index == self.frame_count:
                self.frame_index = 0
        

        x, y = fast_round_point(self.pos)
        surface.blit(self.frames[self.frame_index], (x+self.offset[0], y+self.offset[1]))

        if game_debugger.show_hitboxes:
            for i in range(len(self.hitboxs)):
                pygame.draw.rect(surface, (255,0,0), self.hitboxs[i], 1)

    def tick(self, elapsed):
        self.pos[0] += elapsed * self.velocity
        for i in range(len(self.hitboxs)):
            self.hitboxs[i].x = self.pos[0] + self.hitbox_offsets[i][0]
            self.hitboxs[i].y = self.pos[1] + self.hitbox_offsets[i][1]
        
        if self.pos[0] < 20:
            self.delete()

    def delete(self):
        self.deleted = True 
        signal("scene.delete_pickup").send(self)

    def on_end_of_path(self, sender):
        self.delete()

