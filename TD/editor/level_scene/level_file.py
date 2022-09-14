import subprocess
import os 
import sys
from pathlib import Path 
import traceback
import math 

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
from TD.editor.globals import current_level, current_scene, current_app
from TD.paths import path_data
from TD.levels.data import LevelEntityType



class LoadPanel(gui.Panel):
    def __init__(self):
        panel_rows = 18
        panel_cols = 36
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "Load File")

        self.file_offset = 0
        self.current_path = Path("TD/levels/").resolve()

        self.txt_path = gui.TextBox("", self.grid_pos(0,0), self.grid_size(15, 1), label="Path: ")
        self.txt_path.editable = False 
        self.em.add(self.txt_path)

        self.btn_refresh = gui.Button("Refresh", self.grid_pos(15, 0), self.grid_size(3, 1))
        self.btn_refresh.on_button_1.append(lambda btn: self.update())
        self.em.add(self.btn_refresh)

        self.btn_chain_pgup = gui.Button("PgUp", self.grid_pos(18, 0), self.grid_size(3, 1), "center")
        self.btn_chain_pgup.on_button_1.append(self.on_btn_pgup)
        self.em.add(self.btn_chain_pgup)

        self.btn_chain_pgdn = gui.Button("PgDn", self.grid_pos(21, 0), self.grid_size(3, 1), "center")
        self.btn_chain_pgdn.on_button_1.append(self.on_btn_pgdn)
        self.em.add(self.btn_chain_pgdn)

        self.sld_page = gui.SlideValueInt(0,255, self.grid_pos(24, 0), self.grid_size(12, 1))
        self.sld_page.on_value_changing.append(self.on_sld_changing)
        self.em.add(self.sld_page)

        self.file_btns = []
                
        self.rows = 17
        for col in range(3):
            for row in range(self.rows):
                btn = gui.Button("File {}".format(row + (col*self.rows)), self.grid_pos(col * 12, row + 1), self.grid_size(12, 1))
                btn.on_button_1.append(lambda btn, index=(row + (col*self.rows)): self.on_file_btn(index))
                self.em.add(btn)
                self.file_btns.append(btn)

        # self.filenames = [p for p in base_path.iterdir() if p.suffix == ".json"]

        self.folders = ["004", "003", "002", "001", "backups"]

        self.update()

    def on_event(self, event, elapsed):
        super().on_event(event, elapsed)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.on_btn_pgdn(None)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.on_btn_pgup(None)
            print(event)

    def on_sld_changing(self, sld):
        self.file_offset = sld.value * (self.rows * 3)
        self.update()

    @property
    def filenames(self):
        if self.current_path.is_dir():
            filenames = [p for p in self.current_path.iterdir() if p.suffix == ".json"]
        else:
            filenames = []
        if self.current_path == Path("TD/levels").resolve():
            for f in self.folders:
                filenames.insert(0, "[{}]".format(f))
        else:
            filenames.insert(0, "[..]")
        return filenames

    def on_btn_pgup(self, btn):
        if self.file_offset > 0:
            self.file_offset -= self.rows * 3
            self.sld_page.value = self.file_offset / (self.rows * 3)

            self.update()

    def on_btn_pgdn(self, btn):
        files = self.filenames
        count = len(files)
        last = (self.rows * 3) + (self.file_offset)

        if count > last:
            self.file_offset += self.rows * 3
            self.sld_page.value = self.file_offset / (self.rows * 3)
            self.update()


    def on_file_btn(self, btn_index):
        file_index = self.file_offset + btn_index
        filename = self.filenames[file_index]
        if filename == "[..]":
            self.current_path = self.current_path.parent 
            self.file_offset = 0
            self.update()
        elif type(filename) == str and filename.startswith("["):
            folder = filename[1:-1]
            self.current_path = self.current_path / folder
            self.file_offset = 0
            self.update()
        else:
            if self.current_path == Path("TD/levels").resolve():
                name = filename.name
            else:
                name = "{}/{}".format(self.current_path.name, filename.name)
            current_scene.load_level(name)
            self.close()


    def update(self):
        self.txt_path.text = str(self.current_path.resolve())
        files = self.filenames 
        count = len(files)
        max_pages = math.ceil(count / (self.rows * 3))
        self.sld_page.max_value = max_pages - 1
        for i, file_btn in enumerate(self.file_btns):
            file_index = self.file_offset + i
            if file_index < len(files):
                filename = files[file_index]
                if type(filename) == str:
                    file_btn.text = filename
                else:
                    file_btn.text = filename.name 
                file_btn.disabled = False
            else:
                file_btn.text = "" 
                file_btn.disabled = True 


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
        self.proc = None 

        self.txt_filename = gui.TextBox(current_level.filename, self.grid_pos(0,0), self.grid_size())
        self.txt_filename.editable = False
        self.txt_filename.on_value_changed.append(self.on_txt_filename)
        self.em.add(self.txt_filename)
        
        self.btn_save_file = gui.Button("Save", self.grid_pos(0,1), self.grid_size(2, 1))
        self.btn_save_file.on_button_1.append(self.on_btn_save)
        self.btn_save_file.on_ctrl_button_1.append(self.on_ctrl_btn_save)
        self.em.add(self.btn_save_file)
    
        self.btn_backup_file = gui.Button("B", self.grid_pos(2,1), self.grid_size(1, 1), "center")
        self.btn_backup_file.on_button_1.append(self.on_btn_backup)
        self.em.add(self.btn_backup_file)
    
        self.btn_play_start = gui.Button("Play Start F5", self.grid_pos(3, 1), self.grid_size(3, 1))
        self.btn_play_start.on_button_1.append(self.on_btn_play_start)
        self.em.add(self.btn_play_start)

        self.btn_play_at_cursor = gui.Button("Play @win F6", self.grid_pos(3, 2), self.grid_size(3, 1))
        self.btn_play_at_cursor.on_button_1.append(self.on_btn_play_at_cursor)
        self.em.add(self.btn_play_at_cursor)


        self.btn_reload_paths = gui.Button("Reload Code", self.grid_pos(0,4), self.grid_size(3, 1))
        self.btn_reload_paths.on_button_1.append(self.on_btn_reload_paths)
        self.em.add(self.btn_reload_paths)

        self.btn_load_file = gui.Button("Load File", self.grid_pos(0,2), self.grid_size(3, 1))
        self.btn_load_file.on_button_1.append(self.on_btn_load)
        self.em.add(self.btn_load_file)

        self.btn_new_file = gui.Button("New File", self.grid_pos(0,3), self.grid_size(3, 1))
        self.btn_new_file.on_button_1.append(self.on_btn_new)
        self.em.add(self.btn_new_file)

    def on_btn_new(self, btn):
        def on_confirm(self, panel):
            current_scene.load_level(None, no_backup=True)
        panel = gui.ConfirmPanel("Create New File?", on_confirm)
        self.em.add(panel)
        panel.show()

    def on_btn_reload_paths(self, btn):
        self.parent.level.save_backup("reload_code")
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
        self.parent.level.save_backup("start_level")
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

    def on_btn_backup(self, btn):
        self.parent.level.save_backup("backup")

    def on_btn_save(self, btn):
        panel = SavePanel()
        self.em.add(panel)
        panel.show()

    def on_ctrl_btn_save(self, btn):
        current_level.save()
        current_scene.gui_level_file.update()

    def on_btn_load(self, btn):
        panel = LoadPanel()
        self.em.add(panel)
        panel.show()

    def draw(self, elapsed, surface):
        grey = (80, 80, 80)
        x = self.txt_filename.rect.right + 3
        pygame.draw.line(surface, grey, (x, EDITOR_SCREEN_RECT.bottom- 150), (x, EDITOR_SCREEN_RECT.bottom))
