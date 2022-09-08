from pygame import Vector2
import pygame
from TD import editor
from TD.config import SCREEN_SIZE, SKY_VELOCITY, SCREEN_RECT
from TD.editor.config import EDITOR_SCREEN_RECT, EDITOR_SCREEN_SIZE

from TD.editor.scene import Scene, GUIGroup
from TD.entity import EntityType, Entity
from .sky import Sky
from TD.editor import gui
from TD.editor.config import EDITOR_SCREEN_SIZE
from TD.assetmanager import asset_manager
from TD.editor.globals import current_level
from TD.paths import path_data
from TD.editor.editorassets import editor_assets
from TD.levels.data import LevelEntityType

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
    def __init__(self, pos):
        size = SCREEN_SIZE + Vector2(200, 200)
        super().__init__(pos, size)
        self.pos.x -= 4
        # self.frames = [pygame.Surface(size)]
        self.type = EntityType.GUI

        # self.surface_lines = pygame.surface((self.surface.get_rect().w, self.surface.get_rect().h), pygame.SRCALPHA)

        self.page = 0

    def draw(self, elapsed, surface):
        self.surface.fill((0,0,0))
        pygame.draw.rect(self.surface, (255,255,255), (100,100,1024,600), 1)
        for i in range(8):
            index = i + (self.page * 8)
            data = path_data[index]
            if not data.hidden:
                points = []
                for data_point in data.points:
                    point = data_point + Vector2(100, 100)
                    points.append(point)
                    pygame.draw.circle(self.surface, COLORS[i], point, 3)
                if len(points) > 1:
                    pygame.draw.lines(self.surface, COLORS[i], False, points, 1)

        super().draw(elapsed, surface)

class SelectPathPanel(gui.Panel):
    def __init__(self, on_select_path):
        panel_rows = 28
        panel_cols = 41
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        # size = Vector2(1024+500, 900)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "Select Path Index")

        self.on_select_path = on_select_path

        self.line_window = LineWindow(self.grid_pos(0,0))
        self.em.add(self.line_window)


        btn_pgup = gui.Button("PgUp", self.grid_pos(35,0), self.grid_size(3, 1), "center")
        btn_pgup.on_button_1.append(self.on_btn_pgup)
        self.em.add(btn_pgup)

        btn_pgdn = gui.Button("PgDn", self.grid_pos(38,0), self.grid_size(3, 1), "center")
        btn_pgdn.on_button_1.append(self.on_btn_pgdn)
        self.em.add(btn_pgdn)

        self.btns_show = []
        self.btns_line = []
        for i in range(8):
            btn_show = gui.ShowButton(self.grid_pos(35,1+(i*2)), self.grid_size(1,2), align="center")
            btn_show.on_button_1.append(lambda btn, index=i: self.on_btn_show(index))
            self.em.add(btn_show)
            btn_line = LineButton(i, "", self.grid_pos(36, 1+(i*2)), self.grid_size(5, 2), "left")
            btn_line.on_button_1.append(lambda btn, index=i: self.on_btn_line(index))
            self.em.add(btn_line)
            self.btns_show.append(btn_show)
            self.btns_line.append(btn_line)

        self._page = 0
        self.selected_line_index = None
        self.update_lines()

        self.btn_save_paths = gui.Button("Save", self.grid_pos(35, 25), self.grid_size(3,1))
        self.btn_save_paths.on_button_1.append(self.on_btn_save_paths)
        self.em.add(self.btn_save_paths)

        self.btn_reload_paths = gui.Button("Reload", self.grid_pos(38, 25), self.grid_size(3,1))
        self.btn_reload_paths.on_button_1.append(self.on_btn_reload_paths)
        self.em.add(self.btn_reload_paths)

        self.btn_select_path_name = gui.Button("Select Path Name", self.grid_pos(35, 26), self.grid_size())
        self.btn_select_path_name.on_button_1.append(self.on_btn_select_path_name)
        self.em.add(self.btn_select_path_name)

        self.btn_select_path_index = gui.Button("Select Path Index", self.grid_pos(35, 27), self.grid_size())
        self.btn_select_path_index.on_button_1.append(self.on_btn_select_path_index)
        self.em.add(self.btn_select_path_index)

    def on_btn_save_paths(self, btn):
        path_data.save()
        for chain in current_level.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]:
            chain.path.set_new_path(chain.path_index)
        self.update_lines()

    def on_btn_select_path_index(self, btn):
        if self.selected_line_index != None:
            self.on_select_path(self.selected_line_index)

    def on_btn_select_path_name(self, btn):
        if self.selected_line_index != None:
            path_name = path_data[self.selected_line_index].name
            self.on_select_path(path_name)

    def on_btn_reload_paths(self, btn):
        path_data.load()
        for chain in current_level.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]:
            chain.path.set_new_path(chain.path_index)
        self.update_lines()

    def on_btn_line(self, btn_index):
        btn_line = self.btns_line[btn_index]
        self.selected_line_index = btn_index + (self._page * 8)
        self.update_lines()
        # btn_line.toggled = not btn_line.toggled

    def on_btn_show(self, btn_index):
        index = btn_index + (self._page * 8)
        data = path_data[index]
        data.hidden = not data.hidden
        self.update_lines() 
        # btn_show = self.btns_show[btn_index]
        # btn_show.toggled = not btn_show.toggled
        # print(btn_index + (self.page * 8))

    @property
    def page(self):
        return self._page 

    @page.setter
    def page(self, value):
        self._page = value 
        self.line_window.page = self._page

    def on_btn_pgdn(self, btn):
        if self.page < (256/ 8) -1:
            self.page += 1
        self.update_lines()
        self.selected_line_index = None 

    def on_btn_pgup(self, btn):
        if self.page > 0:
            self.page -= 1
        self.update_lines()
        self.selected_line_index = None 

    def update_lines(self):
        for i in range(8):
            index = i + (self._page * 8)
            data = path_data[index]
            btn_show = self.btns_show[i]
            btn_line = self.btns_line[i]
            p = len(data.points)
            d = data.total_length
            btn_line.text = "{}: p{}, d{:0.0f}\n\"{}\"".format(index, p, d, data.name)
            btn_show.toggled = not data.hidden
            if index == self.selected_line_index:
                btn_line.toggled = True 
            else:
                btn_line.toggled = False 

    # def draw(self, elapsed, surface):
    #     # super().draw(elapsed, surface)
    #     # x = self.pos.x + 1024 + 200 + 8
    #     # y = self.pos.y + 35
    #     # pygame.draw.line(surface, (80,80,80), (x,y), (x,y+820), 1)




class GUILevelPaths(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

       
        self.btn_reload_paths = gui.Button("Reload Paths", self.grid_pos(0,2), self.grid_size(3, 1))
        self.btn_reload_paths.on_button_1.append(self.on_btn_reload_paths)
        self.em.add(self.btn_reload_paths)
    
    def on_btn_reload_paths(self, btn):
        path_data.load()
        for chain in current_level.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]:
            chain.path.set_new_path(chain.path_index)

