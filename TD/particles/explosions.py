import pygame

from TD.assetmanager import asset_manager
from TD.debuging import game_debugger
# from TD.bullets import Bullet
from TD.entity import EntityVectorMovement, EntityType, Entity
from TD.particles.particles import ParticleEntityFollower, ParticleVectorMovement

class ExplosionMedium(ParticleVectorMovement):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = asset_manager.sprites["Explosion Medium"]
        self.frame_duration = 1000/15
        self.velocity = -0.1
        self.sprite_offset = [-64, -64]
        self.frame_loop_end = 1

class ExplosionSmall(ParticleVectorMovement):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = asset_manager.sprites["Explosion Small"]
        self.frame_duration = 1000/15
        self.velocity = -0.1
        self.sprite_offset = [-16, -16]
        self.frame_loop_end = 1

class ExplosionSmallFollow(ParticleEntityFollower):
    def __init__(self, follow_entity, follow_offset):
        super().__init__(follow_entity, follow_offset)
        self.frames = asset_manager.sprites["Explosion Small"]
        self.frame_duration = 1000/15
        # self.sprite_offset = [-16, -16]
        self.sprite_offset = [-32, -32]
        self.frame_loop_end = 1
