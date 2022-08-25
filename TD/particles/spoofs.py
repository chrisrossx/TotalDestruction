import pygame

from TD.assetmanager import asset_manager
from TD.particles.particles import ParticleEntityFollower

class SpoofHitFollow(ParticleEntityFollower):
    def __init__(self, follow_entity, follow_offset):
        super().__init__(follow_entity, follow_offset)
        self.frames = asset_manager.sprites["Spoof Hit 001"]
        self.frame_duration = 1000/25
        self.sprite_offset = [-8, -8]
        self.frame_loop_end = 1
