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



class SelectEnemyPanel(gui.Panel):
    def __init__(self, on_selected, current_value=None):
        panel_rows = 12
        panel_cols = 6
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "Choose Chain Enemny")

        self.on_selected = on_selected

        btn = gui.ButtonGraphic(editor_assets.sprites["icon T8"], "T8", self.grid_pos(0,0), self.grid_size(6, 2))
        if current_value == "T8":
            btn.toggled = True
        btn.on_button_1.append(lambda btn: self.on_btn("T8"))
        self.em.add(btn)

        btn = gui.ButtonGraphic(editor_assets.sprites["icon CX5B"], "CX5B", self.grid_pos(0,2), self.grid_size(6, 2))
        if current_value == "CX5B":
            btn.toggled = True
        btn.on_button_1.append(lambda btn: self.on_btn("CX5B"))
        self.em.add(btn)

        btn = gui.ButtonGraphic(editor_assets.sprites["icon HX7"], "HX7", self.grid_pos(0,4), self.grid_size(6, 2))
        if current_value == "HX7":
            btn.toggled = True
        btn.on_button_1.append(lambda btn: self.on_btn("HX7"))
        self.em.add(btn)

        btn = gui.ButtonGraphic(editor_assets.sprites["icon D2"], "D2", self.grid_pos(0,6), self.grid_size(6, 2))
        if current_value == "D2":
            btn.toggled = True
        btn.on_button_1.append(lambda btn: self.on_btn("D2"))
        self.em.add(btn)

        btn = gui.ButtonGraphic(editor_assets.sprites["icon BT1"], "BT1", self.grid_pos(0,8), self.grid_size(6, 2))
        if current_value == "BT1":
            btn.toggled = True
        btn.on_button_1.append(lambda btn: self.on_btn("BT1"))
        self.em.add(btn)


        btn = gui.Button("None", self.grid_pos(0,10), self.grid_size(6, 2))
        if current_value == None:
            btn.toggled = True
        btn.on_button_1.append(lambda btn: self.on_btn(None))
        self.em.add(btn)

    def on_btn(self, selection):
        self.close()
        self.on_selected(selection)



