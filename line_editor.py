from pathlib import Path
import math
import json
from pickle import FALSE
from re import T 

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
]


class UIButton:
    def __init__(self, rect, text, parent, color=None, text_color=None, hover_color=None, callback=None):
        self.text = text
        self.rect = rect 
        self.parent = parent
        self.color = (80, 80, 80) if color == None else color
        self.hover_color = (30, 30, 30) if hover_color == None else hover_color
        self.text_color = (255, 255, 255) if text_color == None else text_color
        self.line_width = 1
        self.text_offset = (8, 8)
        self.hover = False
        if callback != None:
            self.callback = callback
    
    def draw(self, elapsed, surface):
        if self.hover:
            pygame.draw.rect(surface, self.hover_color, self.rect, 0)
        pygame.draw.rect(surface, self.color, self.rect, self.line_width)
        line = self.parent.font.render(self.text, True, self.text_color)
        surface.blit(line, (self.rect.x + self.text_offset[0], self.rect.y + self.text_offset[1]))

    def tick(self, elapsed):
        pass

    def callback(self):
        raise NotImplementedError

    def clicked(self, mouse_pos):
        """check and see if mouse_pos was a click"""
        if self.rect.collidepoint(mouse_pos):
            self.callback()
        
    def hovered(self, mouse_pos):
        """check and see if mouse_pos was a hover"""
        if self.rect.collidepoint(mouse_pos):
            self.hover = True
        else:
            self.hover = False

class UILineButton(UIButton):
    def __init__(self, rect, text_1, text_2, parent, color=None, text_color=None, hover_color=None, callback=None):
        super().__init__(rect, text_1, parent, color, text_color, hover_color, callback)
        self.text_2 = "abc"
    
    def draw(self, elapsed, surface):
        if self.hover:
            pygame.draw.rect(surface, self.hover_color, self.rect, 0)
        pygame.draw.rect(surface, self.color, self.rect, self.line_width)
        line = self.parent.font.render(self.text_1, True, self.text_color)
        surface.blit(line, (self.rect.x + self.text_offset[0], self.rect.y + self.text_offset[1]))
        line = self.parent.font_sm.render(self.text_2, True, self.text_color)
        surface.blit(line, (self.rect.x + self.text_offset[0], self.rect.y + 21 + self.text_offset[1]))

