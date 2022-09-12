import random 
from pygame import Vector2

from TD.enemies.enemy import EnemyPathFollower
from TD.assetmanager import asset_manager


class EnemyT8(EnemyPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.frames = asset_manager.sprites["T8"]
        self.frame_index = random.randrange(0, len(self.frames))
        self.frame_duration = 30
        self.velocity = 0.25
        self.sprite_offset = Vector2(-32, -32)
        self.add_hitbox((0, 0, 40, 20), Vector2(-32, -12))
