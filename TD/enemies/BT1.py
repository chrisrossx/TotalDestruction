import random
from pygame import Vector2

from TD.enemies.enemy import EnemyPathFollower
from TD.assetmanager import asset_manager


class EnemyBT1(EnemyPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.frames = asset_manager.sprites["BT1"]
        self.frame_index = random.randrange(0, len(self.frames))
        self.frame_duration = 80    
        self.velocity = 0.05
        self.sprite_offset = Vector2(-32, -32)

        self.add_hitbox((0, 0, 32, 32), Vector2(-16, -24))
        self.add_hitbox((0, 0, 20, 15), Vector2(-10, 8))
        self.gun_points = [Vector2(0, 20),]

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)

