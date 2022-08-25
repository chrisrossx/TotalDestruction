from pygame import Vector2

from TD.enemies.enemy import EnemyPathFollower
from TD.assetmanager import asset_manager


class EnemyHX7(EnemyPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.frames = asset_manager.sprites["HX7"]
        self.frame_duration = 30    
        self.velocity = 0.15
        #TODO
        self.sprite_offset = Vector2(-22, -42)

        self.add_hitbox((0, 0, 70, 32), Vector2(-35, -28))
        self.add_hitbox((0, 0, 40, 15), Vector2(-20, 4))
        self.gun_points = [Vector2(-16, 20), Vector2(16, 20),]
