import statistics

import pygame 
from pygame import Vector2
from TD.config import SCREEN_RECT

from TD.editor import gui 
from TD import paths
from .gui_group import PanelGUIGroup
from TD.editor.globals import current_scene
from .utils import validate_txt_point

class Transforms(PanelGUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        start_row = 14

        self.lbl_Transform = gui.Label("Transform", self.grid_pos(41, start_row), self.grid_size(3, 1))
        self.em.add(self.lbl_Transform)


        self.btn_copy = gui.Button("Copy", self.grid_pos(41, start_row+1), self.grid_size(3, 1))
        self.btn_copy.on_button_1.append(self.on_btn_copy)
        self.em.add(self.btn_copy)

        self.btn_paste = gui.Button("Paste", self.grid_pos(44, start_row+1), self.grid_size(3, 1))
        self.btn_paste.on_button_1.append(self.on_btn_paste)
        self.em.add(self.btn_paste)

        # self.btn_move = gui.Button("Move", self.grid_pos(41, start_row+2), self.grid_size(3, 1))
        # self.btn_move.on_button_1.append(self.on_btn_move)
        # self.em.add(self.btn_move)

        self.txt_move_to = gui.TextBox("", self.grid_pos(41, start_row+2), self.grid_size(4, 1), "x, y: ")
        self.em.add(self.txt_move_to)

        self.btn_move_to = gui.Button("Move To", self.grid_pos(45, start_row+2), self.grid_size(2, 1))
        self.btn_move_to.on_button_1.append(self.on_btn_move_to)
        self.em.add(self.btn_move_to)

        self.txt_translate = gui.TextBox("", self.grid_pos(41, start_row+3), self.grid_size(4, 1), "x, y: ")
        self.em.add(self.txt_translate)
        
        self.btn_translate = gui.Button("Transl", self.grid_pos(45, start_row+3), self.grid_size(2, 1))
        self.btn_translate.on_button_1.append(self.on_btn_translate)
        self.em.add(self.btn_translate)

        self.txt_rotate = gui.TextBox("", self.grid_pos(41, start_row+4), self.grid_size(4, 1))
        self.em.add(self.txt_rotate)
        self.btn_rotate = gui.Button("Rotate", self.grid_pos(45, start_row+4), self.grid_size(2, 1), "deg: ")
        self.btn_rotate.on_button_1.append(self.on_btn_rotate)
        self.em.add(self.btn_rotate)

        self.btn_mirror_x = gui.Button("Mirror X", self.grid_pos(41, start_row+5), self.grid_size(3, 1))
        self.btn_mirror_x.on_button_1.append(self.on_btn_mirror_x)
        self.em.add(self.btn_mirror_x)
 
        self.btn_mirror_y = gui.Button("Mirror Y", self.grid_pos(44, start_row+5), self.grid_size(3, 1))
        self.btn_mirror_y.on_button_1.append(self.on_btn_mirror_y)
        self.em.add(self.btn_mirror_y)

        self.btn_clear = gui.Button("Clear Pts", self.grid_pos(41, start_row+6), self.grid_size(3, 1))
        self.btn_clear.on_button_1.append(self.on_btn_clear)
        self.em.add(self.btn_clear)
 
        self.btn_delete = gui.Button("Delete", self.grid_pos(44, start_row+6), self.grid_size(3, 1))
        self.btn_delete.on_button_1.append(self.on_btn_delete)
        self.em.add(self.btn_delete)

        self.copied_path_data = None 

        self.update()

    def on_btn_copy(self, btn):
        path_data = self.get_path_data()
        self.copied_path_data = path_data.duplicate()

    def on_btn_paste(self, btn):
        if self.copied_path_data != None:
            self.clear_mode()
            data = self.copied_path_data.duplicate()
            data.name += " (COPY)"
            paths.path_data[self.selected_line_index] = data
            self.parent.update()
    
    def on_btn_move(self, btn):
        pass

    def on_btn_move_to(self, btn):
        vector = validate_txt_point(self.txt_move_to.text)
        if vector == None:
            print("Invalid Input for Move To \"{}\" expected \"1.0, 1.0\"".format(self.txt_translate.text))
        else:
            self.clear_mode()
            path_data = self.get_path_data()
            if len(path_data.points) > 0:
                delta = vector - Vector2(path_data.points[0])
                for i in range(len(path_data.points)):
                    point = Vector2(path_data.points[i])
                    point += delta 
                    path_data.points[i] = [round(point.x, 0), round(point.y, 0)]
                path_data.calculate()
                self.parent.update()
    
    def on_btn_translate(self, btn):
        vector = validate_txt_point(self.txt_translate.text)
        if vector == None:
            print("Invalid Input for Translate \"{}\" expected \"1.0, 1.0\"".format(self.txt_translate.text))
        else:
            self.clear_mode()
            path_data = self.get_path_data()
            if len(path_data.points) > 0:
                for i in range(len(path_data.points)):
                    point = path_data.points[i]
                    point[0] += vector.x
                    point[1] += vector.y
                    path_data.points[i] = [round(point[0], 0), round(point[1], 0)]
                path_data.calculate()
                self.parent.update()

    def on_btn_rotate(self, btn):
        #find center of the path 
        try:
            degrees = float(self.txt_rotate.text)
        except:
            print("Invalid Input for Rotate \"{}\" expected \"1.0\"".format(self.txt_rotate.text))
            return None 
        self.clear_mode()
        path_data = self.get_path_data()        
        if len(path_data.points) > 0:
            #Rotate aronud Median Center of Points, But could consider rotate around Point[0]
            x_values = [p[0] for p in path_data.points]
            y_values = [p[1] for p in path_data.points]
            center = Vector2(statistics.median(x_values), statistics.median(y_values))
            for i in range(len(path_data.points)):
                point = Vector2(path_data.points[i])
                point = point - center 
                point.rotate_ip(-float(self.txt_rotate.text))
                point = point + center 
                path_data.points[i] = [round(point.x, 0), round(point.y, 0)]
            path_data.calculate()
            self.parent.update()



    def on_btn_mirror_x(self, btn):
        self.clear_mode()
        path_data = self.get_path_data()
        if len(path_data.points) > 0:
            for i in range(len(path_data.points)):
                point = path_data.points[i]
                point[0] -= SCREEN_RECT.w / 2
                point[0] *= -1
                point[0] += SCREEN_RECT.w / 2
                path_data.points[i] = [round(point[0], 0), round(point[1], 0)]
            path_data.calculate()
            self.parent.update()

    def on_btn_mirror_y(self, btn):
        self.clear_mode()
        path_data = self.get_path_data()
        if len(path_data.points) > 0:
            for i in range(len(path_data.points)):
                point = path_data.points[i]
                point[1] -= SCREEN_RECT.h / 2
                point[1] *= -1
                point[1] += SCREEN_RECT.h / 2
                path_data.points[i] = [round(point[0], 0), round(point[1], 0)]
            path_data.calculate()
            self.parent.update()
                
    def on_btn_clear(self, btn):
        self.clear_mode()
        def on_confirm(panel):
            path_data = self.get_path_data()
            path_data.points = []
            path_data.calculate()
            self.parent.update()
        confirm = gui.ConfirmPanel("Confirm Clear All Points From Path Data", on_confirm)
        current_scene.em.add(confirm)
        confirm.show()
    
    def on_btn_delete(self, btn):
        self.clear_mode()
        def on_confirm(panel):
            path_data = self.get_path_data()
            path_data.name = ""
            path_data.hidden = False 
            path_data.points = []
            path_data.calculate()
            self.parent.update()
        confirm = gui.ConfirmPanel("Confirm Delete Path Data", on_confirm)
        current_scene.em.add(confirm)
        confirm.show()

    def update(self):

        if self.parent.selected_line_index == None:
            hidden = False
        else:
            path_data = self.get_path_data()
            hidden = path_data.hidden

        disabled = True if self.parent.selected_line_index == None or hidden == True else False
        self.lbl_Transform.disabled = disabled
        self.btn_copy.disabled = disabled 
        self.btn_paste.disabled = disabled 
        # self.btn_move.disabled = disabled 
        self.btn_move_to.disabled = disabled 
        self.btn_translate.disabled = disabled 
        self.btn_rotate.disabled = disabled 
        self.btn_mirror_x.disabled = disabled
        self.btn_mirror_y.disabled = disabled
        self.btn_clear.disabled = disabled 
        self.btn_delete.disabled = disabled 
        self.txt_translate.disabled = disabled 
        self.txt_rotate.disabled = disabled 
        self.txt_move_to.disabled = disabled 

