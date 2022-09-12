from pygame import Vector2
import random 

from TD.enemies.enemy import EnemyPathFollower
from TD.assetmanager import asset_manager


class EnemyCX5B(EnemyPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.frames = asset_manager.sprites["CX5B"]
        self.frame_duration = 25    
        self.frame_index = random.randrange(0, len(self.frames))
        self.velocity = 0.25
        self.sprite_offset = Vector2(-32, -32)
        self.add_hitbox((0, 0, 55, 18), Vector2(-32, -12))
        self.gun_points = [Vector2(-25, -4),]


class EnemyCX5B_SLOW(EnemyPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.frames = asset_manager.sprites["CX5B"]
        self.frame_index = random.randrange(0, len(self.frames))
        self.frame_duration = 25    
        self.velocity = 0.2
        self.sprite_offset = Vector2(-32, -32)
        self.add_hitbox((0, 0, 55, 18), Vector2(-32, -12))
        self.gun_points = [Vector2(-25, -4),]


# class EnemyCX5B_FAST(EnemyPathFollower):
#     def __init__(self, path_index):
#         super().__init__(path_index)
#         self.frames = asset_manager.sprites["CX5B"]
#         self.frame_duration = 25    
#         self.velocity =0.25 + 0.125
#         self.sprite_offset = Vector2(-32, -32)
#         self.add_hitbox((0, 0, 55, 18), Vector2(-32, -12))
#         self.gun_points = [Vector2(-25, -4),]

