
import pygame 
from pygame import Vector2

from TD.debuging import game_debugger
from TD.bullets import Bullet001, Missile
from TD.entity import Entity, EntityType
from TD.config import SCREEN_SIZE
from .pickups import PickupType
from TD.scenes.levels.level_state import LevelState
from TD.assetmanager import asset_manager
from TD import current_scene, current_app
from TD.particles.spoofs import SpoofHitFollow
from TD.particles.explosions import ExplosionSmallFollow

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

        self.pos = Vector2(-40, 320)
        # self.x = -40
        # self.y = 300

        self.input_enabled = False
        self.paused = False

        self.velocity = 0.25
        self.heading = Vector2(0, 0)

        self.add_hitbox((0, 0, 30, 20), pygame.Vector2(-20, -10))
        self.add_hitbox((0, 0, 40, 8), pygame.Vector2(-20, -4))

        rect = surface.get_rect()
        left = rect.w / 2
        right = self.screen_size[0] - left
        top = rect.h / 2
        bottom = self.screen_size[1] - top
        self.bounds = pygame.Rect((left, top, right-left, bottom-top))

        self.firing = False
        self.firing_elapsed = 1000 # start high so fire right away

        self.health = 3
        self.been_hit = False
        self.coins = 0

    def get_pos(self):
        return self.pos.copy()

    def pickedup(self, pickup):
        if pickup.pickup_type == PickupType.HEART:
            current_app.mixer.play("heart pickup")
            if self.health < 3:
                self.health += 1
                current_scene.hud_lives(self.health)
        
        if pickup.pickup_type == PickupType.COIN:
            current_app.mixer.play("coin pickup")
            self.coins += 1

    def hit(self, bullet):
        if game_debugger.god_mode == False:
            self.health -= bullet.damage
            self.been_hit = True 

        current_scene.hud_lives(self.health)
        current_scene.hud_been_hit()
            
        if type(bullet) == Missile:
            l = (bullet.pos.lerp(self.pos, 0.8) - bullet.pos) * -1
            current_scene.em.add(ExplosionSmallFollow(self, l))
        else:
            l = (bullet.pos.lerp(self.pos, 0.9) - bullet.pos) * -1
            current_scene.em.add(SpoofHitFollow(self, l))
        current_app.mixer.play("player hit")


        if self.health <= 0:
            current_scene.change_state(LevelState.DEAD)
        

    def collision(self):
        pass
        "No Damage to Player if Overlapping a Enemy, Bullets Only!"
        # if game_debugger.god_mode == False:
        #     self.health -= 1
        #     signal("scene.hud.lives").send(self.health)
        #     if self.health == 0:
        #         signal("scene.change_state").send(LevelState.DEAD)
        #     self.been_hit = True 
        #     signal("scene.hud.medal.heart").send(False)
        #     signal("mixer.play").send("player collision")

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
        bullet = Bullet001([x, y], -15)
        current_scene.em.add(bullet)
        bullet = Bullet001([x, y], 0)
        current_scene.em.add(bullet)
        bullet = Bullet001([x, y], 15)
        current_scene.em.add(bullet)
        current_app.mixer.play("player gun")

    def pressed(self, pressed, elapsed):

        if self.input_enabled:

            if pressed[pygame.K_SPACE] or pressed[pygame.K_LCTRL]:
                self.firing = True
            else:
                self.firing = False
                # self.firing_elapsed = 1000

            # Account for anguluar velocity, so that ship doesn't fly faster at diagonals. 
            heading = Vector2(0,0)
            if pressed[pygame.K_DOWN] and not pressed[pygame.K_UP]:
                heading[1] = 1
            if pressed[pygame.K_UP] and not pressed[pygame.K_DOWN]:
                heading[1] = -1
            if pressed[pygame.K_LEFT] and not pressed[pygame.K_RIGHT]:
                heading[0] = -1
            if pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
                heading[0] = 1

            if heading.length() > 0:
                heading.normalize_ip()
            self.heading = heading

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        if game_debugger.show_hitboxes:
            health = "{}(GOD)".format(self.health) if game_debugger.god_mode else self.health
            line = asset_manager.fonts["xxs"].render("[  H={}  ]".format(health), True, (255,0,0))
            pos = self.pos + self.sprite_offset
            pos.y -= line.get_rect().h
            surface.blit(line, pos)


        # pygame.draw.circle(surface, (255,255,0), (self.x, self.y), 4)
        # print("player draw")


    def tick(self, elapsed):
        #Move Ship
        self.pos += (self.heading * self.velocity) * elapsed

        #bounds checking
        if self.input_enabled:
            if self.pos.x < self.bounds.left:
                self.pos.x = self.bounds.left
            if self.pos.x > self.bounds.right:
                self.pos.x = self.bounds.right
            if self.pos.y < self.bounds.top:
                self.pos.y = self.bounds.top
            if self.pos.y > self.bounds.bottom:
                self.pos.y = self.bounds.bottom

        self.firing_elapsed += elapsed
        if self.firing and self.input_enabled:
            if self.firing_elapsed > 350:
                self.firing_elapsed = 0
                self.fire()

        super().tick(elapsed)

