import pygame 

from TD.entity import EntityVectorMovement, EntityType
from TD.assetmanager import asset_manager



class Bullet(EntityVectorMovement):
    pass


class BulletGreenRound001(EntityVectorMovement):
    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.PLAYERBULLET
        self.frames = asset_manager.sprites["Bullet Green Round 001"]
        self.frame_loop_start = 2
        self.frame_duration = 75
        # self.heading = pygame.Vector2(1.0,0.0)
        self.heading.rotate_ip(30)
        self.velocity = 0.75
        self.pos = pos
        self.sprite_offset = pygame.Vector2(-32, -32)
        self.add_hitbox((0,0,16,16), pygame.Vector2(4,4))


    def tick(self, elapsed):
        super().tick(elapsed)
        if self.x > 1024:
            self.delete()
