from multiprocessing import Value
from tracemalloc import start
from pygame import Vector2
import pygame
from TD import editor
from TD.config import SKY_VELOCITY, SCREEN_RECT
from TD.editor.config import EDITOR_SCREEN_RECT, EDITOR_SCREEN_SIZE

from TD.editor.scene import Scene, GUIGroup
from TD.entity import EntityType
from TD.levels.data import LevelEntityControlType
from .sky import Sky
from TD.editor import gui
from TD.editor.config import EDITOR_SCREEN_SIZE
from TD.assetmanager import asset_manager
from TD.editor.globals import current_scene, current_level
from TD.editor.editorassets import editor_assets
from TD.editor.level_scene.level_paths import SelectPathPanel


class GUILevelControlDetails(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_control = None

        start_col = 30

        self.lbl_control_properties = gui.Label("Control Point Properties:", self.grid_pos(start_col, 0), self.grid_size())
        self.em.add(self.lbl_control_properties)

        self.txt_name = gui.TextBox("", self.grid_pos(start_col, 1), self.grid_size(), label="Name: ")
        self.txt_name.on_value_changed.append(self.on_txt_name)
        self.em.add(self.txt_name)

        self.txt_time = gui.TextBoxFloat(0.0, self.grid_pos(start_col, 2), self.grid_size(), label="Time: ")
        self.txt_time.on_value_changed.append(self.on_txt_time)
        self.em.add(self.txt_time)

        self.btn_move_time_to_cursor = gui.Button("Move 2 Cursor", self.grid_pos(start_col, 3), self.grid_size(3))
        self.btn_move_time_to_cursor.on_button_1.append(self.on_btn_move_time_to_cursor)
        self.em.add(self.btn_move_time_to_cursor)

        self.btn_undo_time_move = gui.Button("Undo Move", self.grid_pos(start_col+3, 3), self.grid_size(3))
        self.btn_undo_time_move.on_button_1.append(self.on_btn_undo_time_move)
        self.em.add(self.btn_undo_time_move)

        self.btn_select_control_type = gui.Button("Type: None", self.grid_pos(start_col+6, 0), self.grid_size(height=1))
        self.btn_select_control_type.on_button_1.append(self.on_btn_select_control_type)
        self.em.add(self.btn_select_control_type)

        self.rbr_move = gui.RubberBand(self.grid_pos(start_col, 4), self.grid_size(), label="Move")
        self.rbr_move.on_value_changing.append(self.on_rbr_changing)
        self.rbr_move.on_value_start.append(self.on_rbr_start)
        self.rbr_move.on_value_changed.append(self.on_rbr_finished)
        self.em.add(self.rbr_move)

        self.txts_arguments = []
        self.btns_arguments = []

        for i in range(4):
            txt = gui.TextBox("", self.grid_pos(start_col+6, 1 + i), self.grid_size(), "Arg {}: ".format(i))
            txt.on_value_changed.append(lambda txt, index=i: self.on_txt_argument(txt, index))
            self.em.add(txt)
            self.txts_arguments.append(txt)

            btn = gui.Button("", self.grid_pos(start_col+6, 1 + i), self.grid_size(), "Arg {}: ".format(i))
            btn.on_button_1.append(lambda txt, index=i: self.on_btn_argument(txt, index))
            self.em.add(btn)
            self.btns_arguments.append(btn)

        self.entities_toggel = [
            self.lbl_control_properties,
            self.txt_name, 
            self.txt_time, 
            self.btn_move_time_to_cursor,
            self.btn_undo_time_move,
            self.btn_select_control_type,
            self.rbr_move,
        ]

        self.hide_control_properities()
        self.rbr_time_value = None

    def on_rbr_changing(self, elapsed, value):
        self.selected_control._time += elapsed * value * 4
        self.update()

    def on_rbr_finished(self, rbr):
        self.selected_control.previous_times.append(self.rbr_time_value)
        self.update()

    def on_rbr_start(self, rbr):
        self.rbr_time_value = self.txt_time.value


    def on_txt_argument(self, txt, index):
        self.selected_control.arguments[index] = txt.text
        self.update()

    def on_btn_argument(self, btn, index):
        if self.selected_control.control_type == LevelEntityControlType.ENEMY_DIALOG:
            if index == 0:
                def on_choice(key, value):
                    self.selected_control.arguments[0] = value
                    self.update()
                items = {
                    "Elle": "Elle",
                    "Sawyer": "Sawyer",
                    "MaiAnh": "MaiAnh",
                    "Christopher": "Christopher",
                }
                panel = gui.ChooseListPanel("Character:", items, self.selected_control.arguments[0])
                panel.on_choice.append(on_choice)
                self.em.add(panel)
                panel.show()
            if index == 1:
                def on_choice(key, value):
                    self.selected_control.arguments[1] = value
                    self.update()
                items = {
                    "TAUNT_1": "TAUNT_1",
                    "THREAT": "THREAT",
                    "PAIN": "PAIN",
                    "DYING": "DYING",
                }
                panel = gui.ChooseListPanel("Dialog:", items, self.selected_control.arguments[1])
                panel.on_choice.append(on_choice)
                self.em.add(panel)
                panel.show()


        self.update()


    def on_btn_select_control_type(self, btn):
        def on_choice(key, value):
            self.selected_control.control_type = value 
            self.update()
            self.em.delete(panel)

        items = {
            LevelEntityControlType(LevelEntityControlType.MUSIC).name: LevelEntityControlType.MUSIC,
            LevelEntityControlType(LevelEntityControlType.END_LEVEL).name: LevelEntityControlType.END_LEVEL,
            LevelEntityControlType(LevelEntityControlType.ENEMY_DIALOG).name: LevelEntityControlType.ENEMY_DIALOG,
        }
        panel = gui.ChooseListPanel("Select Control Type", items, self.selected_control.control_type)
        panel.on_choice.append(on_choice)
        self.em.add(panel)
        panel.show()

    def on_btn_undo_time_move(self, btn):
        self.selected_control.undo_time_move()
        self.update()

    def update(self):
        if self.selected_control == None:
            return
        self.txt_name.text = self.selected_control.name 
        self.txt_time.text = self.selected_control.time
        if len(self.selected_control.previous_times) > 0:
            self.btn_undo_time_move.disabled = False
        else:
            self.btn_undo_time_move.disabled = True 
        if self.selected_control.control_type == None:
            self.btn_select_control_type.text = "Type: None"
        else:
            self.btn_select_control_type.text = "Type: {}".format(LevelEntityControlType(self.selected_control.control_type).name)
        self.selected_control.update_badge()

        for i in range(4):
            txt = self.txts_arguments[i]
            if txt.text != self.selected_control.arguments[i]:
                txt.text = self.selected_control.arguments[i]
        self.update_arguments()

    def on_btn_move_time_to_cursor(self, btn):
        time = current_scene.time + ((1024 / SKY_VELOCITY) * current_scene.gui_level_size.time_cursor_position)
        self.selected_control.time = time
        self.update()

    def on_txt_time(self, txt):
        self.selected_control.time = txt.value
        self.selected_control.update_badge()

    def on_txt_name(self, txt):
        self.selected_control.name = txt.text 
        self.selected_control.update_badge()

    def select_control(self, entity):
        if self.selected_control:
            self.selected_control.selected = False
            self.selected_control = None
            # self.no_chain_selected()
            self.hide_control_properities()
        if entity:
            for e in self.entities_toggel:
                e.disabled = False 
            entity.selected = True 
            self.selected_control = entity
            self.update()
            self.show_control_properities()

    def hide_control_properities(self):
        self.toggle_display(False)

    def update_arguments(self):
        if self.selected_control.control_type == LevelEntityControlType.ENEMY_DIALOG:
            btns = ["Character", "Dialog", None, None]
            txts = [None, None, None, None]
        elif  self.selected_control.control_type == LevelEntityControlType.MUSIC:
            btns = [None, None, None, None]
            txts = ["Music Key: ", None, None, None]
        else:
            txts = [None, None, None, None]
            btns = [None, None, None, None]

        for i, lbl in enumerate(btns):
            btn = self.btns_arguments[i]
            if lbl == None:
                btn.enabled = False
            else:
                btn.text = "{}: {}".format(lbl, self.selected_control.arguments[i]) 
                btn.enabled = True 

        for i, lbl in enumerate(txts):
            txt = self.txts_arguments[i]
            if lbl == None:
                txt.enabled = False
            else:
                txt.label = lbl
                txt.text = self.selected_control.arguments[i]
                txt.enabled = True 


    def show_control_properities(self):
        self.toggle_display(True)
        for e in self.btns_arguments:
            e.enabled = True
        for e in self.txts_arguments:
            e.enabled = False
        self.update_arguments()

    def toggle_display(self, value):
        for e in self.entities_toggel:
            e.enabled = value 
        if value == False:
            for e in self.txts_arguments:
                e.enabled = value 
            for e in self.btns_arguments:
                e.enabled = value 