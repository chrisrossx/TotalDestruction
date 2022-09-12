from dis import dis
from pygame import Vector2
import pygame 

from TD.editor.scene import GUIGroup
from TD.editor import gui 
from TD.paths import path_data
from TD.editor.globals import current_scene
from .select_mode import PathEditMode
from .gui_group import PanelGUIGroup

class MoveMode(PanelGUIGroup):
    def __init__(self, parent):
        super().__init__(parent)


        self.update()

    def update(self):
        pass

    def start_move_mode(self):
        pass

    def end_move_mode(self):
        pass

    def move_path(self, pos):
        # self.clear_mode()
        path_data = self.get_path_data()
        if len(path_data.points) > 0:
            delta = pos - Vector2(path_data.points[0])
            for i in range(len(path_data.points)):
                point = Vector2(path_data.points[i])
                point += delta 
                path_data.points[i] = [round(point.x, 0), round(point.y, 0)]
            path_data.calculate()
            self.parent.update()
        

    def on_event(self, event, elapsed):
        pass
        if current_scene.gui_layer <= self.parent.line_window.gui_layer:
            if self.path_edit_mode == PathEditMode.MOVE:
                if event.type == pygame.MOUSEBUTTONDOWN and self.parent.line_window.rect.collidepoint(event.pos):
                    self.move_path(self.parent.line_window.cursor)
