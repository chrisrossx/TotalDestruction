from pathlib import Path
import math
import json 

import pygame
from blinker import signal

FILENAME = "line_editor.json"

COLORS = [
    (230, 25, 75),
    (60, 180, 75), 
    (255, 225, 25), 
    (0, 130, 200), 
    (245, 130, 48),
    (145, 30, 180),
    (70, 240, 240),
    (128, 128, 0),
    (170, 110, 40),

    (250, 190, 212),
    (0, 128, 128),
    (220, 190, 255),
    (240, 50, 230),
    (255, 250, 200),
    (128, 0, 0),
    (210, 245, 60),
    (170, 255, 195),
    (255, 215, 180),
    (0, 0, 128),
    (128, 128, 128),
    (255, 255, 255),
    
    (255, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (252, 186, 3),
    (209, 138, 90),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (144, 3, 252),
    (202, 252, 3),
]

class LineEditor:

    def __init__(self, size):
        self.surface = pygame.Surface(size)
        self.cursor = (0, 0)

        self.waypoints = []
        self.hide_line = []
        for i in range(10):
            self.waypoints.append([])
            self.hide_line.append(False)

        try:        
            with open(FILENAME, "r") as f:
                data = json.load(f)
            for i in range(10):
                try:
                    key = "waypoint_{}".format(i)
                    self.waypoints[i] = data[key]
                except KeyError:
                    pass
        except FileNotFoundError:
            pass
        
        self.index = 0
        
        self.font = pygame.font.SysFont(None, 24)

        self.button_rects = []
        for i in range(18):
            rect = pygame.Rect(1224+10, 10 + (i * 40), 180, 30)
            self.button_rects.append(rect)

        self.copied_line = []
        self.move_line = False
        self.saved = True
        pygame.display.set_caption("Line Editor")

    def not_saved(self):
        self.saved = False
        pygame.display.set_caption("[Not Saved] - Line Editor")

    def tick(self, elapsed):
        pass

    def pressed(self, pressed, elapsed):
        pass

    def on_event(self, event, elapsed):
        if event.type == pygame.MOUSEMOTION:
            self.cursor = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cursor = event.pos
            if self.cursor[0] <= 1224:
                if self.move_line and len(self.waypoints[self.index]) > 0:
                    tx = self.waypoints[self.index][0][0] - self.cursor[0]
                    ty = self.waypoints[self.index][0][1] - self.cursor[1]
                    new_waypoints = []
                    for old_waypoint in self.waypoints[self.index]:
                        nx = old_waypoint[0] - tx
                        ny = old_waypoint[1] - ty
                        new_waypoints.append((nx, ny))
                    self.waypoints[self.index] = new_waypoints
                    self.not_saved()
                else:
                    self.not_saved()
                    self.waypoints[self.index].append(event.pos)
            else:
                for i in range(len(self.button_rects)):
                    button = self.button_rects[i]
                    if button.collidepoint(self.cursor):
                        if i >= 0 and i <= 9:
                            self.index = i
                        if i == 10:
                            self.waypoints[self.index] = []
                            self.not_saved()
                        if i == 11:
                            self.waypoints[self.index].pop()
                            self.not_saved()
                        if i == 12:
                            self.copied_line = [p for p in self.waypoints[self.index]]
                        if i == 13:
                            self.waypoints[self.index] = self.copied_line
                            self.not_saved()
                        if i == 14:
                            self.hide_line[self.index] = not self.hide_line[self.index]
                        if i == 15:
                            self.move_line = not self.move_line
                        if i == 16:
                            self.save()
                        if i == 17:
                            import sys
                            sys.exit()

    def save(self):
        data = {}
        with open(FILENAME, "w") as f:
            f.write("{\n")
            for i in range(10):
                key = "waypoint_{}".format(i)
                l = json.dumps(self.waypoints[i])
                comma = "," if i < 9 else ""
                f.write("\"{}\": {}{}\n".format(key, l, comma))
            f.write("}\n")
        print("Saved")
        self.saved = True

    def draw(self, elapsed):
        self.surface.fill((0,0,0))
        if self.cursor[0] <= 1224:
            # pygame.draw.circle(self.surface, (255,0,0), self.cursor, 5)
            c = (255, 255, 255)
            x, y = self.cursor
            d = 5
            p1 = (x, y-d)
            p2 = (x, y+d)
            pygame.draw.line(self.surface, c, p1, p2, 1)
            p1 = (x-d, y)
            p2 = (x+d, y)
            pygame.draw.line(self.surface, c, p1, p2, 1)

        
        for i in range(len(self.waypoints)):
            color = COLORS[i]
            waypoints = self.waypoints[i]
            if not self.hide_line[i]:
                if len(waypoints) > 1:
                    pygame.draw.lines(self.surface, color, False, waypoints)
                for i in range(len(waypoints)):
                    pygame.draw.circle(self.surface, color, waypoints[i], 3)
                        

        self.screen_rect = pygame.Rect(100, 100, 1024, 600)

        pygame.draw.rect(self.surface, (80,80,80), self.screen_rect, 1)
        pygame.draw.line(self.surface, (80,80,80), (1224, 0), (1224,800))

        for i in range(len(self.button_rects)):
            rect = self.button_rects[i]
            b_color = (80,80,80)
            if i <= 9:
                
                if self.index == i:
                    width = 5 
                    b_color = (120, 120, 120)
                else:
                    width = 1
            else:
                width = 1
            pygame.draw.rect(self.surface, b_color, rect, width)
            
            color = (255, 255, 255)
            if i <= 9:
                color = COLORS[i]
                h = " " if self.hide_line[i] else "x"
                line = self.font.render("[{}] Waypoint {}: {}".format(h, i, len(self.waypoints[i])), True, color)

            if i == 10:
                line = self.font.render("Clear Line", True, color)
            
            if i == 11:
                line = self.font.render("Delete Last Point", True, color)

            if i == 12:
                line = self.font.render("Copy Line", True, color)

            if i == 13:
                line = self.font.render("Paste Line", True, color)
            if i == 14:
                line = self.font.render("Show/Hide Line", True, color)
            if i == 15:
                m = "x" if self.move_line else " "
                line = self.font.render("[{}] Move Line".format(m), True, color)
            if i == 16:
                s = "x" if self.saved else " "
                line = self.font.render("[{}] Save".format(s), True, color)
            if i == 17:
                line = self.font.render("Exit", True, color)
            
            x = rect.x + 8
            y = rect.y + 8
            self.surface.blit(line, (x, y))

            line = self.font.render("({}, {})".format(self.cursor[0]- 100, self.cursor[1]-100), True, (180,180,180))
            self.surface.blit(line, (5,5))
               
        

class TD:

    def __init__(self):
        # self.size = (640, 480)
        self.size = (1024+400, 600+200)

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Line Editor")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 24)


    def run(self):

        scene = LineEditor(self.size)
        self.clock.tick()
        running = True

        frame_count = 0
        frame_count_elapsed = 0
        frame_count_surface = self.font.render("---", True, (255, 255, 0))


        while running:
            elapsed = self.clock.tick(60)

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

                
                # if frame_count_surface:
                    # self.screen.blit(frame_count_surface, (20, 20))

                pygame.display.flip()


if __name__ == "__main__":
    app = TD()
    app.run()
