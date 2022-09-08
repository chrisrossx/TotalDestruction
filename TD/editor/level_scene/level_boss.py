from multiprocessing import Value
from tracemalloc import start
from pygame import Vector2
import pygame
from TD import editor
from TD.config import SKY_VELOCITY, SCREEN_RECT
from TD.editor.config import EDITOR_SCREEN_RECT, EDITOR_SCREEN_SIZE

from TD.editor.scene import Scene, GUIGroup
from TD.entity import EntityType
from .sky import Sky
from TD.editor import gui
from TD.editor.config import EDITOR_SCREEN_SIZE
from TD.assetmanager import asset_manager
from TD.editor.globals import current_scene, current_level
from TD.editor.editorassets import editor_assets
from TD.editor.level_scene.level_paths import SelectPathPanel



class SelectBossPanel(gui.Panel):
    def __init__(self, on_selected, current_value = None):
        panel_rows = 12
        panel_cols = 6
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "Choose Chain Enemny")

        self.on_selected = on_selected

        btn = gui.ButtonGraphic(editor_assets.sprites["icon Boss 001"], "Boss 001", self.grid_pos(0,0), self.grid_size(6, 2))
        if current_value == "Boss 001":
            btn.toggled = True        
        btn.on_button_1.append(lambda btn: self.on_btn("Boss 001"))
        self.em.add(btn)

        # btn = gui.ButtonGraphic(editor_assets.sprites["icon CX5B"], "CX5B", self.grid_pos(0,2), self.grid_size(6, 2))
        # btn.on_button_1.append(lambda btn: self.on_btn("CX5B"))
        # self.em.add(btn)

        # btn = gui.ButtonGraphic(editor_assets.sprites["icon HX7"], "HX7", self.grid_pos(0,4), self.grid_size(6, 2))
        # btn.on_button_1.append(lambda btn: self.on_btn("HX7"))
        # self.em.add(btn)

        # btn = gui.ButtonGraphic(editor_assets.sprites["icon D2"], "D2", self.grid_pos(0,6), self.grid_size(6, 2))
        # btn.on_button_1.append(lambda btn: self.on_btn("D2"))
        # self.em.add(btn)

        # btn = gui.ButtonGraphic(editor_assets.sprites["icon BT1"], "BT1", self.grid_pos(0,8), self.grid_size(6, 2))
        # btn.on_button_1.append(lambda btn: self.on_btn("BT1"))
        # self.em.add(btn)


        btn = gui.Button("None", self.grid_pos(0,10), self.grid_size(6, 2))
        if current_value == None:
            btn.toggled = True
        btn.on_button_1.append(lambda btn: self.on_btn(None))
        self.em.add(btn)

    def on_btn(self, selection):
        self.close()
        self.on_selected(selection)



class GUILevelBossDetails(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_boss = None

        start_col = 30

        self.lbl_boss_properties = gui.Label("Boss Properties:", self.grid_pos(start_col, 0), self.grid_size())
        self.em.add(self.lbl_boss_properties)

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

        self.btn_select_boss = gui.ButtonGraphic(None, "Select Boss", self.grid_pos(start_col+6, 0), self.grid_size(height=2))
        self.btn_select_boss.on_button_1.append(self.on_btn_boss_enemy)
        self.btn_select_boss.align = "center" 
        self.em.add(self.btn_select_boss)
        
        self.rbr_move = gui.RubberBand(self.grid_pos(start_col, 4), self.grid_size(), label="Move")
        self.rbr_move.on_value_changing.append(self.on_rbr_changing)
        self.rbr_move.on_value_start.append(self.on_rbr_start)
        self.rbr_move.on_value_changed.append(self.on_rbr_finished)
        self.em.add(self.rbr_move)



        self.entities_toggel = [
            self.lbl_boss_properties,
            self.txt_name, 
            self.txt_time, 
            self.btn_move_time_to_cursor,
            self.btn_undo_time_move,
            self.btn_select_boss,
            self.rbr_move,
        ]

        self.hide_boss_properities()
        self.rbr_time_value = None

    def on_rbr_changing(self, elapsed, value):
        self.selected_boss._time += elapsed * value * 4
        self.update()

    def on_rbr_finished(self, rbr):
        self.selected_boss.previous_times.append(self.rbr_time_value)
        self.update()

    def on_rbr_start(self, rbr):
        self.rbr_time_value = self.txt_time.value

    def on_btn_boss_enemy(self, btn):
        def selected(enemy):
            self.selected_boss.boss = enemy
            self.update()
            self.em.delete(panel)
        panel = SelectBossPanel(selected, self.selected_boss.boss)
        self.em.add(panel)
        panel.show()

    def on_btn_undo_time_move(self, btn):
        self.selected_boss.undo_time_move()
        self.update()

    def update(self):
        if self.selected_boss == None:
            return 
        self.txt_name.text = self.selected_boss.name 
        self.txt_time.text = self.selected_boss.time
        if len(self.selected_boss.previous_times) > 0:
            self.btn_undo_time_move.disabled = False
        else:
            self.btn_undo_time_move.disabled = True 
        if self.selected_boss.boss == None:
            self.btn_select_boss.align="center"
            self.btn_select_boss.text = "Select Boss"
            self.btn_select_boss.image = None
        if self.selected_boss.boss in ["Boss 001", ]:
            self.btn_select_boss.align="left"
            self.btn_select_boss.text = self.selected_boss.boss
            self.btn_select_boss.image = editor_assets.sprites["icon {}".format(self.selected_boss.boss)]

        self.selected_boss.update_badge()

    def on_btn_move_time_to_cursor(self, btn):
        time = current_scene.time + ((1024 / SKY_VELOCITY) * current_scene.gui_level_size.time_cursor_position)
        self.selected_boss.time = time
        self.update()

    def on_txt_time(self, txt):
        self.selected_boss.time = txt.value
        self.selected_boss.update_badge()

    def on_txt_name(self, txt):
        self.selected_boss.name = txt.text 
        self.selected_boss.update_badge()

    def select_boss(self, entity):
        if self.selected_boss:
            self.selected_boss.selected = False
            self.selected_boss = None
            # self.no_chain_selected()
            self.hide_boss_properities()
        if entity:
            for e in self.entities_toggel:
                e.disabled = False 
            entity.selected = True 
            self.selected_boss = entity
            self.update()
            self.show_boss_properities()

    def hide_boss_properities(self):
        self.toggle_display(False)

    def show_boss_properities(self):
        self.toggle_display(True)

    def toggle_display(self, value):
        for e in self.entities_toggel:
            e.enabled = value 