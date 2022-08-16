import pygame
from blinker import signal
from pygame import Vector2

from TD.assetmanager import asset_manager
from TD.paths import PathFollowerOld
from TD.debuging import game_debugger
from TD.entity import EntityPathFollower, EntityType
from TD.particles.explosions import ExplosionMedium002
from TD.bullets import  BulletGreenRound001, BulletBlueRound001
import random

from ..pickups import PickupCoin 

class EnemyPlaneT8(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.ENEMY
        self.frames = asset_manager.sprites["T8"]
        self.frame_duration = 30
        self.velocity = 0.25
        self.sprite_offset = pygame.Vector2(-32, -32)
        self.add_hitbox((0, 0, 40, 20), pygame.Vector2(-32, -12))

        self.firing = False
        self.firing_elapsed = 1000 #start high so fire right away  

        self.drops = []
        self.drop_coins = True 

    def on_end_of_path(self, sender):
        signal("scene.enemy_missed").send(self)
        self.delete()


    def fire(self):
        # x, y = self.pos
        # y += 20
        b = BulletBlueRound001(self.pos.copy(), 0)
        # signal("scene.add_entity").send(b)

    def killed(self):
        signal("scene.player.enemy_killed").send(self)
        signal("scene.add_entity").send(ExplosionMedium002(self.pos))
        asset_manager.sounds["explosion md"].play()

        for pickup in self.drops:
            p = pickup(self.pos)
            signal("scene.add_entity").send(p)
            
        if self.drop_coins:
            r = (random.randint(0, 40)**2)/500
            r = round(r, 0)
            for i in range(int(r)):
                p = PickupCoin(self.pos)
                signal("scene.add_entity").send(p)

        self.delete()
        
    def tick(self, elapsed):
        super().tick(elapsed)
        self.firing_elapsed += elapsed
        if self.firing_elapsed > 300:
            self.firing_elapsed = 0
            self.fire()

