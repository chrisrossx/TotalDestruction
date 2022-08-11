from blinker import signal
import pygame 


class GameDebugger:
    def __init__(self):

        self.surface = None
        self.font = None
        self.frame_count = 0
        self.frame_count_elapsed = 0
        self.frame_count_surface = None
        self.lines = [None for i in range(20)]

        self.show_panel = True 

        self.show_sky = True
        self.show_hitboxes = not True
        self.show_paths = not True
        self.show_bounds = not True 

        self.disable_input = 0
        signal("debugger.disable_input").connect(self.on_disable_input)
        signal("debugger.enable_input").connect(self.on_enable_input)

    def on_disable_input(self, sender):
        self.disable_input += 1

    def on_enable_input(self, sender):
        self.disable_input -= 1

    def load(self):
        self.surface = pygame.Surface((200,300), pygame.SRCALPHA, 32)
        self.font = pygame.font.SysFont("consolas", 12)
        self.frame_count = 0
        self.frame_count_elapsed = 0
        self.frame_count_surface = self.font.render("---", True, (255, 255, 0))

    def tick(self, elapsed):

        #fps
        if self.show_panel == 1 or self.show_panel == 2:
            self.frame_count += 1
            self.frame_count_elapsed += elapsed
            if self.frame_count_elapsed >= 1000:
                self.frame_count_surface = self.font.render(str(self.frame_count), True, (255, 255, 0))
                self.frame_count = 0
                self.frame_count_elapsed = 0.0
            
    def on_event(self, event, elapsed):
        if self.disable_input == 0 and event.type == pygame.KEYDOWN:
            if event.key == 96:
                if self.show_panel == None:
                    self.show_panel = 1
                elif self.show_panel == 1:
                    self.show_panel = 2
                else:
                    self.show_panel = None
                # self.show_panel = not self.show_panel

            if event.key == pygame.K_s:
                if self.show_panel :
                    self.show_sky = not self.show_sky

            if event.key == pygame.K_h:
                if self.show_panel:
                    self.show_hitboxes = not self.show_hitboxes

            if event.key == pygame.K_p:
                if self.show_panel:
                    self.show_paths = not self.show_paths

            if event.key == pygame.K_e:
                if self.show_panel:
                    from TD.particles.explosions import ExplosionMedium
                    signal("scene.add_entity").send(ExplosionMedium(pygame.Vector2(800,300)))

            if event.key == pygame.K_r:
                if self.show_panel:
                    from TD.particles.explosions import ExplosionMedium002
                    signal("scene.add_entity").send(ExplosionMedium002(pygame.Vector2(800,400)))

            if event.key == pygame.K_b:
                if self.show_panel:
                    self.show_bounds = not self.show_bounds

    def draw(self, elapsed):

        self.surface.fill((0,0,0,0))
        if self.show_panel:
            if self.show_panel == 1 or self.show_panel == 2:
                if self.frame_count_surface:
                    self.surface.blit(self.frame_count_surface, (10, 10))
            if self.show_panel == 1:
                for i in range(len(self.lines)):
                    line = self.lines[i]
                    if line:
                        #TODO Could optomize this by cacheing rendered text, only update when set
                        surface = self.font.render(line, True, (255, 255, 0))
                        self.surface.blit(surface, (10, (i * 17)+25))

game_debugger = GameDebugger()
