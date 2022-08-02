import pygame 

class DebugDisplay:
    def __init__(self):

        self.surface = None
        self.font = None
        self.frame_count = 0
        self.frame_count_elapsed = 0
        self.frame_count_surface = None
        self.line1 = None
        self.line2 = None
        self.show_panel = True 

    def load(self):
        self.surface = pygame.Surface((200,200), pygame.SRCALPHA, 32)
        self.font = pygame.font.SysFont("consolas", 12)
        self.frame_count = 0
        self.frame_count_elapsed = 0
        self.frame_count_surface = self.font.render("---", True, (255, 255, 0))

    def tick(self, elapsed):
        #render fps
        self.frame_count += 1
        self.frame_count_elapsed += elapsed
        if self.frame_count_elapsed >= 1000:
            # frame_count_last = frame_count
            self.frame_count_surface = self.font.render(str(self.frame_count), True, (255, 255, 0))
            self.frame_count = 0
            self.frame_count_elapsed = 0.0
        
    def on_event(self, event, elapsed):
        if event.type == pygame.KEYDOWN and event.key == 96:
            self.show_panel = not self.show_panel

    def draw(self, elapsed):
        # self.surface.fill((0,0,0,100))

        self.surface.fill((0,0,0,0))
        if self.show_panel:
            if self.frame_count_surface:
                self.surface.blit(self.frame_count_surface, (10, 10))
            if self.line1:
                #TODO Could optomize this by cacheing rendered text, only update when set
                line = self.font.render(self.line1, True, (255, 255, 0))
                self.surface.blit(line, (10, 25))
            if self.line2:
                line = self.font.render(self.line2, True, (255, 255, 0))
                self.surface.blit(line, (10, 40))

debug_display = DebugDisplay()
