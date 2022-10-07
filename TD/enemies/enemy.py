import random 

import pygame 
from pygame import Vector2

from TD.entity import EntityPathFollower, EntityType, EntityVectorMovement
from TD.particles.explosions import ExplosionMedium
from TD.pickups import PickupCoin, PickupUpgrade
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

        self.glow_surface = None
        self.glow_offset = Vector2(0, 0)

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

        current_scene.enemies_killed += 1
        self.delete()

    def hit(self, bullet):
        self.health -= bullet.damage
        if self.health <= 0:
            self.killed()
            current_app.mixer.play("enemy hit")
        # print("enemy hit", bullet)

    def collision(self):
        """Hit by player ship"""
        self.killed()

    def enemy_missed(self):
        current_scene.enemy_missed(self)
        if self.chain != None:
            if self.chain.chain_lost == False:
                current_app.mixer.play("chain lost")
            self.chain.chain_lost = True 
        self.delete()

    def set_gun(self, gun):
        self.gun = gun
        self.gun.parent = self 
    
    def _enemy_tick(self, elapsed):
        if self.gun:
            self.gun.tick(elapsed)

    def _enemy_draw(self, elapsed, surface):
        if game_debugger.show_hitboxes:
            for i in range(len(self.gun_points)):
                pygame.draw.circle(surface, (0,255,0), self.pos + self.gun_points[i], 5, 1)

            line = asset_manager.fonts["xxs"].render("[  H={} ]".format(self.health), True, (255,0,0))
            pos = self.pos + self.sprite_offset
            pos.y -= line.get_rect().h
            if pos.y < 0:
                #Draw below caharacter if its to high up on the screen! 
                pos.y = self.pos.y# + self.get_rect().h
            surface.blit(line, pos)
    
    def _enemy_draw_glow(self, elapsed, surface):
        if PickupUpgrade in self.drops and self.glow_surface:
            surface.blit(self.glow_surface, self.pos + self.sprite_offset + self.glow_offset)


class EnemyPathFollower(EntityPathFollower, Enemy):
    def __init__(self, path):
        super().__init__(path)
        self._enemy_init()
        self.chain = None

    def on_end_of_path(self):
        self.enemy_missed()

    def tick(self, elapsed):
        super().tick(elapsed)
        self._enemy_tick(elapsed)

    def draw(self, elapsed, surface):
        self._enemy_draw_glow(elapsed, surface)
        super().draw(elapsed, surface)
        self._enemy_draw(elapsed, surface)


class EnemyVectorMovement(Enemy, EntityVectorMovement):
    def __init__(self):
        super().__init__()
        self._enemy_init()
        self.chain = None

    def tick(self, elapsed):
        super().tick(elapsed)
        self._enemy_tick(elapsed)
        if self.pos.y <= -40:
            self.on_off_screen()

    def on_off_screen(self):
        self.enemy_missed()

    def draw(self, elapsed, surface):
        self._enemy_draw_glow(elapsed, surface)
        super().draw(elapsed, surface)
        self._enemy_draw(elapsed, surface)
