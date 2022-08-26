from enum import Enum
import random 

import pygame
from pygame import Vector2

from TD.assetmanager import asset_manager
from TD.debuging import game_debugger
# from TD.bullets import Bullet
from TD.utils import fast_round_point
from TD.entity import EntityVectorMovement, EntityType
from TD.config import SCREEN_SIZE, SKY_VELOCITY
from TD import current_scene

class PickupType(Enum):
    HEART = 0 
    COIN = 1

class PickupEntity(EntityVectorMovement):
    _screen_rect = pygame.Rect(-40 ,-40, SCREEN_SIZE.x+80, SCREEN_SIZE.y+80) # Delete Sprite if it goes off screen

    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.PICKUP
        self.pickup_type = None 
        self.velocity = 0.1
        self.pos = pos.copy()
        self.heading = Vector2(-1, 0)
        
        # self.delta_heading = delta 
        self.drop_heading = Vector2(random.uniform(-1, 1.0),random.uniform(-1, 1.0))
        self.drop_heading.normalize_ip()
        self.drop_velocity = random.uniform(0.2, 0.7)
        self.delta_elapsed = 0

        self.magnet_velocity = 0
        self.magnet_heading = Vector2(0,0)

    def pickedup(self):
        current_scene.player.pickedup(self)
        self.delete()

    def tick(self, elapsed):
        self.pos += self.magnet_heading * self.magnet_velocity * elapsed 

        self.delta_elapsed += elapsed
        
        drop_duration = 200
        if self.drop_heading and self.delta_elapsed < drop_duration:
            v = self.drop_velocity - ((self.drop_velocity - 0.1) * (self.delta_elapsed/drop_duration))
            self.pos += self.drop_heading * v * elapsed
            self.drop_velocity -= elapsed / 10000

        super().tick(elapsed)
        if not self._screen_rect.collidepoint(self.pos):
            self.delete()

    def set_magnet_force(self, heading, velocity):
        self.magnet_heading = heading
        self.magnet_velocity = velocity


class PickupHeart(PickupEntity):

    def __init__(self, pos):
        super().__init__(pos)
        self.pickup_type = PickupType.HEART
        self.frames = asset_manager.sprites["Pickup Heart"]
        self.frame_duration = 120
        self.sprite_offset = Vector2(-24, -24)
        self.add_hitbox((0,0,32,32), Vector2(-16, -16))


class PickupCoin(PickupEntity):

    def __init__(self, pos):
        super().__init__(pos)
        self.pickup_type = PickupType.COIN
        self.frames = asset_manager.sprites["Pickup Star"]
        self.frame_duration = 150
        self.sprite_offset = Vector2(-16, -16)
        self.add_hitbox((0,0,32,32), Vector2(-16, -16))
        self.frame_index = random.randrange(0, len(self.frames))

        current_scene.total_coins += 1

