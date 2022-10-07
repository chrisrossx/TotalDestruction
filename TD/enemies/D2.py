import random 

from pygame import Vector2

from TD.enemies.enemy import EnemyPathFollower
from TD.assetmanager import asset_manager


class EnemyD2(EnemyPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.frames = asset_manager.sprites["D2"]
        self.frame_index = random.randrange(0, len(self.frames))

        self.frame_duration = 30    
        self.velocity = 0.08
        self.sprite_offset = Vector2(-59, -32)
        self.health = 7

        self.add_hitbox((0, 0, 70, 32), Vector2(-35, -24))
        self.add_hitbox((0, 0, 40, 15), Vector2(-20, 10))
        self.gun_points = [Vector2(-16, 25), Vector2(16, 25),]
