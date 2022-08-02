
import pygame 

class PlayerShip:
    def __init__(self, screen_size) -> None:
        self.screen_size = screen_size
        self.surface = pygame.Surface((40,40), pygame.SRCALPHA, 32)
        self.surface.convert_alpha()
        self.render_simple_ship()
        self.rect = self.surface.get_rect()

        self.pos = [50.0, self.screen_size[1] / 2]
        self.velocity = 0.5

        
        left = self.rect.w / 2
        right = screen_size[0] - left
        top = self.rect.h / 2
        bottom = self.screen_size[1] - top
        self.bounds = pygame.Rect((left, top, right-left, bottom-top))

    def render_simple_ship(self):


        #Guns under Wings
        rect = pygame.Rect(8, 5, 10, 3)
        pygame.draw.rect(self.surface, (60,60,60), rect)
        rect.y = 33
        pygame.draw.rect(self.surface, (60,60,60), rect)

        #Main Ship body
        points = ((0,0), (40,20), (0,40))
        pygame.draw.polygon(self.surface, (80,80,80), points)
        #white lines behind visor
        points = ((0, 15), (20, 15), (20,25), (0, 25))
        pygame.draw.lines(self.surface, (100,100,100), False, points)
        #visor
        points = ((20, 15), (35, 20), (20, 25))
        pygame.draw.polygon(self.surface, (180,180,180), points)
        #dark wings
        points = ((0, 0), (0, 10), (18, 12))
        pygame.draw.polygon(self.surface, (60,60,60), points)
        points = ((0, 40), (0, 30), (18, 28))
        pygame.draw.polygon(self.surface, (60,60,60), points)

    def draw(self, elapsed, surface):
        self.rect.center = self.pos
        surface.blit(self.surface, self.rect)
    
    def pressed(self, pressed, elapsed):

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

        velocity = self.velocity if not pressed[pygame.K_LSHIFT] else self.velocity * 3

        self.pos[0] += (heading[0] * velocity) * elapsed
        self.pos[1] += (heading[1] * velocity) * elapsed

        #bounds checking
        if self.pos[0] < self.bounds.left:
            self.pos[0] = self.bounds.left
        if self.pos[0] > self.bounds.right:
            self.pos[0] = self.bounds.right
        if self.pos[1] < self.bounds.top:
            self.pos[1] = self.bounds.top
        if self.pos[1] > self.bounds.bottom:
            self.pos[1] = self.bounds.bottom

        # if self.pos[0] > 200:
            # self.pos[0] = 200
