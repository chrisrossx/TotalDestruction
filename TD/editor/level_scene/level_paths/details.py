from enum import Enum

from pygame import Vector2

from TD.editor import gui 
from TD.paths import path_data
from .gui_group import PanelGUIGroup

class Details(PanelGUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self.page = 0

        self.txt_name = gui.TextBox("", self.grid_pos(41, 1), self.grid_size(6, 1), "Name: ")
        self.txt_name.on_value_changed.append(self.on_txt_name)
        self.em.add(self.txt_name)

        self.txt_index = gui.TextBox("0", self.grid_pos(41, 2), self.grid_size(2, 1), "#: ")
        self.txt_index.editable = False 
        self.em.add(self.txt_index)

        self.txt_segments = gui.TextBox("", self.grid_pos(43, 2), self.grid_size(4, 1), "Segments: ")
        self.txt_segments.editable = False
        self.em.add(self.txt_segments)

        self.txt_total_length = gui.TextBox("", self.grid_pos(41, 3), self.grid_size(3, 1), "Len: ")
        self.txt_total_length.editable = False 
        self.em.add(self.txt_total_length)

        self.txt_points = gui.TextBox("", self.grid_pos(44, 3), self.grid_size(3, 1), "Pt: ")
        self.txt_points.editable = False 
        self.em.add(self.txt_points)


        self.txt_cursor_position = gui.TextBox("", self.grid_pos(41, 0), self.grid_size(6, 1), "Cursor: ")
        self.txt_cursor_position.editable = False
        self.em.add(self.txt_cursor_position)


        self.update()

    def tick(self, elapsed):
        super().tick(elapsed)
        
        if self.parent.line_window.cursor == None:
            self.txt_cursor_position.text = "---, ---"
        else:
            pos = self.parent.line_window.cursor
            self.txt_cursor_position.text = "{}, {}".format(int(round(pos[0], 0)), int(round(pos[1], 0)))

    def on_txt_name(self, txt):
        path_data = self.get_path_data()
        path_data.name = txt.text
        self.parent.update()

    def on_selected_line_index(self, selected_line_inedx):
        pass

    def update(self):
        
        self.txt_name.disabled = True if self.parent.selected_line_index == None else False
        self.txt_total_length.disabled = True if self.parent.selected_line_index == None else False
        self.txt_segments.disabled = True if self.parent.selected_line_index == None else False
        self.txt_index.disabled = True if self.parent.selected_line_index == None else False
        self.txt_points.disabled = True if self.parent.selected_line_index == None else False

        if self.parent.selected_line_index == None:
            self.txt_name.text = ""
            self.txt_index.text = ""
            self.txt_points.text = ""
            self.txt_segments.text = ""
            self.txt_total_length.text = ""
        else:
            data = path_data[self.parent.selected_line_index]
            self.txt_name.text = data.name
            self.txt_index.text = str(self.selected_line_index)
            self.txt_total_length.text = "{:.02f}".format(data.total_length)
            self.txt_segments.text = "{}".format(len(data.length))
            self.txt_points.text = "{}".format(len(data.points))
