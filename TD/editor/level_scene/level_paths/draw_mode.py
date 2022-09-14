from dis import dis
from pygame import Vector2
import pygame 

from TD.editor.scene import GUIGroup
from TD.editor import gui 
from TD.paths import path_data
from TD.editor.globals import current_scene
from .select_mode import PathEditMode
from .gui_group import PanelGUIGroup

class DrawMode(PanelGUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self.lbl_draw = gui.Label("Draw Mode", self.grid_pos(41, 6), self.grid_size(3, 1))
        self.em.add(self.lbl_draw)

        self.btn_delete_last_point = gui.Button("Delete Last Point", self.grid_pos(41, 7), self.grid_size())
        self.btn_delete_last_point.on_button_1.append(self.on_btn_delete_last_point)
        self.em.add(self.btn_delete_last_point)

        self.update()

    def on_btn_delete_last_point(self, btn):
        path_data = self.get_path_data()
        if len(path_data.points) > 0:
            path_data.points.pop()
            path_data.calculate()
            self.parent.update()

    def update(self):

        if self.parent.selected_line_index == None:
            hidden = False
        else:
            path_data = self.get_path_data()
            hidden = path_data.hidden        
        disabled = True if self.parent.selected_line_index == None or hidden == True else False
        self.lbl_draw.disabled = disabled

        if self.path_edit_mode == PathEditMode.DRAW:
            self.btn_delete_last_point.disabled = False
        else:
            self.btn_delete_last_point.disabled = True 

    def start_draw_mode(self):
        # self.update()
        pass

    def end_draw_mode(self):
        # self.update()
        pass

    def add_point(self, pos):
        path_data = self.get_path_data()
        path_data.points.append((pos.x, pos.y))
        path_data.calculate() 
        self.parent.update()

    def on_event(self, event, elapsed):
        if current_scene.gui_layer <= self.parent.line_window.gui_layer:
            if self.path_edit_mode == PathEditMode.DRAW:
                if event.type == pygame.MOUSEBUTTONDOWN and self.parent.line_window.rect.collidepoint(event.pos):
                    # pos = event.pos - self.parent.line_window.pos - Vector2(100, 100)
                    pos = self.parent.line_window.cursor
                    self.add_point(pos)
            if self.path_edit_mode == PathEditMode.DRAW:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.on_btn_delete_last_point(None)

            if self.path_edit_mode == PathEditMode.DRAW:
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN):
                    # self.on_btn_delete_last_point(None)
                    self.parent.gui_groups["select_mode"].clear_mode()

