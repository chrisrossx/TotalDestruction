import pygame
from pathlib import Path
import math


class Background:
    def __init__(self, size, velocity=[-0.1, 0.0]):
        """
        Background Object, Create Parallax Scrolling Clouds
        """
        self.size = size


        self.sky = pygame.image.load(Path("assets/layered.jpg"))
        self.sky.convert()
        self.rect = self.sky.get_rect()
        self.offset = [0, 0]
        self.velocity = velocity

    def draw(self, elapsed, surface):
        x_count = math.ceil((self.size[0] - self.offset[0]) / self.rect.w)
        y_count = math.ceil((self.size[1] - self.offset[1]) / self.rect.h)
        for x in range(x_count):
            for y in range(y_count):
                x_px = (x * self.rect.w) + self.offset[0]
                y_px = (y * self.rect.h) + self.offset[1]
                surface.blit(self.sky, (x_px, y_px))

    def tick(self, elapsed):
        for i in range(2):
            self.offset[i] += elapsed * self.velocity[i]
            if self.offset[i] > 0:
                self.offset[i] -= self.rect[i+2]
            if self.offset[i] < -self.rect[i+2]:
                self.offset[i] += self.rect[i+2]


class Ship:
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


class NeverEndingLevel:

    def __init__(self, size):
        self.surface = pygame.Surface(size)
        self.sky = Background(size)
        
        self.ship = Ship(size)




        # self.T8 = pygame.image.load()
        self.T8 = pygame.image.load(Path("assets/TD T-8.png"))
        self.T8.convert()
        self.CX5 = pygame.image.load(Path("assets/TD CX-5.png"))
        self.CX5.convert()
        # self.pos = (0, 0)

    def tick(self, elapsed):
        self.sky.tick(elapsed)


    def pressed(self, pressed, elapsed):
        self.ship.pressed(pressed, elapsed)

    def on_event(self, event, elapsed):
        pass
        # self.ship.on_event(event, elapsed)

    def draw(self, elapsed):
        self.surface.fill((0,0,0))

        #fill background with Sky Texture
        self.sky.draw(elapsed, self.surface)
        self.surface.blit(self.T8, (400,200))
        self.surface.blit(self.CX5, (400,280))
        self.ship.draw(elapsed, self.surface)
       

        

        # rect = pygame.Rect(self.pos[0]-25, self.pos[1]-25, 50, 50)
        # pygame.draw.rect(self.surface, (80, 80, 80), rect)


class TD:

    def __init__(self):
        # self.size = (640, 480)
        self.size = (1024, 600)

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 24)


    def run(self):

        scene = NeverEndingLevel(self.size)
        self.clock.tick()
        running = True

        frame_count = 0
        frame_count_elapsed = 0
        frame_count_surface = self.font.render("---", True, (255, 255, 0))


        while running:
            elapsed = self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                scene.on_event(event, elapsed)
            
            pressed = pygame.key.get_pressed()
            scene.pressed(pressed, elapsed)

            if running:
                scene.tick(elapsed)
            
                scene.draw(elapsed)
                self.screen.blit(scene.surface, (0,0))

                #render fps
                frame_count += 1
                frame_count_elapsed += elapsed
                if frame_count_elapsed >= 1000:
                    # frame_count_last = frame_count
                    frame_count_surface = self.font.render(str(frame_count), True, (255, 255, 0))
                    frame_count = 0
                    frame_count_elapsed = 0.0

                
                if frame_count_surface:
                    self.screen.blit(frame_count_surface, (20, 20))

                pygame.display.flip()


if __name__ == "__main__":
    app = TD()
    app.run()
