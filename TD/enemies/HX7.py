import random 
from pygame import Vector2

from TD.enemies.enemy import EnemyPathFollower
from TD.assetmanager import asset_manager


class EnemyHX7(EnemyPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.frames = asset_manager.sprites["HX7"]
        self.frame_index = random.randrange(0, len(self.frames))
        self.frame_duration = 30    
        self.velocity = 0.15 
        #TODO
        self.sprite_offset = Vector2(-22, -42)
        self.health = 5

        self.add_hitbox((0, 0, 55, 20), Vector2(-20, -10))
        self.gun_points = [Vector2(-16, 10),]



class EnemyHX7_L4_FAST(EnemyPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.frames = asset_manager.sprites["HX7"]
        self.frame_index = random.randrange(0, len(self.frames))
        self.frame_duration = 30    
        self.velocity = 0.15 
        #TODO
        self.sprite_offset = Vector2(-22, -42)
        self.health = 2

        self.add_hitbox((0, 0, 55, 20), Vector2(-20, -10))
        self.gun_points = [Vector2(-16, 10),]
