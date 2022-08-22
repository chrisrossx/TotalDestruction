import random 

import pygame 
from pygame import Vector2
from blinker import signal 

from TD.entity import EntityPathFollower, EntityType, EntityVectorMovement
from TD.particles.explosions import ExplosionMedium
from TD.pickups import PickupCoin
from TD.debuging import game_debugger

class Enemy:
    def _enemy_init(self):
        self.drops = []
        self.drop_coins = True 
        self.type = EntityType.ENEMY
        self.gun = None 
        self.gun_points = [Vector2(0, 0),]
        self.chain = None 

    def killed(self):
        signal("scene.player.enemy_killed").send(self)
        signal("scene.add_entity").send(ExplosionMedium(self.pos))
        signal("mixer.play").send("explosion md")

        if self.drop_coins:
            r = (random.randint(0, 40)**2)/500
            r = round(r, 0)
            for i in range(int(r)):
                p = PickupCoin(self.pos)
                signal("scene.add_entity").send(p)

        for pickup in self.drops:
            p = pickup(self.pos)
            signal("scene.add_entity").send(p)
        self.delete()

    def enemy_missed(self):
        signal("scene.enemy_missed").send(self)
        if self.chain != None:
            if self.chain.chain_lost == False:
                print("Chain Lost!")
            self.chain.chain_lost = True 
        self.delete()

    def set_gun(self, gun):
        self.gun = gun
        self.gun.parent = self 


class EnemyPathFollower(EntityPathFollower, Enemy):
    def __init__(self, path):
        super().__init__(path)
        self._enemy_init()
        self.chain = None

    def on_end_of_path(self, sender):
        self.enemy_missed()

    def tick(self, elapsed):
        if self.gun:
            self.gun.tick(elapsed)
        super().tick(elapsed)

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        for i in range(len(self.gun_points)):
            if game_debugger.show_hitboxes:
                pygame.draw.circle(surface, (0,255,0), self.pos + self.gun_points[i], 5, 1)


class EnemyVectorMovement(Enemy, EntityVectorMovement):
    def __init__(self):
        super().__init__()
        self._enemy_init()
        self.chain = None

    def tick(self, elapsed):
        if self.gun:
            self.gun.tick(elapsed)
        super().tick(elapsed)

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        for i in range(len(self.gun_points)):
            if game_debugger.show_hitboxes:
                pygame.draw.circle(surface, (0,255,0), self.pos + self.gun_points[i], 5, 1)
