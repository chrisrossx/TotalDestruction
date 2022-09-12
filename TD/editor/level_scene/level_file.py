import subprocess
import os 
import sys
from pathlib import Path 
import traceback

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
from TD.editor.globals import current_level, current_scene
from TD.paths import path_data
from TD.levels.data import LevelEntityType


class SavePanel(gui.Panel):
    def __init__(self):
        panel_rows = 2
        panel_cols = 12
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "Save File")

        self.txt_filename = gui.TextBox(current_level.filename, self.grid_pos(0,0), self.grid_size(10, 1), label="Filename: ")
        self.txt_filename.on_value_changed.append(self.on_txt_filename)
        self.em.add(self.txt_filename)
        
        self.btn_filename_minus = gui.Button("-", self.grid_pos(10, 0), self.grid_size(1,1), "center")
        self.btn_filename_minus.on_button_1.append(self.on_btn_filename_minus)
        self.em.add(self.btn_filename_minus)
        self.btn_filename_plus = gui.Button("+", self.grid_pos(11, 0), self.grid_size(1,1), "center")
        self.btn_filename_plus.on_button_1.append(self.on_btn_filename_plus)
        self.em.add(self.btn_filename_plus)

        self.txt_exists = gui.TextBox("", self.grid_pos(0, 1), self.grid_size(6, 1), label="Exists:   ")
        self.txt_exists.editable = False
        self.em.add(self.txt_exists)

        self.btn_save = gui.Button("Save Level", self.grid_pos(6, 1), self.grid_size(), "center")
        self.btn_save.on_button_1.append(self.on_btn_save)
        self.em.add(self.btn_save)



        self.update()


    def on_btn_save(self, btn):
        path = current_level.base_path / self.txt_filename.text
        if self.txt_filename.text != None:
            if path.exists():
                panel = gui.ConfirmPanel("Overwrite File?", lambda btn: self.save())
                current_scene.em.add(panel)
                panel.show()                
                exists = "True"
            else:
                self.save()

    def save(self):
        current_level.filename = self.txt_filename.text
        current_level.save()
        current_scene.gui_level_file.update()
        self.close()

    def on_btn_filename_minus(self, btn):
        path = Path(self.txt_filename.text)
        parts = path.stem.split(".")
        if len(parts) == 1:
            new_path = path.stem + ".001" + path.suffix
            self.txt_filename.text = str(new_path)
            self.update()
        elif len(parts) == 2:
            new_step = int(parts[1]) - 1
            if new_step >= 0:
                new_path = parts[0] + ".{:>03}".format(new_step) + path.suffix
                self.txt_filename.text = str(new_path)
                self.update()

    def on_btn_filename_plus(self, btn):
        path = Path(self.txt_filename.text)
        parts = path.stem.split(".")
        if len(parts) == 1:
            new_path = path.stem + ".001" + path.suffix
            self.txt_filename.text = str(new_path)
            self.update()
        elif len(parts) == 2:
            new_step = int(parts[1]) + 1
            if new_step < 999:
                new_path = parts[0] + ".{:>03}".format(new_step) + path.suffix
                self.txt_filename.text = str(new_path)
                self.update()

    def update(self):
        try:
            path = current_level.base_path / self.txt_filename.text
            if path.exists() and self.txt_filename.text != "":
                exists = "True"
            else:
                exists = "False"
        except:
            exists = "Error"
        self.txt_exists.text = "[{}]".format(exists)

    def on_txt_filename(self, txt):
        self.update()


