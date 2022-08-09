import pygame 
from pygame import Vector2

from TD.entity import EntityVectorMovement, EntityType
from TD.assetmanager import asset_manager
from TD.config import SCREEN_SIZE


class Bullet(EntityVectorMovement):

    angle_config = {
        0: {"SpriteOffset": Vector2(0, 0), "HitboxSize": Vector2(10, 10), "HitboxOffset": Vector2(-5, -5)},
    }
    
    _screen_rect = pygame.Rect(-40 ,-40, SCREEN_SIZE.x+80, SCREEN_SIZE.y+80) # Delete Sprite if it goes off screen

    def __init__(self, pos, angle):
        super().__init__()
        self.pos = pos 
        ac = self.angle_config[angle]
        self.heading = pygame.Vector2(1.0,0.0)
        self.heading.rotate_ip(angle * -1)
        self.add_hitbox((0,0, ac["HitboxSize"].x, ac["HitboxSize"].y), ac["HitboxOffset"])
        self.sprite_offset = ac["SpriteOffset"]

    def tick(self, elapsed):
        super().tick(elapsed)
        # Delete Sprite if it goes off screen
        if not self._screen_rect.collidepoint(self.pos):
            self.delete()


class BulletGreenRound001(Bullet):
    angle_config = {
        0: {"SpriteOffset": Vector2(-32, -10), "HitboxSize": Vector2(14, 14), "HitboxOffset": Vector2(-7, -7)},
        -15: {"SpriteOffset": Vector2(-32, -25), "HitboxSize": Vector2(14, 14), "HitboxOffset": Vector2(-7, -7)},
        15: {"SpriteOffset": Vector2(-32, -25), "HitboxSize": Vector2(14, 14), "HitboxOffset": Vector2(-7, -7)},
        180: {"SpriteOffset": Vector2(-32, -10), "HitboxSize": Vector2(14, 14), "HitboxOffset": Vector2(-7, -7)},

    }

    def __init__(self, pos, angle):
        super().__init__(pos, angle)
        self.type = EntityType.PLAYERBULLET
        self.frames = asset_manager.sprites["Bullet Green Round 001"][angle]
        self.frame_loop_start = 2
        self.frame_duration = 75
        self.velocity = 0.75

class BulletBlueRound001(Bullet):
    angle_config = {
        0: {"SpriteOffset": Vector2(-5, -5), "HitboxSize": Vector2(8, 8), "HitboxOffset": Vector2(-4, -4)},

    }
    def __init__(self, pos, angle):
        super().__init__(pos, angle)
        self.type = EntityType.ENEMYBULLET
        self.frames = asset_manager.sprites["Bullet Blue Round 001"][angle]
        self.velocity = 0.50
        self.heading = Vector2(-1, 0)
