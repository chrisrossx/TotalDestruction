from pprint import PrettyPrinter
import pygame 
from pygame import Vector2
from TD.entity import EntityType
from TD.scenes.scene import Scene

from TD.characters import Sawyer, Elle

import pprint
p = PrettyPrinter(indent=2)


class Chris(Sawyer):
    pass


class TestScene(Scene):
    def __init__(self):
        super().__init__()


        c = Chris("credits")
        c.path.velocity = 0
        c.path.distance = 415
        c.type = EntityType.PARTICLE

        s = Sawyer("credits")
        s.path.velocity = 0
        s.path.distance = 400
        s.type = EntityType.PARTICLE
        self.em.add(c)
        self.em.add(s)

        e = Elle("credits")
        e.path.velocity = 0
        e.path.distance = 500
        self.e = e
        self.s = s 
        self.em.add(e)



    def on_event(self, event, elapsed):
        super().on_event(event, elapsed)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.e.path.distance = 400

    def tick(self, elapsed):
        super().tick(elapsed)
        print("="*40)
        print("Chris and Sawyer are Particles")
        print("Elle is GUI")

        hits = self.em.collidetypes(EntityType.PARTICLE, EntityType.GUI, False)
        if len(hits) > 0:
            p.pprint(hits)
        else:
            print("---")


        hits = self.em.collidetypes(EntityType.GUI, EntityType.PARTICLE, True)
        if len(hits) > 0:
            p.pprint(hits)
        else:
            print("---")

        hits = self.em.collidetypes(EntityType.GUI, EntityType.PARTICLE, False)
        if len(hits) > 0:
            p.pprint(hits)
        else:
            print("---")


        hits = self.em.collidetype(self.e, EntityType.PARTICLE, True)
        if len(hits) > 0:
            p.pprint(hits)
        else:
            print("---")

        hits = self.em.collidetype(self.e, EntityType.PARTICLE, False)
        if len(hits) > 0:
            p.pprint(hits)
        else:
            print("---")








