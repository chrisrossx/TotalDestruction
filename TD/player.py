
from blinker import signal 
import pygame 

from TD.debuging import game_debugger
from TD.bullets import BulletGreenRound001
from TD.entity import Entity, EntityType
from TD.config import SCREEN_SIZE


class PlayerShip(Entity):
    def __init__(self):
        super().__init__()
        self.type = EntityType.PLAYER
        self.screen_size = SCREEN_SIZE
        surface = pygame.Surface((40,40), pygame.SRCALPHA, 32)
        surface.convert_alpha()
        self.render_simple_ship(surface)
        self.frames.append(surface)
        self.sprite_offset = pygame.Vector2(-20, -20)

        self.x = -40
        self.y = 300

        self.input_enabled = False

        self.velocity = 0.25
        self.heading = [0, 0]

        self.add_hitbox((0, 0, 30, 20), pygame.Vector2(-20, -10))
        self.add_hitbox((0, 0, 40, 8), pygame.Vector2(-20, -4))

        rect = surface.get_rect()
        left = rect.w / 2
        right = self.screen_size[0] - left
        top = rect.h / 2
        bottom = self.screen_size[1] - top
        self.bounds = pygame.Rect((left, top, right-left, bottom-top))

        self.firing = False
        self.firing_elapsed = 1000 #start high so fire right away
        


    def render_simple_ship(self, surface):
        #Guns under Wings
        rect = pygame.Rect(8, 5, 10, 3)
        pygame.draw.rect(surface, (60,60,60), rect)
        rect.y = 33
        pygame.draw.rect(surface, (60,60,60), rect)

        #Main Ship body
        points = ((0,0), (40,20), (0,40))
        pygame.draw.polygon(surface, (80,80,80), points)
        #white lines behind visor
        points = ((0, 15), (20, 15), (20,25), (0, 25))
        pygame.draw.lines(surface, (100,100,100), False, points)
        #visor
        points = ((20, 15), (35, 20), (20, 25))
        pygame.draw.polygon(surface, (180,180,180), points)
        #dark wings
        points = ((0, 0), (0, 10), (18, 12))
        pygame.draw.polygon(surface, (60,60,60), points)
        points = ((0, 40), (0, 30), (18, 28))
        pygame.draw.polygon(surface, (60,60,60), points)

    def fire(self):
        x, y = self.pos
        x += 20
        bullet = BulletGreenRound001([x, y], -15)
        # signal("scene.add_entity").send(bullet)
        bullet = BulletGreenRound001([x, y], 0)
        signal("scene.add_entity").send(bullet)
        bullet = BulletGreenRound001([x, y], 15)
        # signal("scene.add_entity").send(bullet)

    def pressed(self, pressed, elapsed):

        if self.input_enabled:

            if pressed[pygame.K_SPACE]:
                self.firing = True
            else:
                self.firing = False
                # self.firing_elapsed = 1000

            # Account for anguluar velocity, so that ship doesn't fly faster at diagonals. 
            heading = [0, 0]
            if pressed[pygame.K_DOWN] and not pressed[pygame.K_UP]:
                heading[1] = 1
            if pressed[pygame.K_UP] and not pressed[pygame.K_DOWN]:
                heading[1] = -1
            if pressed[pygame.K_LEFT] and not pressed[pygame.K_RIGHT]:
                heading[0] = -1
            if pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                heading[0] = 1

            if heading[0] != 0 and heading[1] != 0:
                heading[0] *= 0.7071 # sqrt(1/2)
                heading[1] *= 0.7071 # sqrt(1/2)

            # velocity = self.velocity if not pressed[pygame.K_LSHIFT] else self.velocity * 3
            self.heading = heading


    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        # pygame.draw.circle(surface, (255,255,0), (self.x, self.y), 4)
        # print("player draw")


    def tick(self, elapsed):
        #Move Ship
        self.x += (self.heading[0] * self.velocity) * elapsed
        self.y += (self.heading[1] * self.velocity) * elapsed

        #bounds checking
        if self.input_enabled:
            if self.x < self.bounds.left:
                self.x = self.bounds.left
            if self.x > self.bounds.right:
                self.x = self.bounds.right
            if self.y < self.bounds.top:
                self.y = self.bounds.top
            if self.y > self.bounds.bottom:
                self.y = self.bounds.bottom

        self.firing_elapsed += elapsed
        if self.firing:
            if self.firing_elapsed > 350:
                self.firing_elapsed = 0
                self.fire()

        super().tick(elapsed)

