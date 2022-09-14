import math 

from pygame import Vector2
import pygame

from TD.editor.level_scene.level_paths.select_mode import PathEditMode 
from .colors import COLORS 
from TD.config import SCREEN_SIZE
from TD.entity import EntityType
from TD.paths import path_data
from TD.editor import gui 
from TD.editor.globals import current_scene


class LineButton(gui.Button):
    def __init__(self, index, text, pos, size, align="left"):
        super().__init__(text, pos, size, align)
        self.font_color = COLORS[index]
        self.font_toggled_color = COLORS[index]
        self.border_toggled_color = (255, 0, 0)
        self.background_toggled_color = self.background_color
        self.background_toggled_hovered_color = self.background_hover_color
        self.render()

    @property
    def toggled(self):
        return self._toggled

    @toggled.setter
    def toggled(self, value):
        if self._toggled != value:
            self._toggled = value 
            if self._toggled:
                self._border_width = 3
            else:
                self._border_width = 1
            self.render()


class LineWindow(gui.GuiEntity):
    def __init__(self, pos, panel):
        size = SCREEN_SIZE + Vector2(200, 200)
        super().__init__(pos, size)
        self.pos.x -= 4
        self.type = EntityType.GUI
        self.parent = panel 
        self.cursor = Vector2(0, 0)

        self.page = 0
        self.cursor = None 

    def set_cursor(self, pos):
        self.cursor = pos

        if self.path_edit_mode == PathEditMode.DRAW and self.cursor != None:
            kmods = pygame.key.get_mods()
            if kmods & pygame.KMOD_CTRL:
                # self.cursor = Vector2(0, 0)
                data = path_data[self.parent.selected_line_index]
                if len(data.points) > 0:
                    mpos = pos
                    last_point = Vector2(data.points[-1])
                    distance = abs(last_point.distance_to(mpos))
                    dx = mpos.x - last_point.x
                    dy = mpos.y - last_point.y
                    rads = math.atan2(dy, dx)
                    rads %= 2 * math.pi 
                    degs = math.degrees(rads)

                    orths = [0, 45, 90, 135, 180, 225, 270, 315, 360]
                    closest_d = 360
                    closestt_degs = None 
                    for o in orths:
                        d = abs(degs - o)
                        if d < closest_d:
                            closest_d = d 
                            closestt_degs = o
                    cursor = Vector2(distance, 0)
                    cursor.rotate_ip(closestt_degs)
                    cursor = cursor + last_point 
                    self.cursor = cursor

    def on_event(self, event, elapsed):
        if current_scene.gui_layer <= self.gui_layer:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    pos = Vector2(event.pos) - self.pos - Vector2(100, 100)
                    self.set_cursor(pos)
                else:
                    self.set_cursor(None)

    def draw(self, elapsed, surface):
        selected_color=(255,255,255)
        self.surface.fill((0,0,0))
        
        # if current_scene.hide_sky:
        c = (80,60,60)
        for y in range(100+150, 700, 150):
            p0 = Vector2(100, y)
            p1 = Vector2(1124, y)
            pygame.draw.line(self.surface, c, p0, p1, 1)
        for x in range(100+150, 1124, 150):
            p0 = Vector2(x, 100)
            p1 = Vector2(x, 700)
            pygame.draw.line(self.surface, c, p0, p1, 1)
        
        pygame.draw.rect(self.surface, (255,255,255), (100,100,1024,600), 1)
        for i in range(8):
            index = i + (self.page * 8)
            data = path_data[index]
            if not data.hidden:
                points = []
                for p, data_point in enumerate(data.points):
                    point = data_point + Vector2(100, 100)
                    points.append(point)
                    if p == 0:
                        x = point.x - 4
                        y = point.y - 4
                        r = pygame.Rect(x, y, 8, 8)
                        if self.parent.selected_line_index == index:
                            r2 = r.inflate(2, 2)
                            pygame.draw.rect(self.surface, selected_color, r2, 0)
                        pygame.draw.rect(self.surface, COLORS[i], r,0)

                    else:
                        if self.parent.selected_line_index == index:
                            pygame.draw.circle(self.surface, selected_color, point, 4, 1)
                        pygame.draw.circle(self.surface, COLORS[i], point, 3)
                if len(points) > 1:
                    if self.parent.selected_line_index == index:
                        # pygame.draw.lines(self.surface, selected_color, False, points, 3)
                        c = (
                            COLORS[i][0] * 0.7,
                            COLORS[i][1] * 0.7,
                            COLORS[i][2] * 0.7,
                        )
                        pygame.draw.lines(self.surface, c, False, points, 3)
                        pygame.draw.lines(self.surface, COLORS[i], False, points, 1)
                    else:
                        pygame.draw.lines(self.surface, COLORS[i], False, points, 1)
                
                if len(points) > 0 and self.parent.selected_line_index == index and self.cursor != None and self.path_edit_mode == PathEditMode.DRAW:
                    p1 = self.cursor + Vector2(100, 100)
                    p2 = points[-1]
                    pygame.draw.line(self.surface, COLORS[i], p1, p2, 1)
                    c = (
                        COLORS[i][0] * 0.7,
                        COLORS[i][1] * 0.7,
                        COLORS[i][2] * 0.7,
                    )
                    pygame.draw.line(self.surface, COLORS[i], p1, p2, 3)
        

        for i, rect in enumerate(self.edit_mode_point_rects):

            if self.cursor != None and rect.collidepoint(self.cursor + Vector2(100, 100)):
                c = (255, 255, 255)
            elif i == self.edit_mode_selected_point_index:
                c = (255, 0, 0)
            else:
                c = (80, 80, 80)

            pygame.draw.rect(self.surface, c, rect, 1)


        super().draw(elapsed, surface)

    @property 
    def edit_mode_point_rects(self):
        return self.parent.gui_groups["edit_mode"].point_rects

    @property 
    def edit_mode_selected_point_index(self):
        return self.parent.gui_groups["edit_mode"].selected_point_index

    @property
    def path_edit_mode(self):
        return self.parent.gui_groups["select_mode"].mode
