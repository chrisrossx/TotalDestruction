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
from TD.levels.data import LevelEntityType
from TD.editor.globals import current_level


class GUILevelDetails(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        # -------------------------

        start_col = 12 + 6

        self.btn_show_controls = gui.ShowButton(self.grid_pos(start_col,0), self.grid_size(1,1))
        self.btn_show_controls.toggled = True 
        self.btn_show_controls.on_button_1.append(self.on_btn_show)
        self.em.add(self.btn_show_controls)
        self.txt_controls_count = gui.TextBoxInt(0, self.grid_pos(start_col + 1, 0), self.grid_size(4, 1), "Control: ")
        self.txt_controls_count.editable = False 
        self.em.add(self.txt_controls_count)

        self.btn_show_chains = gui.ShowButton(self.grid_pos(start_col,1), self.grid_size(1,1))
        self.btn_show_chains.toggled = True
        self.btn_show_chains.on_button_1.append(self.on_btn_show)
        self.em.add(self.btn_show_chains)
        self.txt_chain_count = gui.TextBoxInt(0, self.grid_pos(start_col + 1, 1), self.grid_size(4, 1), "Chains:  ")
        self.txt_chain_count.editable = False 
        self.em.add(self.txt_chain_count)

        self.btn_show_boss = gui.ShowButton(self.grid_pos(start_col,2), self.grid_size(1,1))
        self.btn_show_boss.toggled = True 
        self.btn_show_boss.on_button_1.append(self.on_btn_show)
        self.em.add(self.btn_show_boss)
        self.txt_boss_count = gui.TextBoxInt(0, self.grid_pos(start_col + 1, 2), self.grid_size(4, 1), "Boss:    ")
        self.txt_boss_count.editable = False 
        self.em.add(self.txt_boss_count)

        self.btn_show_enemies = gui.ShowButton(self.grid_pos(start_col,3), self.grid_size(1,1))
        self.btn_show_enemies.toggled = True 
        self.em.add(self.btn_show_enemies)
        self.btn_show_enemies.disabled = True 
        self.txt_enemies_count = gui.TextBoxInt(0, self.grid_pos(start_col + 1, 3), self.grid_size(4, 1), "Enemies: ")
        self.txt_enemies_count.editable = False 
        self.em.add(self.txt_enemies_count)

        self.btn_show_past_end = gui.ShowButton(self.grid_pos(start_col,4), self.grid_size(1,1))
        self.btn_show_past_end.toggled = True 
        self.em.add(self.btn_show_past_end)
        self.btn_show_past_end.disabled = True 
        self.txt_past_end_count = gui.TextBoxInt(None, self.grid_pos(start_col + 1, 4), self.grid_size(4, 1), "Past:    ")
        self.txt_past_end_count.editable = False 
        self.em.add(self.txt_past_end_count)

        self.btn_hide_sky = gui.Button("Hide Sky", self.grid_pos(14,3), self.grid_size(2,1))
        self.btn_hide_sky.toggled = self.parent.hide_sky
        self.btn_hide_sky.on_button_1.append(self.on_btn_hide_sky)
        self.em.add(self.btn_hide_sky)

        self.btn_hide_badge = gui.Button("Hide Bdg", self.grid_pos(16,3), self.grid_size(2,1))
        self.btn_hide_badge.toggled = self.parent.hide_badge
        self.btn_hide_badge.on_button_1.append(self.on_btn_hide_badge)
        self.em.add(self.btn_hide_badge)

    def on_btn_hide_sky(self, btn):
        self.parent.hide_sky = not self.parent.hide_sky
        self.btn_hide_sky.toggled = self.parent.hide_sky

    def on_btn_hide_badge(self, btn):
        self.parent.hide_badge = not self.parent.hide_badge
        self.btn_hide_badge.toggled = self.parent.hide_badge

    def on_btn_show(self, btn):
        btn.toggled = not btn.toggled

    def tick(self, elapsed):
        if len(current_level.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]) != self.txt_chain_count.value:
            self.txt_chain_count.text = len(current_level.level_entities_by_type[LevelEntityType.ENEMY_CHAIN])

        if len(current_level.level_entities_by_type[LevelEntityType.BOSS]) != self.txt_boss_count.value:
            self.txt_boss_count.text = len(current_level.level_entities_by_type[LevelEntityType.BOSS])

        if len(current_level.level_entities_by_type[LevelEntityType.CONTROL]) != self.txt_controls_count.value:
            self.txt_controls_count.text = len(current_level.level_entities_by_type[LevelEntityType.CONTROL])

        if current_level.total_enemies != self.txt_enemies_count.value:
            self.txt_enemies_count.text = current_level.total_enemies

        last = 0
        count = 0
        for entity in current_level.level_entities:
            if entity.time > current_level.total_time:
                count += 1
            if entity.time > last:
                last = entity.time

        if count > 0:
            txt = int(last)
        else:
            txt = None
        if txt != self.txt_past_end_count.value:
            self.txt_past_end_count.text = txt
