from enum import Enum

import pygame
from blinker import signal

from TD.player import PlayerShip
from TD.enemies.PlaneT8 import EnemyPlaneT8
from TD.backgrounds import Sky
from TD.debuging import game_debugger
from TD.pickups import PickupHeart
from TD.particles.explosions import ExplosionMedium
from TD.states import State
from ..entity import EntityManager, EntityType


class NeverEndingLevel:

    def __init__(self, size):

        self.em = EntityManager()

        self.font = pygame.font.SysFont(None, 24)

        self.surface = pygame.Surface(size)
        self.sky = Sky(size)

        self.state = State.STARTING

        #Starting State Information
        self.starting_step = 0
        self.starting_elapsed = 0.0
        
        #Playing State Information
        signal("scene.delete_entity").connect(self.em.delete)
        signal("scene.add_entity").connect(self.em.add)

        # self.ship = PlayerShip(size)
        self.ship = PlayerShip(size)
        self.em.add(self.ship)

        a = EnemyPlaneT8(0)
        self.em.add(a)

        self.timed_add = []
        # self.timed_add.append((0, "enemy", EnemyPlaneT8(0)))
        # self.timed_add.append((0, "enemy", EnemyPlaneT8(1)))
        # self.timed_add.append((0, "enemy", EnemyPlaneT8("T8 Charlie")))
        # self.timed_add.append((400, "enemy", EnemyPlaneT8("T8 Delta")))
        # self.timed_add.append((400, "enemy", EnemyPlaneT8("T8 Echo")))
        # self.timed_add.append((500, "enemy", EnemyPlaneT8((500, 100))))
        # self.timed_add.append((1000, "enemy", EnemyPlaneT8((500, 100))))
        # self.timed_add.append((1500, "enemy", EnemyPlaneT8((500, 100))))
        # self.timed_add.append((0, "pickup", PickupHeart([500, 100])))
        # self.timed_add.append((0, "particle", ExplosionMedium([1000, 100])))

        self.runtime = 0.0

    # def on_add_particle(self, entity):
    #     self.particles.append(entity)

    # def on_delete_particle(self, entity):
    #     particles = []
    #     for particle in self.particles:
    #         if entity != particle:
    #             particles.append(particle)
    #     self.particles = particles

    # def on_add_pickup(self, entity):
    #     self.pickups.append(entity)

    # def on_delete_pickup(self, entity):
    #     pickups = []
    #     for pickup in self.pickups:
    #         if entity != pickup:
    #             pickups.append(pickup)
    #     self.pickups = pickups

    # def on_add_player_bullet(self, entity):
    #     self.player_bullets.append(entity)

    # def on_add_enemy_bullet(self, entity):
    #     self.enemy_bullets.append(entity)

    # def on_add_enemey(self, entity):
    #     self.enemies.append(entity)

    # def on_delete_enemey(self, entity):
    #     enemies = []
    #     for enemy in self.enemies:
    #         if entity != enemy:
    #             enemies.append(enemy)
    #     self.enemies = enemies

    def change_state(self, state):
        self.state = state 
        if self.state == State.PLAYING:
            self.ship.input_enabled = True

    def tick_starting(self, elapsed):
        # Skip for now
        self.change_state(State.PLAYING)
        self.ship.pos[0] = 200

        if self.starting_step == 0:
            self.ship.pos[0] += elapsed * 0.12
            if self.ship.pos[0] > 200: 
                self.starting_step = 1
                self.starting_elapsed = 0.0
        elif self.starting_step == 1:
            self.starting_elapsed += elapsed
            if self.starting_elapsed > 500:
                self.change_state(State.PLAYING)

    def tick_playing(self, elapsed):
        self.runtime += elapsed
        self.ship.tick(elapsed)


        #TODO How to bullets delete themselves
        # for pbullet in [e for e in self.player_bullets]:
        #     pbullet.tick(elapsed)
        #     #TODO consider moving this to the bullet itself, like the end of path for enemies PathFollower
        #     if pbullet.pos[0] > 1024:
        #         self.player_bullets.remove(pbullet)

        #TODO How to bullets delete themselves
        # for ebullet in [e for e in self.enemy_bullets]:
        #     ebullet.tick(elapsed)
        #     #TODO consider moving this to the bullet itself, like the end of path for enemies PathFollower
        #     if ebullet.pos[0] < 20:
        #         self.enemy_bullets.remove(ebullet)


        def on_enemy_hit_player(enemy):
            enemy.killed()

        self.em.collidelist(self.ship.hitboxes, on_enemy_hit_player, EntityType.ENEMY)

        # 

    #     #Check if Player is hitting any enemies. 
    #     for enemy in [e for e in self.em.entities_by_type[EntityType.ENEMY]]:
    #         if not enemy.deleted:
    #             for ship_hitbox in self.ship.hitboxes:
    #                 if ship_hitbox.collidelist(enemy.hitboxes) != -1:
    # #                   #TODO Player Damage!
    #                     enemy.killed()
                        # enemy.delete()


        # #check if player bullets are hitting any enemies
        # ebullet_hitboxs = [b.hitbox for b in self.enemy_bullets]
        # for ship_hitbox in self.ship.hitboxs:
        #     hits = ship_hitbox.collidelistall(ebullet_hitboxs)
        #     if len(hits) > 0:
        #         #TODO Player Damage!
        #         print("PLAYER HIT!")
        #         bullets = [self.enemy_bullets[i] for i in hits]
        #         for b in bullets:
        #             self.enemy_bullets.remove(b)
        #     break

        # #check if enemy bullets are hitting player
        # pbullet_hitboxs = [b.hitbox for b in self.player_bullets]
        # for enemy in [e for e in self.enemies]:
        #     if not enemy.deleted:
        #         for enemy_hitbox in enemy.hitboxs:
        #             hits = enemy_hitbox.collidelistall(pbullet_hitboxs)
        #             if len(hits) > 0:
        #                 print("ENEMY HIT")
        #                 enemy.killed()
        #                 bullets = [self.player_bullets[i] for i in hits]
        #                 for b in bullets:
        #                     self.player_bullets.remove(b)
        #             break
    
        timed_add = []
        for time_to_add, entity_type, entity in self.timed_add:
            if time_to_add <= self.runtime:
                pass
                # if entity_type == "enemy":
                #     self.signal_add_enemy.send(entity)
                # if entity_type == "pickup":
                #     self.signal_add_pickup.send(entity)
                # if entity_type == "particle":
                #     self.signal_add_particle.send(entity)
            else:
                timed_add.append((time_to_add, entity_type, entity))
        self.timed_add = timed_add

    def tick(self, elapsed):
        self.sky.tick(elapsed)

        if self.state == State.PLAYING:
            self.tick_playing(elapsed)
        elif self.state == State.STARTING:
            self.tick_starting(elapsed)

        self.em.tick(elapsed)
 
    def pressed(self, pressed, elapsed):
        self.ship.pressed(pressed, elapsed)

    def on_event(self, event, elapsed):
        pass
        # self.ship.on_event(event, elapsed)

    def draw_starting(self, elapsed):
        if self.starting_step == 1:
            font = pygame.font.SysFont("consolas", 96)
            line = font.render("GO!", True, (255,255,255))
            lr = line.get_rect()
            sr = self.surface.get_rect()
            x = (sr.width/2) - (lr.width/2)
            y = (sr.height/2) - (lr.height/2)
            self.surface.blit(line, (x, y))

    def draw(self, elapsed):
        self.surface.fill((0,0,0))

        #fill background with Sky Texture
        self.sky.draw(elapsed, self.surface)
        if self.state == State.PLAYING:
            pass
            
        elif self.state == State.STARTING:
            self.draw_starting(elapsed)
 
        self.em.draw(elapsed, self.surface, EntityType.ENEMY)
        self.em.draw(elapsed, self.surface, EntityType.PARTICLE)
        self.em.draw(elapsed, self.surface, EntityType.PICKUP)
        self.em.draw(elapsed, self.surface, EntityType.ENEMYBULLET)
        self.em.draw(elapsed, self.surface, EntityType.PLAYERBULLET)
        self.em.draw(elapsed, self.surface, EntityType.PLAYER)
        self.em.draw(elapsed, self.surface, EntityType.ENEMY)

        #Debug Runtime
        game_debugger.lines[0] = "Runtime: {}".format(str(round(self.runtime/1000, 1)))
        game_debugger.lines[1] = "Entities: {}".format(str(len(self.em.entities)))
        game_debugger.lines[2] = "- Particles: {}".format(str(len(self.em.entities_by_type[EntityType.PARTICLE])))
        game_debugger.lines[3] = "- Enemies: {}".format(str(len(self.em.entities_by_type[EntityType.ENEMY])))
        game_debugger.lines[4] = "- Enemy Bullets: {}".format(str(len(self.em.entities_by_type[EntityType.ENEMYBULLET])))
        game_debugger.lines[5] = "- Player Bullets: {}".format(str(len(self.em.entities_by_type[EntityType.PLAYERBULLET])))
        game_debugger.lines[6] = "- Pickups: {}".format(str(len(self.em.entities_by_type[EntityType.PICKUP])))

        
