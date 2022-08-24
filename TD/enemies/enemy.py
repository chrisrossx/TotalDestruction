import random 

import pygame 
from pygame import Vector2

from TD.entity import EntityPathFollower, EntityType, EntityVectorMovement
from TD.particles.explosions import ExplosionMedium
from TD.pickups import PickupCoin
from TD.debuging import game_debugger
from TD.assetmanager import asset_manager
from TD import current_app, current_scene

class Enemy:
    def _enemy_init(self):
        self.drops = []
        self.drop_coins = True 
        self.type = EntityType.ENEMY
        self.gun = None 
        self.gun_points = [Vector2(0, 0),]
        self.chain = None 
        self.health = 1

    def killed(self):
        current_scene.em.add(ExplosionMedium(self.pos))
        current_app.mixer.play("explosion md")

        if self.drop_coins:
            r = (random.randint(0, 40)**2)/500
            r = round(r, 0)
            for i in range(int(r)):
                p = PickupCoin(self.pos)
                current_scene.em.add(p)

        for pickup in self.drops:
            p = pickup(self.pos)
            current_scene.em.add(p)
        self.delete()

    def hit(self, bullet):
        self.health -= bullet.damage
        if self.health <= 0:
            self.killed()
        # print("enemy hit", bullet)

    def collision(self):
        """Hit by player ship"""

    def enemy_missed(self):
        current_scene.enemy_missed(self)
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
        if game_debugger.show_hitboxes:
            for i in range(len(self.gun_points)):
                pygame.draw.circle(surface, (0,255,0), self.pos + self.gun_points[i], 5, 1)

            line = asset_manager.fonts["xs"].render("[  H={} ]".format(self.health), True, (255,0,0))
            pos = self.pos + self.sprite_offset
            pos.y -= line.get_rect().h
            surface.blit(line, pos)



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
