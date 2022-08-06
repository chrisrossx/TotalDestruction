import pygame
from blinker import signal

from TD.assetmanager import asset_manager
from TD.paths import PathFollowerOld
from TD.debuging import game_debugger
from TD.bullets import Bullet
from TD.particles.explosions import ExplosionMedium
from TD.entity import EntityPathFollower, EntityType
from TD.particles.explosions import ExplosionMedium002


class EnemyPlaneT8(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.ENEMY
        self.frames = asset_manager.sprites["T8"]
        self.frame_duration = 30
        self.velocity = 0.25
        self.sprite_offset = [-32, -32]
        self.add_hitbox((0, 0, 40, 20), (-32, -12))

    def killed(self):
        signal("scene.add_entity").send(ExplosionMedium002((self.x, self.y)))
        self.delete()
        

class EnemyPlaneT8O:
    def __init__(self, path_index):
        self.firing = False
        self.firing_elapsed = 1000 #start high so fire right away        
        
    def fire(self):
        x, y = self.path.pos
        y += 20
        bullet = Bullet([x, y])
        bullet.velocity = -0.5
        # signal("scene.add_enemy_bullet").send(bullet)
        
    def tick(self, elapsed):
        self.firing_elapsed += elapsed
        # if self.firing:
        if self.firing_elapsed > 100:
            self.firing_elapsed = 0
            self.fire()

