from enum import Enum 

import pygame
from pygame import Vector2
from blinker import signal 

from TD.entity import EntityType, EntityManager
from TD.config import SCREEN_SIZE
from TD.backgrounds import Sky


class Scene:
    def __init__(self): 
        self.em = EntityManager()
        self.surface = pygame.Surface(SCREEN_SIZE)
        self.background = Sky(SCREEN_SIZE)

        self.signal_add_entity = signal("scene.add_entity")
        self.signal_add_entity.connect(self.em.add)
        signal("scene.delete_entity").connect(self.em.delete)
        
    def pressed(self, pressed, elapsed):
        pass

    def on_event(self, event, elapsed):
        pass

    def on_start_scene(self):
        pass

    def on_delete_scene(self):
        pass

    def tick(self, elapsed):
        self.em.tick(elapsed)
        self.background.tick(elapsed)
    
    def draw(self, elapsed):
        self.surface.fill((0,0,0))
        self.background.draw(elapsed, self.surface)

        self.em.draw(elapsed, self.surface, EntityType.ENEMY)
        self.em.draw(elapsed, self.surface, EntityType.PARTICLE)
        self.em.draw(elapsed, self.surface, EntityType.PICKUP)
        self.em.draw(elapsed, self.surface, EntityType.ENEMYBULLET)
        self.em.draw(elapsed, self.surface, EntityType.PLAYERBULLET)
        self.em.draw(elapsed, self.surface, EntityType.PLAYER)
        self.em.draw(elapsed, self.surface, EntityType.ENEMY)
        self.em.draw(elapsed, self.surface, EntityType.GUI)
