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

class PickupEntity(EntityVectorMovement):
    _screen_rect = pygame.Rect(-40 ,-40, SCREEN_SIZE.x+80, SCREEN_SIZE.y+80) # Delete Sprite if it goes off screen

    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.PICKUP
        self.velocity = 0.0001
        self.pos = pos.copy()
        self.heading = Vector2(-1, 0)

        self.magnet_velocity = 0
        self.magnet_heading = Vector2(0,0)

    def pickedup(self):
        self.delete()

    def tick(self, elapsed):
        self.pos += self.heading * self.velocity * elapsed 
        self.pos += self.magnet_heading * self.magnet_velocity * elapsed 
        super().tick(elapsed)
        if not self._screen_rect.collidepoint(self.pos):
            self.delete()


    def set_magnet_force(self, heading, velocity):
        self.magnet_heading = heading
        self.magnet_velocity = velocity


class PickupHeart(PickupEntity):

    def __init__(self, pos):
        super().__init__(pos)
        self.frames = asset_manager.sprites["Pickup Heart"]
        self.frame_duration = 120
        self.sprite_offset = Vector2(-24, -24)
        self.add_hitbox((0,0,32,32), Vector2(-16, -16))



class PickupStar(PickupEntity):

    def __init__(self, pos):
        super().__init__(pos)
        self.frames = asset_manager.sprites["Pickup Star"]
        self.frame_duration = 150
        self.sprite_offset = Vector2(-16, -16)
        self.add_hitbox((0,0,32,32), Vector2(-16, -16))