class GUILevelChainDetails(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_chain = None

        start_col = 30

        self.lbl_chain_properties = gui.Label("Chain Properties:", self.grid_pos(start_col, 0), self.grid_size())
        self.em.add(self.lbl_chain_properties)

        self.txt_chain_name = gui.TextBox("", self.grid_pos(start_col, 1), self.grid_size(), label="Name: ")
        self.txt_chain_name.on_value_changed.append(self.on_txt_chain_name)
        self.em.add(self.txt_chain_name)

        self.txt_chain_time = gui.TextBoxFloat(0.0, self.grid_pos(start_col, 2), self.grid_size(), label="Time: ")
        self.txt_chain_time.on_value_changed.append(self.on_txt_chain_time)
        self.em.add(self.txt_chain_time)

        self.btn_move_time_to_cursor = gui.Button("Move To Crsr", self.grid_pos(start_col, 3), self.grid_size(3))
        self.btn_move_time_to_cursor.on_button_1.append(self.on_btn_move_time_to_cursor)
        self.em.add(self.btn_move_time_to_cursor)

        self.btn_undo_time_move = gui.Button("Undo Move", self.grid_pos(start_col+3, 3), self.grid_size(3))
        self.btn_undo_time_move.on_button_1.append(self.on_btn_undo_time_move)
        self.em.add(self.btn_undo_time_move)

        self.btn_chain_enemy = gui.ButtonGraphic(None, "Select Enemy", self.grid_pos(start_col+6, 0), self.grid_size(height=2))
        self.btn_chain_enemy.on_button_1.append(self.on_btn_chain_enemy)
        self.btn_chain_enemy.align = "center" 
        self.em.add(self.btn_chain_enemy)

        self.sld_count = gui.SlideValueInt(1,10,self.grid_pos(start_col+6, 2), self.grid_size(6, 1), label="Count: ")
        self.sld_count.on_value_changed.append(self.on_sld_count)
        self.em.add(self.sld_count)

        self.txt_spacing = gui.TextBoxFloat(1000.0, self.grid_pos(start_col+6, 3), self.grid_size(6, 1), label="Spacing: ")
        self.txt_spacing.on_value_changed.append(self.on_txt_spacing)
        self.em.add(self.txt_spacing)

        self.btn_path = gui.Button("Path: ", self.grid_pos(start_col+6, 4), self.grid_size())
        self.btn_path.on_button_1.append(self.on_btn_path)
        self.em.add(self.btn_path)

        self.rbr_move = gui.RubberBand(self.grid_pos(start_col, 4), self.grid_size(), label="Move")
        self.rbr_move.on_value_changing.append(self.on_rbr_changing)
        self.rbr_move.on_value_start.append(self.on_rbr_start)
        self.rbr_move.on_value_changed.append(self.on_rbr_finished)
        self.em.add(self.rbr_move)

        self.btn_chain_library = gui.Button("Library", self.grid_pos(start_col+14+6, 4), self.grid_size(4, 1))
        self.btn_chain_library.on_button_1.append(self.on_btn_chain_library)
        self.em.add(self.btn_chain_library)

        self.lbl_guns = gui.Label("Guns:", self.grid_pos(start_col+12, 0), self.grid_size(2, 1))
        self.lbl_upgrades = gui.Label("Upgrades:", self.grid_pos(start_col+12, 1), self.grid_size(2, 1))
        self.lbl_hearts = gui.Label("Hearts:", self.grid_pos(start_col+12, 2), self.grid_size(2, 1))
        self.lbl_coins = gui.Label("Coins:", self.grid_pos(start_col+12, 3), self.grid_size(2, 1))
        self.em.add(self.lbl_guns)
        self.em.add(self.lbl_upgrades)
        self.em.add(self.lbl_hearts)
        self.em.add(self.lbl_coins)

        self.btns_gun = []
        self.btns_upgrade = []
        self.btns_heart = []
        self.btns_coin = []
        for i in range(10):
            btn_gun = gui.Button(str(i), self.grid_pos(start_col+14+i, 0), self.grid_size(1,1))
            btn_gun.align = "center"
            btn_gun.on_button_1.append(lambda btn, index=i: self.on_btn_gun(index))
            self.em.add(btn_gun)
            self.btns_gun.append(btn_gun)

            btn_upgrade = gui.Button(str(i), self.grid_pos(start_col+14+i, 1), self.grid_size(1,1))
            btn_upgrade.align = "center"
            btn_upgrade.on_button_1.append(lambda btn, index=i: self.on_btn_upgrade(index))
            self.em.add(btn_upgrade)
            self.btns_upgrade.append(btn_upgrade)

            btn_heart = gui.Button(str(i), self.grid_pos(start_col+14+i, 2), self.grid_size(1,1))
            btn_heart.align = "center"
            btn_heart.on_button_1.append(lambda btn, index=i: self.on_btn_heart(index))
            self.em.add(btn_heart)
            self.btns_heart.append(btn_heart)

            btn_coin = gui.Button(str(i), self.grid_pos(start_col+14+i, 3), self.grid_size(1,1))
            btn_coin.align = "center"
            btn_coin.on_button_1.append(lambda btn, index=i: self.on_btn_coin(index))
            self.em.add(btn_coin)
            self.btns_coin.append(btn_coin)


        self.entities_toggel = [
            self.txt_chain_name,
            self.txt_chain_time,
            self.btn_chain_enemy, 
            self.btn_move_time_to_cursor,
            self.btn_undo_time_move,
            self.txt_spacing,
            self.sld_count,
            self.btn_path,
            self.rbr_move,
            self.btn_chain_library, 
        ]

        # self.no_chain_selected()
        self.hide_chain_properities()

        self.rbr_time_value = None

    def on_btn_chain_library(self, btn):
        current_scene.gui_level_chain_library.show()

    def on_rbr_changing(self, elapsed, value):
        self.selected_chain._time = round((self.selected_chain._time + (elapsed * value * 4)),2 )
        self.update()

    def on_rbr_finished(self, rbr):
        self.selected_chain.previous_times.append(self.rbr_time_value)
        self.update()

    def on_rbr_start(self, rbr):
        self.rbr_time_value = self.txt_chain_time.value

    def on_txt_spacing(self, txt):
        self.selected_chain.spacing = txt.value
        self.update()

    def on_btn_path(self, btn):
        def on_select_path(path_index):
            self.selected_chain.path_index = path_index
            panel.close()
            self.em.delete(panel)
            self.update()
        def on_cancel(panel):
            self.em.delete(panel)
        panel = SelectPathPanel(on_select_path=on_select_path)
        panel.on_cancel.append(on_cancel)
        panel.show()
        self.em.add(panel)

    def on_btn_gun(self, index):
        self.btns_gun[index].toggled = not self.btns_gun[index].toggled
        if self.btns_gun[index].toggled:
            if index not in self.selected_chain.guns:
                self.selected_chain.guns.append(index)
        else:
            if index in self.selected_chain.guns:
                self.selected_chain.guns.remove(index)
        self.selected_chain.update_badge()

    def on_btn_upgrade(self, index):
        self.btns_upgrade[index].toggled = not self.btns_upgrade[index].toggled
        if self.btns_upgrade[index].toggled:
            if index not in self.selected_chain.upgrades:
                self.selected_chain.upgrades.append(index)
        else:
            if index in self.selected_chain.upgrades:
                self.selected_chain.upgrades.remove(index)
        self.selected_chain.update_badge()

    def on_btn_heart(self, index):
        self.btns_heart[index].toggled = not self.btns_heart[index].toggled
        if self.btns_heart[index].toggled:
            if index not in self.selected_chain.hearts:
                self.selected_chain.hearts.append(index)
        else:
            if index in self.selected_chain.hearts:
                self.selected_chain.hearts.remove(index)
        self.selected_chain.update_badge()

    def on_btn_coin(self, index):
        self.btns_coin[index].toggled = not self.btns_coin[index].toggled
        if self.btns_coin[index].toggled:
            if index not in self.selected_chain.coins:
                self.selected_chain.coins.append(index)
        else:
            if index in self.selected_chain.coins:
                self.selected_chain.coins.remove(index)
        self.selected_chain.update_badge()

    def on_sld_count(self, sld):
        self.selected_chain.count = sld.value
        self.update()

    def on_btn_chain_enemy(self, btn):
        def selected(enemy):
            self.selected_chain.enemy = enemy
            self.update()
            self.em.delete(panel)
        panel = SelectEnemyPanel(selected, self.selected_chain.enemy)
        self.em.add(panel)
        panel.show()

    def on_btn_undo_time_move(self, btn):
        self.selected_chain.undo_time_move()
        self.update()

    def update(self):
        if self.selected_chain == None:
            return 
        self.txt_chain_name.text = self.selected_chain.name 
        self.txt_chain_time.text = self.selected_chain.time
        self.sld_count.value = self.selected_chain.count
        self.txt_spacing.text = self.selected_chain.spacing
        self.btn_path.text = "Path: {}".format(self.selected_chain.path_index)
        if len(self.selected_chain.previous_times) > 0:
            self.btn_undo_time_move.disabled = False
        else:
            self.btn_undo_time_move.disabled = True 
        if self.selected_chain.enemy == None:
            self.btn_chain_enemy.align="center"
            self.btn_chain_enemy.text = "Select Enemy"
            self.btn_chain_enemy.image = None
        if self.selected_chain.enemy in ["T8", "CX5B", "HX7", "D2", "BT1"]:
            self.btn_chain_enemy.align="left"
            self.btn_chain_enemy.text = self.selected_chain.enemy
            self.btn_chain_enemy.image = editor_assets.sprites["icon {}".format(self.selected_chain.enemy)]

        for i, e in enumerate(self.btns_gun):
            e.disabled = False if i < self.selected_chain.count else True 
            e.toggled = True if i in self.selected_chain.guns else False 

        for i, e in enumerate(self.btns_upgrade):
            e.disabled = False if i < self.selected_chain.count else True 
            e.toggled = True if i in self.selected_chain.upgrades else False 

        for i, e in enumerate(self.btns_heart):
            e.disabled = False if i < self.selected_chain.count else True 
            e.toggled = True if i in self.selected_chain.hearts else False 

        for i, e in enumerate(self.btns_coin):
            e.disabled = False if i < self.selected_chain.count else True 
            e.toggled = True if i in self.selected_chain.coins else False 
        self.selected_chain.update_badge()

    def on_btn_move_time_to_cursor(self, btn):
        time = current_scene.time + ((1024 / SKY_VELOCITY) * current_scene.gui_level_size.time_cursor_position)
        self.selected_chain.time = time
        self.update()

    def on_txt_chain_time(self, txt):
        self.selected_chain.time = txt.value
        self.selected_chain.update_badge()

    def on_txt_chain_name(self, txt):
        self.selected_chain.name = txt.text 
        self.selected_chain.update_badge()

    def select_chain(self, entity):
        if self.selected_chain:
            self.selected_chain.selected = False
            self.selected_chain = None
            # self.no_chain_selected()
            self.hide_chain_properities()
        if entity:
            for e in self.entities_toggel:
                e.disabled = False 
            entity.selected = True 
            self.selected_chain = entity
            self.update()
            self.show_chain_properities()

    def hide_chain_properities(self):
        self.toggle_display(False)

    def show_chain_properities(self):
        self.toggle_display(True)

    def toggle_display(self, value):
        for e in self.entities_toggel:
            e.enabled = value 
        for e in self.btns_coin:
            e.enabled = value 
        for e in self.btns_heart:
            e.enabled = value 
        for e in self.btns_gun:
            e.enabled = value 
        for e in self.btns_upgrade:
            e.enabled = value 
        self.lbl_chain_properties.enabled = value
        self.lbl_coins.enabled = value 
        self.lbl_guns.enabled = value
        self.lbl_hearts.enabled = value 
        self.lbl_upgrades.enabled = value 

    def draw(self, elapsed, surface):
        grey = (80, 80, 80)
        # Time Window Label Leader Lines
        x = self.lbl_chain_properties.x - 4
        pygame.draw.line(surface, grey, (x, EDITOR_SCREEN_RECT.bottom- 150), (x, EDITOR_SCREEN_RECT.bottom))
        # Time Window Curos Triangles / Center of Window