class LineEditor:

    def __init__(self, size):
        self.surface = pygame.Surface(size)
        self.cursor = (0, 0)

        self.waypoints = []
        self.hide_line = []
        self.names = []
        for i in range(255):
            self.waypoints.append([])
            self.hide_line.append(False)
            self.names.append("Path {}".format(i))

        try:        
            with open(FILENAME, "r") as f:
                data = json.load(f)
            for i in range(255):
                try:
                    key = "waypoint_{}".format(i)
                    self.names[i] = data[key][0]
                    data[key].pop(0)
                    self.waypoints[i] = data[key]
                except KeyError:
                    pass
        except FileNotFoundError:
            pass
        except:
            pass
        
        self.index = 0  # Selected Line
        self.page = 0   # Which Lines to Show
        self.copied_line = [] # Buffer for copied line
        self.move_line = False # Move LIne Mode
        self.saved = True # Is File Saved
        pygame.display.set_caption("Line Editor")
        
        self.font = pygame.font.SysFont(None, 24)
        self.font = pygame.font.SysFont("consolas", 16)
        self.font_sm = pygame.font.SysFont("consolas", 14)
        
        # #########################
        # Setup Buttons

        self.buttons = []
        rect = pygame.Rect(1234, 10 , 85, 30)
        button = UIButton(rect, "PgUp".format(i-1), self, callback=self.on_page_up)
        self.buttons.append(button)
        rect = pygame.Rect(1234+95, 10 , 85, 30)
        button = UIButton(rect, "PgDn".format(i-1), self, callback=self.on_page_down)
        self.buttons.append(button)
        
        self.line_buttons = []
        for i in range(0, 8):
            rect = pygame.Rect(1224+10, 50 + (i * 57), 180, 47)
            button = UILineButton(rect, "", "", self, callback=lambda i=i: self.on_line_button(i))
            self.buttons.append(button)
            self.line_buttons.append(button)

        y = 517
        rect = pygame.Rect(1234, y, 180, 30)
        self.buttons.append(UIButton(rect, "Rename Line", self))
        y += 40
        rect = pygame.Rect(1234, y, 85, 30)
        self.buttons.append(UIButton(rect, "Copy", self, callback=self.on_copy))
        rect = pygame.Rect(1234+95, y, 85, 30)
        self.buttons.append(UIButton(rect, "Paste", self, callback=self.on_paste))
        y += 40
        rect = pygame.Rect(1234, y, 85, 30)
        self.show_button = UIButton(rect, "[x] Show", self, callback=self.on_show)
        self.buttons.append(self.show_button)
        rect = pygame.Rect(1234+95, y, 85, 30)
        self.move_button = UIButton(rect, "[ ] Move", self, callback=self.on_move)
        self.buttons.append(self.move_button)
        y += 40
        rect = pygame.Rect(1234, y, 180, 30)
        self.buttons.append(UIButton(rect, "Delete Last Point", self, callback=self.on_delete_last))
        y += 40
        rect = pygame.Rect(1234, y, 180, 30)
        self.buttons.append(UIButton(rect, "Clear Line", self, callback=self.on_clear))
        y += 40
        rect = pygame.Rect(1234, y, 180, 30)
        self.saved_button = UIButton(rect, "[x] Save", self, callback=self.save)
        self.buttons.append(self.saved_button)
        y = 800-40
        rect = pygame.Rect(1234, y, 180, 30)
        self.buttons.append(UIButton(rect, "Exit", self, callback=self.on_exit))

        self.page_changed()

    def on_copy(self):
        self.copied_line = [p for p in self.waypoints[self.index]]
    
    def on_paste(self):
        if not self.hide_line[self.index]:
            if len(self.copied_line) > 0:
                self.waypoints[self.index] = self.copied_line
                self.update_line_buttons()
                self.not_saved()

    def on_delete_last(self):
        if not self.hide_line[self.index]:
            self.waypoints[self.index].pop()
            self.update_line_buttons()
            self.not_saved()

    def on_clear(self):
        if not self.hide_line[self.index]:
            self.waypoints[self.index] = []
            self.update_line_buttons()
            self.not_saved()
    
    def on_move(self):
        self.move_line = not self.move_line
        t = "x" if self.move_line else " "
        self.move_button.text = "[{}] Move".format(t)

    def clear_move(self):
        self.move_line = False
        self.move_button.text = "[ ] Move"

    def on_show(self):
        self.hide_line[self.index] = not self.hide_line[self.index]
        self.update_line_buttons()
        self.update_show_button()
    
    def update_show_button(self):
        if self.hide_line[self.index]:
            text = "[ ] Show"
        else:
            text = "[x] Show"
        self.show_button.text = text
        
    def on_exit(self):
        import sys
        sys.exit()

    def on_page_up(self):
        if self.page > 0:
            self.page -= 1
            self.index -= 8
        self.page_changed()

    def on_page_down(self):
        if self.page < (255 / 8) - 2:
            self.page += 1
            self.index += 8
        self.page_changed()
    
    def update_line_buttons(self):
        for i, button in enumerate(self.line_buttons):
            index = (self.page * 8) + i
            h = " " if self.hide_line[index] else "x"
            button.text_1 = "[{}] Path {}: {}".format(h, index, len(self.waypoints[index]))
            button.text_2 = "\"{}\"".format(self.names[index])
            button.text_color = COLORS[i]

    def page_changed(self):
        self.update_line_buttons()
        self.index = (self.page * 8)
        self.select_line_button(self.line_buttons[0])

    def select_line_button(self, selected_button):
        for button in self.buttons:
            button.line_width = 1
            button.color = (80, 80, 80)
        selected_button.line_width = 4
        selected_button.color = (255, 80, 80)
        self.update_show_button()

    def on_line_button(self, button_index):
        self.index = (self.page * 8) + button_index
        self.select_line_button(self.line_buttons[button_index])

    def not_saved(self):
        self.saved = False
        self.saved_button.text = "[ ] Save"
        pygame.display.set_caption("[Not Saved] - Line Editor")

    def tick(self, elapsed):
        pass

    def pressed(self, pressed, elapsed):
        pass

    def on_event(self, event, elapsed):
        if event.type == pygame.MOUSEMOTION:
            self.cursor = event.pos
            for button in self.buttons:
                button.hovered(self.cursor)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cursor = event.pos
            if self.cursor[0] <= 1224:
                if not self.hide_line[self.index]:
                    self.not_saved()
                    x, y = self.cursor[0] - 100, self.cursor[1] - 100
                    if self.move_line and len(self.waypoints[self.index]) > 0:
                        tx = self.waypoints[self.index][0][0] - x
                        ty = self.waypoints[self.index][0][1] - y
                        new_waypoints = []
                        for old_waypoint in self.waypoints[self.index]:
                            nx = old_waypoint[0] - tx
                            ny = old_waypoint[1] - ty
                            new_waypoints.append((nx, ny))
                        self.waypoints[self.index] = new_waypoints
                        self.clear_move()
                    else:
                        self.waypoints[self.index].append((x, y))
                    self.update_line_buttons()
            else:
                for button in self.buttons:
                    button.clicked(self.cursor)

    def save(self):
        data = {}
        with open(FILENAME, "w") as f:
            f.write("{\n")
            for i in range(255):
                key = "waypoint_{}".format(i)
                name_list = []
                name_list.append(self.names[i])
                name_list = name_list + self.waypoints[i]
                l = json.dumps(name_list)
                comma = "," if i < 254 else ""
                f.write("\"{}\": {}{}\n".format(key, l, comma))
            f.write("}\n")
        print("Saved")
        self.saved_button.text = "[x] Save"
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

        
        for i in range(8):
            
            color = COLORS[i]
            index = (self.page * 8) + i
            if not self.hide_line[index]:
                waypoints = [(x+100, y+100) for x, y in self.waypoints[index]]
                if len(waypoints) > 1:

                    pygame.draw.lines(self.surface, color, False, waypoints)
                for i in range(len(waypoints)):
                    pygame.draw.circle(self.surface, color, waypoints[i], 3)
                        

        self.screen_rect = pygame.Rect(100, 100, 1024, 600)

        pygame.draw.rect(self.surface, (80,80,80), self.screen_rect, 1)
        pygame.draw.line(self.surface, (80,80,80), (1224, 0), (1224,800))
        pygame.draw.line(self.surface, (80,80,80), (1224, 507), (1424,507))

        for button in self.buttons:
            button.draw(elapsed, self.surface)

        # for i in range(len(self.button_rects)):
        #     if i == 10:
        #         line = self.font.render("Clear Line", True, color)
            
        #     if i == 11:
        #         line = self.font.render("Delete Last Point", True, color)

        #     if i == 12:
        #         line = self.font.render("Copy Line", True, color)

        #     if i == 13:
        #         line = self.font.render("Paste Line", True, color)
        #     if i == 14:
        #         line = self.font.render("Show/Hide Line", True, color)
        #     if i == 15:
        #         m = "x" if self.move_line else " "
        #         line = self.font.render("[{}] Move Line".format(m), True, color)
        #     if i == 16:
        #         s = "x" if self.saved else " "
        #         line = self.font.render("[{}] Save".format(s), True, color)
        #     if i == 17:
        #         line = self.font.render("Exit", True, color)
            
        #     x = rect.x + 8
        #     y = rect.y + 8
        #     self.surface.blit(line, (x, y))

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
