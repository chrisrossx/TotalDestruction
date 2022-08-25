import random
import pygame

from TD.assetmanager import asset_manager
from TD.debuging import game_debugger
# from TD.bullets import Bullet
from TD.entity import EntityVectorMovement, EntityType, Entity
from TD.particles.particles import ParticleEntityFollower, ParticleVectorMovement

class MissileSmoke(ParticleVectorMovement):
    def __init__(self, pos):
        super().__init__(pos)
        i = random.randrange(0, len(asset_manager.sprites["Missile Smoke 004"]))
        i = 0
        self.frames = [asset_manager.sprites["Missile Smoke 004"][i].copy(), ]

        self.frame_duration = 1000/15
        self.velocity = -0.0
        self.sprite_offset = [-8, -8]
        self.total_elapsed = 0

    def tick(self, elapsed):
        super().tick(elapsed)
        self.total_elapsed += elapsed
        fs = 350
        fd = 500
        if self.total_elapsed >= fs:
            l = (self.total_elapsed - fs) / fd
            l = 255 - (l * 255)
            self.surface.set_alpha(l)
        if self.total_elapsed >= fs + fd:
            self.delete()
