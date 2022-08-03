import pygame 

class GameDebugger:
    def __init__(self):

        self.surface = None
        self.font = None
        self.frame_count = 0
        self.frame_count_elapsed = 0
        self.frame_count_surface = None
        self.lines = [None for i in range(10)]

        self.show_panel = True 

        self.show_sky = False
        self.show_hitboxs = True
        self.show_paths = not True

    def load(self):
        self.surface = pygame.Surface((200,200), pygame.SRCALPHA, 32)
        self.font = pygame.font.SysFont("consolas", 12)
        self.frame_count = 0
        self.frame_count_elapsed = 0
        self.frame_count_surface = self.font.render("---", True, (255, 255, 0))

    def tick(self, elapsed):

        #fps
        self.frame_count += 1
        self.frame_count_elapsed += elapsed
        if self.frame_count_elapsed >= 1000:
            self.frame_count_surface = self.font.render(str(self.frame_count), True, (255, 255, 0))
            self.frame_count = 0
            self.frame_count_elapsed = 0.0
        
    def on_event(self, event, elapsed):
        if event.type == pygame.KEYDOWN:
            if event.key == 96:
                self.show_panel = not self.show_panel

            if event.key == pygame.K_s:
                if self.show_panel :
                    self.show_sky = not self.show_sky

            if event.key == pygame.K_h:
                if self.show_panel:
                    self.show_hitboxs = not self.show_hitboxs

            if event.key == pygame.K_p:
                if self.show_panel:
                    self.show_paths = not self.show_paths

    def draw(self, elapsed):

        self.surface.fill((0,0,0,0))
        if self.show_panel:
            if self.frame_count_surface:
                self.surface.blit(self.frame_count_surface, (10, 10))
            for i in range(10):
                line = self.lines[i]
                if line:
                    #TODO Could optomize this by cacheing rendered text, only update when set
                    surface = self.font.render(line, True, (255, 255, 0))
                    self.surface.blit(surface, (10, (i * 17)+25))

game_debugger = GameDebugger()
