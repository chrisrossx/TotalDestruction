from pygame import Vector2
from TD.editor import gui
from TD.editor.level_scene.level_paths.select_mode import PathEditMode 
from TD.paths import path_data
from .gui_group import PanelGUIGroup
from TD.editor.editorassets import editor_assets

class XYGrid(PanelGUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self.page = 0

        start_col = 47
        start_row = 0

        self.btn_pgup = gui.Button("PgUp", self.grid_pos(start_col, start_row), self.grid_size(3, 1), "center")
        # self.btn_pgup.disabled = True 
        self.btn_pgup.on_button_1.append(self.on_btn_pgup)
        self.em.add(self.btn_pgup)

        self.btn_pgdn = gui.Button("PgDn", self.grid_pos(start_col + 3, start_row), self.grid_size(3, 1), "center")
        # self.btn_pgdn.disabled = True
        self.btn_pgdn.on_button_1.append(self.on_btn_pgdn)
        self.em.add(self.btn_pgdn)
        self.row_count = 27

        self.point_txts = []
        self.point_delete_btns = []
        self.point_select_btns = []
        for row in range(self.row_count):
            point_txt = gui.TextBox("1000, 1000", self.grid_pos(start_col, start_row + 1 + row), self.grid_size(4, 1), "{}: ".format(row))
            point_txt.on_value_changed.append(lambda txt, index=row: self.on_txt_point(txt, index))
            btn_delete = gui.ButtonGraphic(editor_assets.sprites["btn icon trash"], "", self.grid_pos(start_col +5, start_row + 1 + row), self.grid_size(1, 1), align="center")
            # btn_delete = gui.Button("X", self.grid_pos(start_col +5, start_row + 1 + row), self.grid_size(1, 1), align="center")
            btn_delete.on_button_1.append(lambda btn, index=row: self.on_btn_delete(index))
            btn_select = gui.Button("S", self.grid_pos(start_col +4, start_row + 1 + row), self.grid_size(1, 1), align="center")
            btn_select.on_button_1.append(lambda btn, index=row: self.on_btn_select(index))
            self.em.add(point_txt)
            self.point_txts.append(point_txt)
            self.em.add(btn_delete)
            self.point_delete_btns.append(btn_delete)
            self.em.add(btn_select)
            self.point_select_btns.append(btn_select)

        self.update()

    def on_btn_select(self, btn_index):
        point_index = btn_index + (self.page * self.row_count)
        self.parent.gui_groups["edit_mode"].select_point_index(point_index)

    def on_btn_delete(self, btn_index):
        point_index = btn_index + (self.page * self.row_count)
        self.parent.gui_groups["edit_mode"].delete_point(point_index)

    def on_txt_point(self, txt, btn_index):
        point_index = btn_index + (self.page * self.row_count)
        self.parent.gui_groups["edit_mode"].update_point_from_text(point_index, txt.text)
        # self.parent.gui_groups["edit_mode"].select_point_index(point_index)

    def on_xy_txts(self, index, x, y):
        print(index, x, y)

    def on_selected_line_index(self, selected_line_inedx):
        self.page = 0

    def update(self):

        if self.parent.selected_line_index == None:
            hidden = False
        else:
            path_data = self.get_path_data()
            hidden = path_data.hidden


        self.btn_pgdn.disabled = True if self.parent.selected_line_index == None or hidden == True else False
        self.btn_pgup.disabled = True if self.parent.selected_line_index == None or hidden == True else False

        for row in range(self.row_count):
            txt = self.point_txts[row]
            btn_delete = self.point_delete_btns[row]
            btn_select = self.point_select_btns[row]
            point_index = row + (self.page * self.row_count)
            txt.label = "{: >2}: ".format((point_index))
            if self.parent.selected_line_index != None:
                txt.disabled = hidden
                btn_delete.disabled = hidden if self.path_edit_mode == PathEditMode.EDIT else True
                if self.path_edit_mode == PathEditMode.EDIT:
                    btn_select.disabled = hidden
                    # print("self.parent.gui_groups[\"edit_mode\"].selected_point_index", self.parent.gui_groups["edit_mode"].selected_point_index)
                    if self.parent.gui_groups["edit_mode"].selected_point_index == point_index :
                        btn_select.toggled = True 
                    else:
                        btn_select.toggled = False
                    
                else:   
                    btn_select.disabled = True
                    btn_select.toggled = False

                if self.path_edit_mode == PathEditMode.EDIT:
                    txt.editable = True 
                else:
                    txt.editable = False 

                if point_index < len(path_data.points):
                    point = path_data.points[point_index]
                    txt.text = "{}, {}".format(int(point[0]), int(point[1]))
                else:
                    txt.disabled = True 
                    btn_delete.disabled = True 
                    btn_select.disabled = True 
                    txt.text = ""

            else:
                txt.disabled = True 
                btn_delete.disabled = True 
                btn_select.disabled = True 
                txt.text = ""

    def on_btn_pgup(self, btn):
        if self.page > 0:
            self.page -= 1
            self.update()


    def on_btn_pgdn(self, btn):
        self.page += 1
        self.update()

