import random 

import pygame 
from pygame import Vector2

from TD.entity import EntityVectorMovement, EntityType, Entity
from TD.assetmanager import asset_manager
from TD.config import SCREEN_SIZE
from TD import current_scene
from TD.debuging import game_debugger
from TD.particles.smoke import MissileSmoke


class Bullet(EntityVectorMovement):
    _screen_rect = pygame.Rect(-40 ,-40, SCREEN_SIZE.x+80, SCREEN_SIZE.y+80) # Delete Sprite if it goes off screen
    hitbox_offset = Vector2(-5, -5)
    hitbox_size = Vector2(10, 10)

    def __init__(self, pos, angle):
        super().__init__()
        self.damage = 1
        self.type = EntityType.ENEMYBULLET
        self.pos = pos 
        self.heading = pygame.Vector2(1.0,0.0)
        self.heading.rotate_ip(angle * -1)
        self.add_hitbox((0,0, self.hitbox_size.x, self.hitbox_size.y), self.hitbox_offset)

    def tick(self, elapsed):
        super().tick(elapsed)
        # Delete Sprite if it goes off screen
        if not self._screen_rect.collidepoint(self.pos):
            self.delete()


class RotatingBullet(EntityVectorMovement):
    _screen_rect = pygame.Rect(-40 ,-40, SCREEN_SIZE.x+80, SCREEN_SIZE.y+80) # Delete Sprite if it goes off screen
    hitbox_vectors = []
    frame_source = None 

    def __init__(self, pos, angle):
        super().__init__()
        self.type = EntityType.ENEMYBULLET
        self.damage = 1
        self.pos = pos.copy() 
        self.angle = angle
        self.old_angle = angle
        self.velocity = 0.1
        self.total_elapsed = 0

        self.rotated(force=True)

    def rotated(self, force=False):
        
        #Rotate Heading
        self.heading = pygame.Vector2(1.0, 0.0)
        self.heading.rotate_ip(self.angle * -1)
        
        # Don't redraw rotation every small angle, step it to +-3 degrees
        d = self.old_angle - self.angle
        if d >= 3 or d <= -3 or force:
            #Rotate Sprite
            self.frames = [s.copy() for s in asset_manager.sprites[self.frame_source]]
            self.frames = [pygame.transform.rotate(s, self.angle) for s in self.frames]
            self.calc_hitboxes()
            self.old_angle = self.angle
            self.sprite_offset = Vector2(self.surface.get_rect().center) * -1
            self.on_rotated(force=force)
    
    def on_rotated(self, force=False):
        pass

    def calc_hitboxes(self):
        self.hitboxes = []
        self.hitbox_offsets = []
        for hitbox_vector in self.hitbox_vectors:
            h = Vector2(1.0, 0.0)
            h.rotate_ip((hitbox_vector["angle"] + self.angle) * -1)
            h *= hitbox_vector["offset"]
            h -= Vector2(hitbox_vector["size"][0]/2, hitbox_vector["size"][1]/2)
            r = pygame.Rect(0, 0, hitbox_vector["size"][0], hitbox_vector["size"][1])
            self.add_hitbox(r, h)


    def tick(self, elapsed):
        self.total_elapsed += elapsed

        super().tick(elapsed)

        # Delete Sprite if it goes off screen
        if not self._screen_rect.collidepoint(self.pos):
            self.delete()    


class Bullet001(RotatingBullet):
    hitbox_vectors = [
        {"size": (10, 10), "angle": 0, "offset": 10},
    ]
    frame_source = "Bullet 001"
    def __init__(self, pos, angle):
        super().__init__(pos, angle)
        self.type = EntityType.PLAYERBULLET
        self.frame_loop_start = 2
        self.frame_duration = 75
        self.velocity = 0.75


class Bullet002(Bullet):
    hitbox_offset = Vector2(-4, -4)
    hitbox_size = Vector2(8, 8)
    def __init__(self, pos, angle=180):
        super().__init__(pos, angle)
        self.sprite_offset = Vector2(-5, -5)
        self.frames = asset_manager.sprites["Bullet 002"]
        self.velocity = 0.55