class GUILevelFile(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self.txt_filename = gui.TextBox(current_level.filename, self.grid_pos(0,0), self.grid_size())
        self.txt_filename.editable = False
        self.txt_filename.on_value_changed.append(self.on_txt_filename)
        self.em.add(self.txt_filename)
        
        self.btn_save_file = gui.Button("Save", self.grid_pos(0,1), self.grid_size(3, 1))
        self.btn_save_file.on_button_1.append(self.on_btn_save)
        self.em.add(self.btn_save_file)
    
        self.btn_play_start = gui.Button("Play Start", self.grid_pos(3, 1), self.grid_size(3, 1))
        self.btn_play_start.on_button_1.append(self.on_btn_play_start)
        self.em.add(self.btn_play_start)

        self.btn_play_at_cursor = gui.Button("Play @win", self.grid_pos(3, 2), self.grid_size(3, 1))
        self.btn_play_at_cursor.on_button_1.append(self.on_btn_play_at_cursor)
        self.em.add(self.btn_play_at_cursor)

        self.proc = None 

        self.btn_reload_paths = gui.Button("Reload Code", self.grid_pos(0,2), self.grid_size(3, 1))
        self.btn_reload_paths.on_button_1.append(self.on_btn_reload_paths)
        self.em.add(self.btn_reload_paths)
       

    def on_btn_reload_paths(self, btn):
        import importlib 

        def reload_enemies():
            print("Reloading Enemy Modules")
            from TD.enemies import HX7
            from TD.enemies import BT1
            from TD.enemies import CX5B
            from TD.enemies import D2
            from TD.enemies import T8        

            for mod in [HX7, BT1, CX5B, D2, T8]:
                for attr in dir(mod):
                    if attr not in ('__name__', '__file__'):
                        delattr(mod, attr)

            HX7 = importlib.reload(HX7)
            BT1 = importlib.reload(BT1)
            CX5B = importlib.reload(CX5B)
            D2 = importlib.reload(D2)
            T8 = importlib.reload(T8)

        try:
            reload_enemies()
        except Exception as e:
            print("[ERROR RELOADING GUNS]")
            traceback.print_exc()
        
        def reload_gun():
            print("Reloading Gun Modules")
            from TD.guns import HX7
            from TD.guns import BT1
            from TD.guns import CX5B
            from TD.guns import D2
            from TD.guns import T8        

            for mod in [HX7, BT1, CX5B, D2, T8]:
                for attr in dir(mod):
                    if attr not in ('__name__', '__file__'):
                        delattr(mod, attr)

            HX7 = importlib.reload(HX7)
            BT1 = importlib.reload(BT1)
            CX5B = importlib.reload(CX5B)
            D2 = importlib.reload(D2)
            T8 = importlib.reload(T8)
        try:
            reload_gun()
        except Exception as e:
            print("[ERROR RELOADING GUNS]")
            traceback.print_exc()

        print("Reloading Paths")
        path_data.load()
        for chain in current_level.level_entities_by_type[LevelEntityType.ENEMY_CHAIN]:
            chain.path.set_new_path(chain.path_index)

        

    def update(self):
        self.txt_filename.text = current_level.filename

    def _start_level(self, start_time):
        if self.proc:
            if self.proc.poll() == None:
                self.proc.kill()
                self.proc = None                 
        filename = current_level.save_temp()

        my_env = os.environ.copy()
        my_env['td_show_debugger'] = "True"
        print(">>> python.exe td.py --file {} --start {}".format(filename, start_time))
        self.proc = subprocess.Popen("python.exe td.py --file {} --start {}".format(filename, start_time), text=True, bufsize=1, stdout=sys.stdout, stderr=subprocess.STDOUT, env=my_env)

    def on_btn_play_start(self, btn):
        self._start_level(1)

    def on_btn_play_at_cursor(self, btn):
        # self._start_level(int(current_scene.gui_level_size.time_cursor))
        self._start_level(int(current_scene.time))

    def on_txt_filename(self, txt):
        current_level.filename = txt.text

    def on_btn_save(self, btn):
        def on_cancel(panel):
            self.em.delete(panel)

        panel = SavePanel()
        self.em.add(panel)
        panel.show()
        # current_level.save()

    def draw(self, elapsed, surface):
        grey = (80, 80, 80)
        x = self.txt_filename.rect.right + 3
        pygame.draw.line(surface, grey, (x, EDITOR_SCREEN_RECT.bottom- 150), (x, EDITOR_SCREEN_RECT.bottom))
