import pygame
from pygame import Vector2
from blinker import signal

from TD.assetmanager import asset_manager
from TD.paths import PathFollowerOld
from TD.debuging import game_debugger
# from TD.bullets import Bullet
from TD.utils import fast_round_point
from TD.entity import EntityVectorMovement, EntityType
from TD.config import SCREEN_SIZE, SKY_VELOCITY


class PickupHeart(EntityVectorMovement):

    _screen_rect = pygame.Rect(-40 ,-40, SCREEN_SIZE.x+80, SCREEN_SIZE.y+80) # Delete Sprite if it goes off screen

    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.PICKUP
        self.frames = asset_manager.sprites["Pickup Heart"]
        self.frame_duration = 120
        self.velocity = 0.1
        self.pos = pos.copy()
        self.heading = Vector2(-1, 0)
        self.add_hitbox((0,0,32,32), Vector2(16, 16))

    def pickedup(self):
        self.delete()


class PickupStar(EntityVectorMovement):

    _screen_rect = pygame.Rect(-40 ,-40, SCREEN_SIZE.x+80, SCREEN_SIZE.y+80) # Delete Sprite if it goes off screen

    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.PICKUP
        self.frames = asset_manager.sprites["Pickup Star"]
        self.velocity = 0.1
        self.pos = pos.copy()
        self.heading = Vector2(-1, 0)
        self.add_hitbox((0,0,32,32), Vector2(16, 16))

    def pickedup(self):
        self.delete()
