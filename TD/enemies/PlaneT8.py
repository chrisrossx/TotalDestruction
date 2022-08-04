import pygame
from blinker import signal

from TD.assetmanager import asset_manager
from TD.paths import PathFollower
from TD.debuging import game_debugger
from TD.bullets import Bullet
from TD.particles.explosions import ExplosionMedium

class EnemyPlaneT8:
    def __init__(self, path_index):
        self.frames = asset_manager.sprites["T8"]
        self.frame_index = 0
        self.frame_elapsed = 0
        self.frame_count = len(self.frames)

        self.velocity = -0.1
        
        self.firing = False
        self.firing_elapsed = 1000 #start high so fire right away        


        self.path = PathFollower(path_index, (-32, -32))
        self.path.on_end_of_path.connect(self.on_end_of_path)
        self.path.velocity = 0.15
        self.deleted = False
        #self.hitbox = self.frames[0].get_rect()
        self.hitboxs = [
            pygame.Rect(0, 0, 40, 20),
            # pygame.Rect(0, 0, 40, 20),
        ]
        self.hitbox_offsets = [
            [0, 20],
            # [0, 20],
        ]
        
    def fire(self):
        x, y = self.path.pos
        y += 20
        bullet = Bullet([x, y])
        bullet.velocity = -0.5
        # signal("scene.add_enemy_bullet").send(bullet)
        

    def draw(self, elapsed, surface):
        self.frame_elapsed += elapsed
        if self.frame_elapsed >= 25:
            self.frame_elapsed = 0
            self.frame_index += 1
            if self.frame_index == self.frame_count:
                self.frame_index = 0
        if game_debugger.show_paths:
            self.path.draw(elapsed, surface)
        surface.blit(self.frames[self.frame_index], (self.path.x, self.path.y))

        if game_debugger.show_hitboxs:
            for i in range(len(self.hitboxs)):
                pygame.draw.rect(surface, (255,0,0), self.hitboxs[i], 1)

    def tick(self, elapsed):
        self.path.tick(elapsed)
        for i in range(len(self.hitboxs)):
            self.hitboxs[i].x = self.path.x + self.hitbox_offsets[i][0]
            self.hitboxs[i].y = self.path.y + self.hitbox_offsets[i][1]

        self.firing_elapsed += elapsed
        # if self.firing:
        if self.firing_elapsed > 100:
            self.firing_elapsed = 0
            self.fire()


    def killed(self):
        self.delete()
        signal("scene.add_particle").send(ExplosionMedium([self.path.x, self.path.y]))

    def delete(self):
        self.deleted = True 
        signal("scene.delete_enemy").send(self)

    def on_end_of_path(self, sender):
        self.delete()

