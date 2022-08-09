from enum import Enum

import pygame
from pygame import Vector2
from blinker import signal

from TD.player import PlayerShip
from TD.enemies.PlaneT8 import EnemyPlaneT8
from TD.backgrounds import Sky
from TD.debuging import game_debugger
from TD.pickups import PickupHeart, PickupStar
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
                
        self.signal_add_entity = signal("scene.add_entity")
        signal("scene.delete_entity").connect(self.em.delete)
        signal("scene.add_entity").connect(self.em.add)

        self.ship = PlayerShip(size)
        self.em.add(self.ship)

        self.timed_add = []
        # self.timed_add.append((0, EnemyPlaneT8(0)))
        # self.timed_add.append((0, EnemyPlaneT8(1)))
        # self.timed_add.append((0, EnemyPlaneT8("T8 Charlie")))
        # self.timed_add.append((400, EnemyPlaneT8("T8 Delta")))
        # self.timed_add.append((400, EnemyPlaneT8("T8 Echo")))
        # for i in range(1, 2):
        #     x = i * 750
        #     self.timed_add.append((x, EnemyPlaneT8(0)))
        #     self.timed_add.append((x, EnemyPlaneT8(1)))
        #     self.timed_add.append((x, EnemyPlaneT8("T8 Charlie")))
        #     self.timed_add.append((400+x, EnemyPlaneT8("T8 Delta")))
        #     self.timed_add.append((400+x, EnemyPlaneT8("T8 Echo")))
        
        self.timed_add.append((0, PickupHeart(Vector2(800, 100))))
        self.timed_add.append((0, PickupStar(Vector2(800, 200))))
        
        # self.timed_add.append((0, "particle", ExplosionMedium([1000, 100])))

        self.runtime = 0.0

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

        for enemy in self.em.collidetypes(EntityType.PLAYER, EntityType.ENEMY).keys():
            enemy.killed()

        for pickup in self.em.collidetypes(EntityType.PLAYER, EntityType.PICKUP).keys():
            pickup.pickedup()

        for enemy, bullets in self.em.collidetypes(EntityType.PLAYERBULLET, EntityType.ENEMY, True).items():
            enemy.killed()
            for b in bullets:
                b.delete()

        for bullets in self.em.collidetypes(EntityType.ENEMYBULLET, EntityType.PLAYER, True).values():
            for b in bullets:
                print("PLAYER HIT")
                b.delete()
                
        timed_add = []
        for time_to_add, entity in self.timed_add:
            if time_to_add <= self.runtime:
                self.signal_add_entity.send(entity)
            else:
                timed_add.append((time_to_add, entity))
        self.timed_add = timed_add

    def tick(self, elapsed):
        self.sky.tick(elapsed)

        self.em.tick(elapsed)
        
        if self.state == State.PLAYING:
            self.tick_playing(elapsed)
        elif self.state == State.STARTING:
            self.tick_starting(elapsed)

 
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
        self.em.draw(elapsed, self.surface, EntityType.GUI)

        #Debug Runtime
        game_debugger.lines[0] = "Runtime: {}".format(str(round(self.runtime/1000, 1)))
        game_debugger.lines[1] = "Entities: {}".format(str(len(self.em.entities)))
        game_debugger.lines[2] = "- Particles: {}".format(str(len(self.em.entities_by_type[EntityType.PARTICLE])))
        game_debugger.lines[3] = "- Enemies: {}".format(str(len(self.em.entities_by_type[EntityType.ENEMY])))
        game_debugger.lines[4] = "- Enemy Bullets: {}".format(str(len(self.em.entities_by_type[EntityType.ENEMYBULLET])))
        game_debugger.lines[5] = "- Player Bullets: {}".format(str(len(self.em.entities_by_type[EntityType.PLAYERBULLET])))
        game_debugger.lines[6] = "- Pickups: {}".format(str(len(self.em.entities_by_type[EntityType.PICKUP])))

        