class Bullet003(Bullet):
    hitbox_offset = Vector2(-5, -5)
    hitbox_size = Vector2(10, 10)
    def __init__(self, pos, angle=180):
        super().__init__(pos, angle)
        self.sprite_offset = Vector2(-8, -8)

        self.frames = asset_manager.sprites["Bullet 003"]
        
        self.frame_index = random.randrange(0, len(self.frames))
        self.frame_duration = 70
        self.velocity = 0.25
        # self.heading = Vector2(-1, 0)


class Bullet004(RotatingBullet):
    hitbox_vectors = [
        {"size": (10, 10), "angle": 0, "offset": 4},
    ]
    frame_source = "Bullet 004"
    def __init__(self, pos, angle):
        super().__init__(pos, angle)
        self.frame_duration = 75
        self.velocity = 0.75


class Bullet005(Bullet):
    hitbox_offset = Vector2(-4, -4)
    hitbox_size = Vector2(8, 8)
    def __init__(self, pos, angle=180):
        super().__init__(pos, angle)
        self.sprite_offset = Vector2(-8, -8)
        self.frames = asset_manager.sprites["Bullet 005"]
        self.frame_duration = 55
        self.velocity = 0.55



class Missile(RotatingBullet):
    # Angle, Distance in Pixels
    smoke_vector = {
        "angle": 180,
        "offset": 17
        }
    frame_source = "Missile 001"
    hitbox_vectors = [
        {"size": (10, 10), "angle": 0, "offset": 4},
    ]

    def __init__(self, pos, angle):
        super().__init__(pos, angle)
        self.frame_duration = 1000/5
        self.velocity = 0.21

        self.emmit_smoke_elapsed = 0
        self.smoke_point = Vector2(0, 0)
        self.turning_rate = 0.20
    
    def on_rotated(self, force):
        self.calc_smoke_point()

    def calc_smoke_point(self):
        h = Vector2(1.0,0.0)
        h.rotate_ip((self.smoke_vector["angle"] + self.angle) * -1)
        h *= self.smoke_vector["offset"]
        self.smoke_point = h

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        if game_debugger.show_hitboxes:
            pygame.draw.circle(surface, (255,155,155), self.smoke_point+self.pos, 5, 1)

    def get_angle(self):
        player_pos = current_scene.player.get_pos()
        gun_pos = self.pos
        angle1 = player_pos - gun_pos
        angle1.normalize_ip()
        angle1 = angle1.angle_to((0,0))
        return angle1

    def tick(self, elapsed):

        #Don't home missle for ever, after elapsed time start to reduce turning ability
        if self.total_elapsed >= 1000:
            #Start to reduce turning rate
            self.turning_rate -= elapsed * 0.0002

        if self.turning_rate > 0:
            a = self.get_angle()
            a = (a - self.angle) % 360 #Diference of angle, normalized
            if a > 180: #Turn Left
                self.angle -= elapsed * self.turning_rate
                self.rotated()
            else: #Turn Right
                self.angle += elapsed * self.turning_rate
                self.rotated()

        self.emmit_smoke_elapsed += elapsed 
        if self.emmit_smoke_elapsed >= 26:
            self.emmit_smoke_elapsed = 0
            a = Vector2(random.randint(-2, 2),random.randint(-2, 2))
            current_scene.em.add(MissileSmoke(self.smoke_point + self.pos+a))
        super().tick(elapsed)


class Missile002(Missile):
    frame_source = "Missile 001"
    def tick(self, elapsed):

        #Don't home missle for ever, after elapsed time start to reduce turning ability
        if self.total_elapsed >= 1000:
            #Start to reduce turning rate
            self.turning_rate -= elapsed * 0.0002

        if self.turning_rate > 0:
            a = self.get_angle()
            a = (a - self.angle) % 360 #Diference of angle, normalized
            if a > 180: #Turn Left
                self.angle -= elapsed * self.turning_rate
                self.rotated()
            else: #Turn Right
                self.angle += elapsed * self.turning_rate
                self.rotated()

        self.emmit_smoke_elapsed += elapsed 
        if self.emmit_smoke_elapsed >= 36:
            self.emmit_smoke_elapsed = 0
            a = Vector2(random.randint(-2, 2),random.randint(-2, 2))
            from TD.particles.smoke import MissileSmoke2
            current_scene.em.add(MissileSmoke2(self.smoke_point + self.pos+a))
        super().tick(elapsed)
