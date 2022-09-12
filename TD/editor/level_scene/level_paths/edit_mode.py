from dis import dis
from pygame import Vector2
import pygame 

from TD.editor.scene import GUIGroup
from TD.editor import gui 
from TD.paths import path_data
from TD.editor.globals import current_scene
from .select_mode import PathEditMode
from .gui_group import PanelGUIGroup
from .utils import validate_txt_point

class EditMode(PanelGUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        start_row = 9
        self.lbl_edit = gui.Label("Edit Mode", self.grid_pos(41, start_row), self.grid_size(3, 1))
        self.em.add(self.lbl_edit)

        self.lbl_selected = gui.Label("Selected:", self.grid_pos(41, start_row+1), self.grid_size(2, 1))
        self.em.add(self.lbl_selected)

        self.txt_selected = gui.TextBox("  1: 1010, 120", self.grid_pos(43, start_row+1), self.grid_size(4, 1))
        self.txt_selected.editable = False
        self.em.add(self.txt_selected)

        self.btn_insert_before = gui.Button("Insert Before", self.grid_pos(41, start_row+2), self.grid_size(3, 1))
        self.btn_insert_before.on_button_1.append(self.on_btn_insert_before)
        self.em.add(self.btn_insert_before)

        self.btn_insert_after = gui.Button("Insert After", self.grid_pos(44, start_row+2), self.grid_size(3, 1))
        self.btn_insert_after.on_button_1.append(self.on_btn_insert_after)
        self.em.add(self.btn_insert_after)

        self.btn_move_selected = gui.Button("Move Point", self.grid_pos(41, start_row+3), self.grid_size(3, 1))
        self.btn_move_selected.on_button_1.append(self.on_btn_move_selected)
        self.em.add(self.btn_move_selected)

        self.selected_point_index = None
        self.point_rects = []
        self.move_selected_mode = False

        self.update()

    # def on_selected_line_index(self, selected_line_inedx):
    #     self.clear_mode()

    def on_btn_insert_before(self, btn):
        if self.selected_point_index != None:
            path_data = self.get_path_data()
            if self.selected_point_index > 0:
                point_start = Vector2(self.get_selected_point())
                point_end = Vector2(path_data.points[self.selected_point_index - 1])
                mid_point = point_start.lerp(point_end, 0.5)
                path_data.points.insert(self.selected_point_index, [round(mid_point[0], 0), round(mid_point[1], 0)])
                path_data.calculate()
                self.parent.update()
            else:
                print("Start of Line")

    
    def on_btn_insert_after(self, btn):
        if self.selected_point_index != None:
            path_data = self.get_path_data()
            if len(path_data.points) -1 > self.selected_point_index:
                point_start = Vector2(self.get_selected_point())
                point_end = Vector2(path_data.points[self.selected_point_index + 1])
                mid_point = point_start.lerp(point_end, 0.5)
                path_data.points.insert(self.selected_point_index + 1, [round(mid_point[0], 0), round(mid_point[1], 0)])
                self.selected_point_index += 1
                
                path_data.calculate()
                self.parent.update()
            else:
                print("End of Line")


    def on_btn_move_selected(self, btn):
        if self.move_selected_mode == True:
            self.clear_move_selected()
        else:
            self.start_move_selected()

    def clear_move_selected(self):
        self.move_selected_mode = False 
        self.btn_move_selected.toggled = False

    def start_move_selected(self):
        self.move_selected_mode = True
        self.btn_move_selected.toggled = True

    def update(self):
        if self.parent.selected_line_index == None:
            hidden = False
        else:
            path_data = self.get_path_data()
            hidden = path_data.hidden        
        
        self.lbl_edit.disabled = True if self.parent.selected_line_index == None or hidden == True else False

        if self.path_edit_mode == PathEditMode.EDIT and self.selected_line_index != None:
            disabled = False 
            point = self.get_selected_point()
            if point != None:
                self.txt_selected.text = "{}, {}".format(point[0], point[1])
                self.txt_selected.label = "{: >3}: ".format((self.selected_point_index))
            else:
                self.txt_selected.text = ""
                self.txt_selected.label = ""
        else:
            disabled = True
            self.txt_selected.text = ""
            self.txt_selected.label = ""

        self.lbl_selected.disabled = disabled
        self.btn_insert_after.disabled = disabled 
        self.btn_insert_before.disabled = disabled 
        self.txt_selected.disabled = disabled 
        self.btn_move_selected.disabled = disabled

        if self.path_edit_mode == PathEditMode.EDIT and self.selected_line_index != None:
            path_data = self.get_path_data()
            d = 8
            self.point_rects = []
            for point in path_data.points:
                point = Vector2(point) + Vector2(100, 100) - Vector2(d,d )
                rect = pygame.Rect(point.x, point.y, d*2, d*2)
                self.point_rects.append(rect)
        elif len(self.point_rects) > 0:
            self.point_rects = []

    def delete_point(self, point_index):
        if self.path_edit_mode == PathEditMode.EDIT:
            self.select_point_index(None)
            path_data = self.get_path_data()
            points = path_data.points[:point_index]
            points += path_data.points[point_index + 1:]
            path_data.points = points 
            path_data.calculate()
            self.parent.update()

    def update_point_from_text(self, point_index, text):
        if self.path_edit_mode == PathEditMode.EDIT:
            vector = validate_txt_point(text)
            if vector != None:
                path_data = self.get_path_data()
                path_data.points[point_index] = [round(vector.x, 0), round(vector.y, 0)]
                path_data.calculate()
            self.parent.update()

    def select_point_index(self, point_index):
        if self.path_edit_mode == PathEditMode.EDIT:
            self.selected_point_index = point_index
        self.parent.update()

    def get_selected_point(self):
        path_data = self.get_path_data()
        if self.selected_point_index != None and self.selected_point_index < len(path_data.points):
            return path_data.points[self.selected_point_index]
        return None 

    def start_edit_mode(self):
        # print("For Shizzle!", self.path_edit_mode, self.selected_line_index)
        self.selected_point_index = None
        self.update()

    def end_edit_mode(self):
        # print("what what")
        self.selected_point_index = None
        self.point_rects = []
        self.clear_move_selected()
        self.update()
        self.update()

    def on_event(self, event, elapsed):
        if current_scene.gui_layer <= self.parent.line_window.gui_layer:
            if self.path_edit_mode == PathEditMode.EDIT:

                #Show the move button toggle when CTRL is pressed
                if self.selected_point_index != None:
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL):
                        if self.move_selected_mode == False:
                            self.btn_move_selected.toggled = True 
                    if event.type == pygame.KEYUP and (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL):
                        if self.move_selected_mode == False:
                            self.btn_move_selected.toggled = False

                #If Cursor is Set either select or Move!
                if self.parent.line_window.cursor != None:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.move_selected_mode == True or pygame.key.get_mods() & pygame.KMOD_CTRL:
                            cursor = self.parent.line_window.cursor
                            if cursor != None and self.selected_point_index != None:
                                path_data = self.get_path_data()
                                path_data.points[self.selected_point_index] = [round(cursor.x, 0), round(cursor.y, 0)]
                                path_data.calculate()
                                self.parent.update()
                                self.clear_move_selected()
                        else:
                            cursor = self.parent.line_window.cursor + Vector2(100, 100)
                            for i, rect in enumerate(self.point_rects):
                                if rect.collidepoint(cursor):
                                    self.selected_point_index = i
                                    self.parent.update()
                                    break

        
