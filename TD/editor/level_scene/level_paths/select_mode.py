from dis import dis
from enum import Enum

from pygame import Vector2

from TD.editor import gui 
from .gui_group import PanelGUIGroup
from TD.paths import path_data

class PathEditMode(Enum):
    NONE = 0
    DRAW = 1 
    EDIT = 2
    MOVE = 3


class SelectMode(PanelGUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self.page = 0

        self.btn_draw = gui.Button("Draw", self.grid_pos(41, 4), self.grid_size(2, 1))
        self.btn_draw.on_button_1.append(self.on_btn_draw)
        self.em.add(self.btn_draw)
        
        self.btn_edit = gui.Button("Edit", self.grid_pos(43, 4), self.grid_size(2, 1))
        self.btn_edit.on_button_1.append(self.on_btn_edit)
        self.em.add(self.btn_edit)

        self.btn_move = gui.Button("Move", self.grid_pos(45, 4), self.grid_size(2, 1))
        self.btn_move.on_button_1.append(self.on_btn_move)
        self.em.add(self.btn_move)

        self.mode = None 

        self.update()

    def on_btn_draw(self, btn):
        if self.mode == PathEditMode.DRAW:
            self.set_new_mode(PathEditMode.NONE)
        else:
            self.set_new_mode(PathEditMode.DRAW)
        self.update()

    def on_btn_move(self, btn):
        if self.mode == PathEditMode.MOVE:
            self.set_new_mode(PathEditMode.NONE)
        else:
            self.set_new_mode(PathEditMode.MOVE)
        self.update()

    def on_btn_edit(self, btn):
        if self.mode == PathEditMode.EDIT:
            self.set_new_mode(PathEditMode.NONE)
        else:
            self.set_new_mode(PathEditMode.EDIT)
        self.update()


    def clear_mode(self):
        self.set_new_mode(PathEditMode.NONE)

    def set_new_mode(self, path_edit_mode):
        if self.mode == PathEditMode.DRAW:
            self.parent.gui_groups["draw_mode"].end_draw_mode()
        if self.mode == PathEditMode.EDIT:
            self.parent.gui_groups["edit_mode"].end_edit_mode()
        # if self.mode == PathEditMode.MOVE:
            # self.parent.gui_groups["move_mode"].end_move_mode()
       
        self.mode = path_edit_mode
        if self.mode == PathEditMode.DRAW:
            self.parent.gui_groups["draw_mode"].start_draw_mode()
        if self.mode == PathEditMode.EDIT:
            self.parent.gui_groups["edit_mode"].start_edit_mode()
        # if self.mode == PathEditMode.MOVE:
            # self.parent.gui_groups["move_mode"].start_move_mode()

        self.parent.update()

    def on_selected_line_index(self, selected_line_inedx):
        self.clear_mode()

    def update(self):
        

        if self.parent.selected_line_index == None:
            hidden = False
        else:
            path_data = self.get_path_data()
            hidden = path_data.hidden

        
        # if hidden:
            # disabled = True 
        # else:
        disabled = True if self.parent.selected_line_index == None or hidden == True else False
        self.btn_draw.disabled = disabled
        self.btn_edit.disabled = disabled
        self.btn_move.disabled = disabled 
        # self.lbl_draw.disabled = disabled
        # self.lbl_edit.disabled = disabled

        if self.mode == PathEditMode.DRAW and hidden == False :
            self.btn_draw.toggled = True 
            self.btn_edit.toggled = False
            self.btn_move.toggled = False
        elif self.mode == PathEditMode.EDIT and hidden == False:
            self.btn_draw.toggled = False
            self.btn_edit.toggled = True 
            self.btn_move.toggled = False
        elif self.mode == PathEditMode.MOVE and hidden == False:
            self.btn_draw.toggled = False
            self.btn_edit.toggled = False
            self.btn_move.toggled = True
        else: 
            self.btn_draw.toggled = False
            self.btn_edit.toggled = False 
            self.btn_move.toggled = False

        # self.btn_pgdn.disabled = True if self.parent.selected_line_index == None else False
        # self.btn_pgup.disabled = True if self.parent.selected_line_index == None else False

