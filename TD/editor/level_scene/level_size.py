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



class InsertTimePanel(gui.Panel):
    def __init__(self, on_insert):
        panel_rows = 2
        panel_cols = 12
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "Insert Time at Cursor")
        self.on_insert = on_insert

        self.txt_value = gui.TextBoxInt(1000, self.grid_pos(0,0), self.grid_size(12, 1), "Time to insert: ")
        self.em.add(self.txt_value)

        btn_insert = gui.Button("Insert", self.grid_pos(6,1), self.grid_size())
        btn_insert.on_button_1.append(self.on_btn_insert)
        self.em.add(btn_insert)

    def on_btn_insert(self, btn):
        value = self.txt_value.value
        self.on_insert(self, value)

class GUILevelSizeTimeCursor(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)
        # -------------------------
        # Level Size and Cursor Widgets

        self.time_cursor_position = 0.5
        start_col = 6

        self.txt_level_total_time = gui.TextBoxInt(
            self.level.total_time,
            self.grid_pos(start_col, 0),
            self.grid_size(),
            label="Total Time:   ",
        )
        self.txt_level_total_time.on_value_changed.append(self.on_txt_level_total_time)
        self.em.add(self.txt_level_total_time)

        self.txt_level_pixel_length = gui.TextBoxFloat(
            self.level.pixel_length,
            self.grid_pos(start_col, 1),
            self.grid_size(),
            label="Pixel Length: ",
        )
        self.em.add(self.txt_level_pixel_length)
        self.txt_level_pixel_length.editable = False

        self.txt_time_cursor_position = gui.TextBoxFloat(
            (512 / SKY_VELOCITY),
            self.grid_pos(start_col, 2),
            self.grid_size(),
            label="Cursor:       ",
        )
        self.txt_time_cursor_position.editable = False
        self.em.add(self.txt_time_cursor_position)

        self.txt_time_value = gui.TextBoxFloat(
            self.time, self.grid_pos(start_col, 4), self.grid_size(), label="Time:         "
        )
        self.txt_time_value.on_value_changed.append(self.on_txt_time_value)
        self.em.add(self.txt_time_value)

        self.sld_level_cursor_position = gui.SlideValue(
            0.0, 1.0, self.grid_pos(start_col, 3), self.grid_size(), "Cursor Pos:   "
        )
        self.sld_level_cursor_position.value = self.time_cursor_position
        self.sld_level_cursor_position.on_value_changing.append(
            self.on_sld_level_cursor_position
        )
        self.em.add(self.sld_level_cursor_position)

        self.btn_left_time_to_selected = gui.Button("Left=E", self.grid_pos(start_col+6, 0), self.grid_size(2,1))
        self.btn_left_time_to_selected.on_button_1.append(lambda btn: self.on_btn_time_to_selected("left"))
        self.em.add(self.btn_left_time_to_selected)

        self.btn_center_time_to_selected = gui.Button("Cntr=E", self.grid_pos(start_col+6+2, 0), self.grid_size(2,1))
        self.btn_center_time_to_selected.on_button_1.append(lambda btn: self.on_btn_time_to_selected("center"))
        self.em.add(self.btn_center_time_to_selected)

        self.btn_right_time_to_selected = gui.Button("Right=E", self.grid_pos(start_col+6+4, 0), self.grid_size(2,1))
        self.btn_right_time_to_selected.on_button_1.append(lambda btn: self.on_btn_time_to_selected("right"))
        self.em.add(self.btn_right_time_to_selected)

        self.btn_cursor_to_selected = gui.Button("Cursor to Selected", self.grid_pos(start_col+6, 1), self.grid_size(6,1))
        self.btn_cursor_to_selected.on_button_1.append(self.on_btn_cursor_to_selected)
        self.em.add(self.btn_cursor_to_selected)

        self.btn_insert_time = gui.Button("Insert Time at Selected", self.grid_pos(start_col+6, 2), self.grid_size(6,1))
        self.btn_insert_time.on_button_1.append(self.on_btn_insert_time)
        self.em.add(self.btn_insert_time)


        self.time_slider = gui.TimelineSlider(
            Vector2(0, 800), Vector2(EDITOR_SCREEN_SIZE.x, 30)
        )
        self.time_slider.on_value_change.append(self.on_time_slider_change)
        self.em.add(self.time_slider)

        self.btn_time_window_start = gui.ButtonTimeCursor(
            "---", (100 - 50, 3), self.grid_size(3, 1), "center"
        )
        self.btn_time_window_start.on_button_1.append(
            lambda btn: self.set_time_cursor_position(0.0)
        )
        self.em.add(self.btn_time_window_start)

        self.btn_time_window_mid = gui.ButtonTimeCursor(
            "---",
            (612 - 50, 3),
            self.grid_size(3, 1),
            "center",
        )
        self.btn_time_window_mid.on_button_1.append(
            lambda btn: self.set_time_cursor_position(0.5)
        )
        self.em.add(self.btn_time_window_mid)

        self.btn_time_window_end = gui.ButtonTimeCursor(
            "---",
            (1124 - 50, 3),
            self.grid_size(3, 1),
            "center",
        )
        self.btn_time_window_end.on_button_1.append(
            lambda btn: self.set_time_cursor_position(1.0)
        )
        self.em.add(self.btn_time_window_end)
        self.update_time_curosr_elements()

        self.btn_play = gui.Button("Play", self.grid_pos(12,3), self.grid_size(2,1), align="left")
        self.btn_play.on_button_1.append(self.on_btn_play)
        self.em.add(self.btn_play)
    
        self.rbr_move = gui.RubberBand(self.grid_pos(12, 4), self.grid_size(), label="Scrub")
        self.rbr_move.on_value_changing.append(self.on_rbr_changing)
        self.em.add(self.rbr_move)

    def on_rbr_changing(self, elapsed, value):
        self.time += elapsed * value * 8
        self.update_time_curosr_elements()
        self.set_time_slider_value(self.time)

        # self.update()

    def on_btn_play(self, btn):
        if btn.text == "Play":
            btn.text = "Stop"
            current_scene.play_time = True
            btn.toggled = True
        else:
            btn.text = "Play"
            current_scene.play_time = False 
            btn.toggled = False

    def on_btn_insert_time(self, btn):
        def on_insert(panel, value):
            panel.close()
            self.em.delete(panel)
            start_time = self.time_cursor
            current_level.insert_time(start_time, value)
            self.update_after_duration_change()
            #Update Markers and Push out if in the gap
            for i in range(2):
                if current_scene.gui_level_marker.marker_time[i] >= start_time:
                    current_scene.gui_level_marker.marker_time[i] += value
            current_scene.gui_level_marker.update()


        def on_cancel(panel):
            self.em.delete(panel)
        panel = InsertTimePanel(on_insert)
        panel.on_cancel.append(on_cancel)
        self.em.add(panel)
        panel.show()

    def update_after_duration_change(self):
        #Update Time Details
        self.txt_level_total_time.text = int(current_level.total_time)
        self.time = (
            self.level.total_time
            - (EDITOR_SCREEN_RECT.w / SKY_VELOCITY)
            + ((EDITOR_SCREEN_RECT.w - 1124) / SKY_VELOCITY)
        ) * self.time_slider.value
        self.txt_level_pixel_length.text = self.level.pixel_length
        #Update Cursor
        self.update_time_curosr_elements()
        
        #Update Properties
        current_scene.gui_level_chain.update()
        current_scene.gui_level_boss.update()
        current_scene.gui_level_control.update()

    def on_btn_cursor_to_selected(self, btn):
        if current_scene.selected_level_entity != None:
            entity_time = current_scene.selected_level_entity.time
            if entity_time >= self.time and entity_time < self.time + (1024/SKY_VELOCITY):
                d = entity_time - self.time
                self.time_cursor_position
                self.time_cursor_position = d / (1024/SKY_VELOCITY)

    def on_btn_time_to_selected(self, which):
        if current_scene.selected_level_entity != None:
            entity_time = current_scene.selected_level_entity.time
            if which == "left":
                self.time = entity_time
            elif which == "center":
                self.time = entity_time - (512 / SKY_VELOCITY)
            elif which == "right":
                self.time = entity_time - (1024 / SKY_VELOCITY)
            self.update_time_curosr_elements()
            self.set_time_slider_value(self.time)

    def update_time_curosr_elements(self):
        self.btn_time_window_start.text = "{:,.02f}".format(self.time)
        self.btn_time_window_end.text = "{:,.02f}".format(
            self.time + (1024 / SKY_VELOCITY)
        )
        self.btn_time_window_mid.text = "{:,.02f}".format(
            self.time + (512 / SKY_VELOCITY)
        )
        self.txt_time_value.text = self.time
        self.txt_time_cursor_position.text = self.time_cursor

    @property
    def time_cursor(self):
        return self.time + (1024 / SKY_VELOCITY) * self.time_cursor_position

    def set_time_slider_value(self, time_value):
        self.time_slider.set_value(time_value / self.level.total_time)
        v = time_value / (
            self.level.total_time
            - (EDITOR_SCREEN_RECT.w / SKY_VELOCITY)
            + ((EDITOR_SCREEN_RECT.w - 1024) / SKY_VELOCITY)
        )
        self.time_slider.set_value(v)

    def on_txt_time_value(self, txt):
        self.time = txt.value
        self.update_time_curosr_elements()
        self.set_time_slider_value(self.time)

    def on_time_slider_change(self, time_slider):
        self.time = (
            self.level.total_time
            - (EDITOR_SCREEN_RECT.w / SKY_VELOCITY)
            + ((EDITOR_SCREEN_RECT.w - 1024) / SKY_VELOCITY)
        ) * time_slider.value

    def on_sld_level_cursor_position(self, sld):
        self.time_cursor_position = sld.value
        self.update_time_curosr_elements()

    def on_txt_level_total_time(self, txt):
        self.level.change_length(txt.value)
        self.time = (
            self.level.total_time
            - (EDITOR_SCREEN_RECT.w / SKY_VELOCITY)
            + ((EDITOR_SCREEN_RECT.w - 1124) / SKY_VELOCITY)
        ) * self.time_slider.value
        self.txt_level_pixel_length.text = self.level.pixel_length

    def set_time_cursor_position(self, value):
        if value < 0:
            value = 0.0
        elif value > 1.0:
            value = 1.0
        self.time_cursor_position = value
        self.sld_level_cursor_position.value = value
        self.update_time_curosr_elements()

    def draw_time_cursor(self, surface):
        d, yellow = 8, (255, 255, 0)
        x = (self.time_cursor_position * 1024.0) + 100
        pygame.draw.line(surface, yellow, (x, 100), (x - d, 100 - d))
        pygame.draw.line(surface, yellow, (x - d, 100 - d), (x + d, 100 - d))
        pygame.draw.line(surface, yellow, (x, 100), (x + d, 100 - d))
        pygame.draw.line(surface, yellow, (x, 700), (x - d, 700 + d))
        pygame.draw.line(surface, yellow, (x - d, 700 + d), (x + d, 700 + d))
        pygame.draw.line(surface, yellow, (x, 700), (x + d, 700 + d))
        pygame.draw.line(surface, yellow, (x, 100), (x, 700))

    def draw(self, elapsed, surface):
        grey = (80, 80, 80)
        # Time Window Label Leader Lines
        pygame.draw.line(surface, grey, (100, 27), (100, 100))
        pygame.draw.line(surface, grey, (612, 27), (612, 100))
        pygame.draw.line(surface, grey, (1124, 27), (1124, 100))
        # Time Window Curos Triangles / Center of Window
        self.draw_time_cursor(surface)
