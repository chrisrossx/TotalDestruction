
import subprocess
import sys 

from pygame import Vector2 
import pygame 

from TD.editor.config import EDITOR_SCREEN_RECT
from TD.editor import gui 
from .gui import LineButton, LineWindow
from TD.paths import path_data
from TD.editor.globals import current_level, current_app, current_scene
from TD.levels.data import LevelEntityType
from .xygrid import XYGrid
from .select_mode import SelectMode
from .draw_mode import DrawMode
from .details import Details
from .transforms import Transforms
from .move_mode import MoveMode
from .edit_mode import EditMode

class SelectPathPanel(gui.Panel):
    def __init__(self, on_select_path, page=0):
        panel_rows = 28
        panel_cols = 41 + 12
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        # size = Vector2(1024+500, 900)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "Path Editor")
        self.em.delete(self.btn_close)
        # self.mask = None
        self.mask.fill((80,80,80))
        self.mask.set_alpha(255)
        self.on_select_path = on_select_path

        self._page = page
        self.selected_line_index = None

        self.line_window = LineWindow(self.grid_pos(0,0), self)
        self.line_window.page = self._page
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

        self.btn_save_paths = gui.Button("Save", self.grid_pos(35, 25), self.grid_size(3,1))
        self.btn_save_paths.on_button_1.append(self.on_btn_save_paths)
        self.em.add(self.btn_save_paths)

        self.btn_reload_paths = gui.Button("Reload", self.grid_pos(38, 25), self.grid_size(3,1))
        self.btn_reload_paths.on_button_1.append(self.on_btn_reload_paths)
        self.em.add(self.btn_reload_paths)

        self.btn_close_no_save = gui.Button("Close Without Save", self.grid_pos(35, 24), self.grid_size())
        self.btn_close_no_save.on_button_1.append(self.on_btn_close_no_save)
        self.em.add(self.btn_close_no_save)

        self.btn_select_path_name = gui.Button("Save and Select Path Name", self.grid_pos(35, 26), self.grid_size())
        self.btn_select_path_name.on_button_1.append(self.on_btn_select_path_name)
        self.em.add(self.btn_select_path_name)

        self.btn_select_path_index = gui.Button("Save and Select Path Index", self.grid_pos(35, 27), self.grid_size())
        self.btn_select_path_index.on_button_1.append(self.on_btn_select_path_index)
        self.em.add(self.btn_select_path_index)

        self.gui_groups = {}
        self.gui_groups["xygrid"] = XYGrid(self)
        self.gui_groups["select_mode"] = SelectMode(self)
        self.gui_groups["details"] = Details(self)
        self.gui_groups["draw_mode"] = DrawMode(self)
        self.gui_groups["transforms"] = Transforms(self)
        self.gui_groups["move_mode"] = MoveMode(self)
        self.gui_groups["edit_mode"] = EditMode(self)

        self.update()

    def on_btn_close_no_save(self, btn):
        path_data.save_backup("close_without_save")
        self._cancel_button(btn)

    def show(self):
        super().show()
        self.set_gui_level
        current_scene.hide_gui_layer = current_scene.gui_layer - 1

    @property
    def path_edit_mode(self):
        return self.gui_groups["general_controls"].mode

    def on_btn_save_paths(self, btn):
        path_data.save()
        self.update()

    def on_btn_select_path_index(self, btn):
        if self.selected_line_index != None:
            path_data.save()
            self.on_select_path(self.selected_line_index)

    def on_btn_select_path_name(self, btn):
        if self.selected_line_index != None:
            path_data.save()
            path_name = path_data[self.selected_line_index].name
            self.on_select_path(path_name)

    def on_btn_reload_paths(self, btn):
        path_data.save_backup("before_reload")
        path_data.load()
        self.update()

    def on_btn_line(self, btn_index):
        btn_line = self.btns_line[btn_index]
        new_index = btn_index + (self._page * 8)
        self.gui_groups["select_mode"].clear_mode()
        if self.selected_line_index == new_index:
            self.selected_line_index = None
        else:
            self.selected_line_index = new_index
        
        for g in self.gui_groups.values():
            g.on_selected_line_index(self.selected_line_index)
        self.update()
        # btn_line.toggled = not btn_line.toggled

    def on_btn_show(self, btn_index):
        index = btn_index + (self._page * 8)
        data = path_data[index]
        data.hidden = not data.hidden
        self.update() 
        self.gui_groups["select_mode"].clear_mode()
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
        self.selected_line_index = None 
        self.gui_groups["select_mode"].clear_mode()
        self.update()

    def on_btn_pgup(self, btn):
        if self.page > 0:
            self.page -= 1
        self.selected_line_index = None 
        self.gui_groups["select_mode"].clear_mode()
        self.update()

    def update(self):
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

        for g in self.gui_groups.values():
            g.update()
        # self.gui_groups["xygrid"].update()
        # self.gui_groups["edit_mode"].update()

    def on_event(self, event, elapsed):
        super().on_event(event, elapsed)
        for g in self.gui_groups.values():
            if hasattr(g, "on_event"):
                g.on_event(event, elapsed)

    def tick(self, elapsed):
        super().tick(elapsed)
        for g in self.gui_groups.values():
            g.tick(elapsed)

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        for g in self.gui_groups.values():
            g.draw(elapsed, surface)
        
        s = 2
        for x in [self.btn_select_path_index.rect.right + s]:
            y = self.pos.y + 34
            pygame.draw.line(surface, (80,80,80), (x, y), (x, self.rect.bottom -2))


