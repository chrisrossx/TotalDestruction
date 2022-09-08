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
from TD.levels.data import EnemyChain, Boss, Control, LevelEntityControlType, LevelEntityType
from TD.editor.globals import current_level, current_scene, current_app


class GUILevelMarker(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)


        start_col = 23
        self.txts_marker_time = []
        for i in range(2):
            btn = gui.Button("Set", self.grid_pos(start_col, i), self.grid_size(1, 1))
            btn.on_button_1.append(lambda btn, index=i: self.on_btn_set(index))
            self.em.add(btn)
            btn = gui.Button("Clr", self.grid_pos(start_col+1, i), self.grid_size(1, 1))
            btn.on_button_1.append(lambda btn, index=i: self.on_btn_clear(index))
            self.em.add(btn)
            txt = gui.TextBoxFloat(0.0, self.grid_pos(start_col+2, i), self.grid_size(5, 1), "Marker {}: ".format(i+1))
            txt.on_value_changed.append(lambda txt, index=i: self.on_txt_marker(txt, index))
            self.em.add(txt)
            self.txts_marker_time.append(txt)

        self.btn_goto_marker_1 = gui.Button("Goto Marker 1", self.grid_pos(start_col, 2), self.grid_size(3, 1))
        self.btn_goto_marker_1.on_button_1.append(self.on_btn_goto_marker_1)
        self.em.add(self.btn_goto_marker_1)

        self.btn_goto_marker_2 = gui.Button("Goto Mark 2", self.grid_pos(start_col+3, 2), self.grid_size(4, 1))
        self.btn_goto_marker_2.on_button_1.append(self.on_btn_goto_marker_2)
        self.em.add(self.btn_goto_marker_2)

        self.btn_copy_entities = gui.Button("Copy Chains", self.grid_pos(start_col, 3), self.grid_size(3, 1))
        self.btn_copy_entities.on_button_1.append(self.on_btn_copy_entities)
        self.em.add(self.btn_copy_entities)

        self.btn_paste_entities = gui.Button("Paste at Cursor", self.grid_pos(start_col+3, 3), self.grid_size(4, 1))
        self.btn_paste_entities.on_button_1.append(self.on_btn_paste_entities)
        self.em.add(self.btn_paste_entities)

        self.btn_clear_entities = gui.Button("Clear Chains", self.grid_pos(start_col, 4), self.grid_size(3, 1))
        self.btn_clear_entities.on_button_1.append(self.on_btn_clear_entities)
        self.em.add(self.btn_clear_entities)

        self.btn_delete_time = gui.Button("Delete Time", self.grid_pos(start_col+3, 4), self.grid_size(4, 1))
        self.btn_delete_time.on_button_1.append(self.on_btn_delete_time)
        self.em.add(self.btn_delete_time)

        self.marker_time = [None, None]
        self.update()

        self.copied_entities = []
        self.copied_entities_start_time = None

    def on_btn_goto_marker_1(self, btn):
        if self.marker_time[0] != None:
            a = current_scene.gui_level_size.time_cursor_position * 1024
            current_scene.time = self.marker_time[0] - (a / SKY_VELOCITY)
            current_scene.gui_level_size.update_time_curosr_elements()
            current_scene.gui_level_size.set_time_slider_value(self.time)

    def on_btn_goto_marker_2(self, btn):
        if self.marker_time[1] != None:
            a = current_scene.gui_level_size.time_cursor_position * 1024
            current_scene.time = self.marker_time[1] - (a / SKY_VELOCITY)
            current_scene.gui_level_size.update_time_curosr_elements()
            current_scene.gui_level_size.set_time_slider_value(self.time)

    def on_btn_copy_entities(self, btn):
        if self.marker_time[0] == None or self.marker_time[1] == None:
            return 

        self.copied_entities = []
        markers = sorted(self.marker_time)
        self.copied_entities_start_time = markers[0]
        #cache a copy incase we delete the original before paste!
        for entity in current_level.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]:
            if entity.time >= markers[0] and entity.time <= markers[1]:
                copied = entity.__class__()
                copied.load(entity.save())
                self.copied_entities.append(copied)

    def on_btn_paste_entities(self, btn):
        for copied in self.copied_entities:
            #create another copy incase we paste more than once
            new = copied.__class__()
            new.load(copied.save())
            delta = copied.time - self.copied_entities_start_time
            new.time = current_scene.gui_level_size.time_cursor + delta
            current_level.add(new)

    def on_btn_clear_entities(self, btn):
        if self.marker_time[0] == None or self.marker_time[1] == None:
            return 
        def confirm(btn):
            markers = sorted(self.marker_time)
            for entity in current_level.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]:
                if entity.time >= markers[0] and entity.time <= markers[1]:
                    current_level.delete(entity)
            self.em.delete(panel)
        def cancel(btn):
            self.em.delete(panel)
        
        count = 0
        markers = sorted(self.marker_time)
        for entity in current_level.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]:
            if entity.time >= markers[0] and entity.time <= markers[1]:
                count += 1
        
        panel = gui.ConfirmPanel("Clear [{}] Chains Between Markers?".format(count), confirm, cancel)
        self.em.add(panel)
        panel.show()

    def on_btn_delete_time(self, btn):
        if self.marker_time[0] == None or self.marker_time[1] == None:
            return 
        def confirm(btn):
            markers = sorted(self.marker_time)
            for entity in current_level.level_entities:
                if entity.time >= markers[0] and entity.time <= markers[1]:
                    current_level.delete(entity)
            current_level.delete_time(markers[0], markers[1] - markers[0])
            self.em.delete(panel)

            self.marker_time[1] = None 
            self.marker_time[0] = markers[0]
            current_scene.gui_level_size.update_after_duration_change()
        def cancel(btn):
            self.em.delete(panel)
        
        count = 0
        markers = sorted(self.marker_time)
        for entity in current_level.level_entities:
            if entity.time >= markers[0] and entity.time <= markers[1]:
                count += 1
        
        panel = gui.ConfirmPanel("Delete [{}ms] and [{}] Entities Between Markers?".format(markers[1] - markers[0], count), confirm, cancel)
        self.em.add(panel)
        panel.show()


    def on_txt_marker(self, txt, index):
        self.marker_time[index] = txt.value
        self.update()

    def on_btn_set(self, index):
        self.marker_time[index] = current_scene.gui_level_size.time_cursor
        self.update()

    def on_btn_clear(self, index):
        self.marker_time[index] = None
        self.update()

    def update(self):
        for i in range(2):
            txt = self.txts_marker_time[i]
            txt.text = self.marker_time[i] if self.marker_time[i] != None else None

    def draw_markers(self, surface):
        d, orange = 8, (255, 155, 0)
        for i, time in enumerate(self.marker_time):
            if time != None:
                x = (time * SKY_VELOCITY)
                x += current_scene.pixel_offset_with_time
                pygame.draw.line(surface, orange, (x, 90), (x - d, 90 - d))
                pygame.draw.line(surface, orange, (x - d, 90 - d), (x + d, 90 - d))
                pygame.draw.line(surface, orange, (x, 90), (x + d, 90 - d))
                pygame.draw.line(surface, orange, (x, 710), (x - d, 710 + d))
                pygame.draw.line(surface, orange, (x - d, 710 + d), (x + d, 710 + d))
                pygame.draw.line(surface, orange, (x, 710), (x + d, 710 + d))
                pygame.draw.line(surface, orange, (x, 90), (x, 710))
                lbl = current_app.font.render(str(i+1), True, (orange))
                rect = lbl.get_rect()
                rect.centerx = x 
                rect.bottom = 90 - d
                surface.blit(lbl, rect)

    def draw(self, elapsed, surface):
        grey = (80, 80, 80)
        x = self.grid_pos(23,0).x - 4
        pygame.draw.line(surface, grey, (x, EDITOR_SCREEN_RECT.bottom- 150), (x, EDITOR_SCREEN_RECT.bottom))

        # Time Window Curos Triangles / Center of Window
        self.draw_markers(surface)
