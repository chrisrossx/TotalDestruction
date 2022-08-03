import pygame 


class Bullet:
    def __init__(self, pos):
        self.surface = pygame.Surface((15,5))
        pygame.draw.rect(self.surface, (255,0,0), self.surface.get_rect())

        self.hitbox = self.surface.get_rect()
        self.pos = pos
        self.hitbox.x = pos[0]
        self.hitbox.y = pos[1]
        self.velocity = 0.5

    def tick(self, elapsed):
        self.pos[0] += elapsed * self.velocity
        self.hitbox.x = self.pos[0]
        self.hitbox.y = self.pos[1]
    
    def draw(self, elapsed, surface):
        surface.blit(self.surface, self.pos)
