from enum import Enum

import pygame
from blinker import signal

from TD.player import PlayerShip
from TD.enemies.PlaneT8 import EnemyPlaneT8
from TD.backgrounds import Sky
from TD.debuging import debug_display

from TD.states import State


class NeverEndingLevel:

    def __init__(self, size):

        self.font = pygame.font.SysFont(None, 24)

        self.surface = pygame.Surface(size)
        self.sky = Sky(size)

        self.state = State.NOT_STARTED
        
        self.enemies = []
        self.signal_add_enemy = signal("scene.add_enemy")
        self.signal_add_enemy.connect(self.on_add_enemey)
        self.signal_delete_enemy = signal("scene.delete_enemy")
        self.signal_delete_enemy.connect(self.on_delete_enemey)

        self.ship = PlayerShip(size)

        self.timed_add = []
        self.timed_add.append((500, "enemy", EnemyPlaneT8((500, 100))))
        self.timed_add.append((1000, "enemy", EnemyPlaneT8((500, 100))))
        self.timed_add.append((1500, "enemy", EnemyPlaneT8((500, 100))))

        self.runtime = 0.0

    def on_add_enemey(self, entity):
        self.enemies.append(entity)

    def on_delete_enemey(self, entity):
        enemies = []
        for enemy in self.enemies:
            if entity != enemy:
                enemies.append(enemy)
        self.enemies = enemies

    def tick(self, elapsed):
        self.sky.tick(elapsed)

        self.runtime += elapsed

        #TODO: Should this sort a cached list because of delets?
        for enemy in self.enemies:
            enemy.tick(elapsed)

        timed_add = []
        for time_to_add, entity_type, entity in self.timed_add:
            if time_to_add <= self.runtime:
                if entity_type == "enemy":
                    self.signal_add_enemy.send(entity)
            else:
                timed_add.append((time_to_add, entity_type, entity))
        self.timed_add = timed_add

    def pressed(self, pressed, elapsed):
        self.ship.pressed(pressed, elapsed)

    def on_event(self, event, elapsed):
        pass
        # self.ship.on_event(event, elapsed)

    def draw(self, elapsed):
        self.surface.fill((0,0,0))

        #fill background with Sky Texture
        self.sky.draw(elapsed, self.surface)
        for enemy in self.enemies:
            enemy.draw(elapsed, self.surface)
        
        self.ship.draw(elapsed, self.surface)

        #Debug Runtime
        debug_display.line1 = "Runtime: {}".format(str(round(self.runtime/1000, 1)))
        debug_display.line2 = "Enemies: {}".format(str(len(self.enemies)))
