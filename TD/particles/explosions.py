import pygame
from blinker import signal

from TD.assetmanager import asset_manager
from TD.paths import PathFollowerOld
from TD.debuging import game_debugger
# from TD.bullets import Bullet
from TD.entity import EntityVectorMovement, EntityType


class ExplosionMedium002(EntityVectorMovement):
    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.PARTICLE
        self.frames = asset_manager.sprites["Explosion Medium 002"]
        self.frame_duration = 1000/15
        self.pos = pos.copy()
        self.velocity = -0.1
        self.sprite_offset = [-64, -64]
        self.frame_loop_end = 1

class ExplosionMedium(EntityVectorMovement):
    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.PARTICLE
        self.frames = asset_manager.sprites["Explosion Medium"]
        self.frame_duration = 75
        self.pos = pos.copy()
        self.velocity = -0.1
        self.sprite_offset = [-64, -64]
        self.frame_loop_end = 1
