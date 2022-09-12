from pathlib import Path
import json 

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
from TD.levels.data import EnemyChain, Boss, Control, LevelEntityControlType
from TD.editor.globals import current_level, current_scene



class ChainLibrary:
    def __init__(self):
        self.chains = [EnemyChain() for e in range(256)]
        self.protected = []
        self.load()

    def save(self):
        path = Path(__file__).parent / "chains.json"
        data = {}

        data["protected"] = [i for i in self.protected]
        data["chains"] = []
        for entity in self.chains:
            data["chains"].append(entity.save())

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        path = Path(__file__).parent / "chains.json"
        with open(path, "r") as f:
            data = json.load(f)
        

        self.protected = data["protected"]

        self.chains = []
        for entity_data in data["chains"]:
            e = EnemyChain()
            e.load(entity_data)
            self.chains.append(e)


class LibraryPanel(gui.Panel):
    def __init__(self, library):
        panel_rows = 9
        panel_cols = 20
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "Chain Library Manager")
        self.library = library

        self.btn_chain_pgup = gui.Button("PgUp", self.grid_pos(0, 0), self.grid_size(4, 1), "center")
        self.btn_chain_pgup.on_button_1.append(self.on_btn_chain_pgup)
        self.em.add(self.btn_chain_pgup)

        self.btn_chain_pgdn = gui.Button("PgDn", self.grid_pos(4, 0), self.grid_size(4, 1), "center")
        self.btn_chain_pgdn.on_button_1.append(self.on_btn_chain_pgdn)
        self.em.add(self.btn_chain_pgdn)

        self.txt_name = gui.TextBox("", self.grid_pos(8, 0), self.grid_size(), "Name: ")
        self.txt_name.on_value_changed.append(self.on_txt_name)
        self.em.add(self.txt_name)

        self.txt_enemy = gui.TextBox("", self.grid_pos(8, 1), self.grid_size(),  "Enemy: ")
        self.txt_enemy.editable = False
        self.em.add(self.txt_enemy)

        self.txt_path_index = gui.TextBox("", self.grid_pos(14, 1), self.grid_size(),  "Path: ")
        self.txt_path_index.editable = False
        self.em.add(self.txt_path_index)

        self.txt_count = gui.TextBox("", self.grid_pos(8, 2), self.grid_size(),  "Count: ")
        self.txt_count.editable = False
        self.em.add(self.txt_count)

        self.txt_spacing = gui.TextBox("", self.grid_pos(14, 2), self.grid_size(),  "Spacing: ")
        self.txt_spacing.editable = False
        self.em.add(self.txt_spacing)

        self.txt_guns = gui.TextBox("", self.grid_pos(8, 4), self.grid_size(),  "Guns:    ")
        self.txt_guns.editable = False
        self.em.add(self.txt_guns)

        self.txt_gun = gui.TextBox("", self.grid_pos(8, 5), self.grid_size(),  "Gun:    ")
        self.txt_gun.editable = False
        self.em.add(self.txt_gun)

        self.txt_upgrades = gui.TextBox("", self.grid_pos(14, 3), self.grid_size(),  "Upgrades: ")
        self.txt_upgrades.editable = False
        self.em.add(self.txt_upgrades)

        self.txt_coins = gui.TextBox("", self.grid_pos(14, 4), self.grid_size(), "Coins:    ")
        self.txt_coins.editable = False
        self.em.add(self.txt_coins)

        self.txt_hearts = gui.TextBox("", self.grid_pos(8, 3), self.grid_size(), "Hearts:  ")
        self.txt_hearts.editable = False
        self.em.add(self.txt_hearts)

        self.btn_clear = gui.Button("Clear Chain", self.grid_pos(8, 7), self.grid_size())
        self.btn_clear.on_button_1.append(self.on_btn_clear)
        self.em.add(self.btn_clear)

        self.btn_protected = gui.Button("Protected", self.grid_pos(14, 7), self.grid_size())
        self.btn_protected.on_button_1.append(self.on_btn_protected)
        self.em.add(self.btn_protected)

        self.btn_copy_from_selected = gui.Button("Copy from Selected", self.grid_pos(8, 8), self.grid_size())
        self.btn_copy_from_selected.on_button_1.append(self.on_btn_copy_from_selected)
        self.em.add(self.btn_copy_from_selected)

        self.btn_copy_to_selected = gui.Button("Copy to Selected", self.grid_pos(14, 8), self.grid_size())
        self.btn_copy_to_selected.on_button_1.append(self.on_btn_copy_to_selected)
        self.em.add(self.btn_copy_to_selected)

        self.chain_library_page = 0
        self.btns_chain_library = []
        self.selected_index = None
        for i in range(8):
            btn = gui.Button("", self.grid_pos(0, 1+i), self.grid_size(8, 1))
            btn.on_button_1.append(lambda btn, index=i: self.on_btn_chain_library(index))
            self.em.add(btn)
            self.btns_chain_library.append(btn)
        self.update_chain_library_btns()
        self.select_library(None)

    def on_btn_protected(self, btn):
        if self.selected_index in self.library.protected:
            self.library.protected.remove(self.selected_index)
        else:
            self.library.protected.append(self.selected_index)
        self.library.save()
        self.update_properities() 

    def on_btn_clear(self, btn):
        pass 

    def on_btn_copy_to_selected(self, btn):
        if self.selected_index == None:
            return 
        
        def confirm(btn):
            selected = current_scene.gui_level_chain.selected_chain
            data = self.library.chains[self.selected_index].save()
            time = selected.time
            selected.load(data)
            selected.time = time 
            current_scene.gui_level_chain.update()
        #     current_scene.em.delete(panel)
        # def cancel(btn):
        #     current_scene.em.delete(panel)
       
        panel = gui.ConfirmPanel("Confirm Override Selected Level Chain Data?", confirm, cancel)
        # panel.set_gui_level(current_scene.gui_layer + 1)
        current_scene.em.add(panel)
        panel.show()

    def on_btn_copy_from_selected(self, btn):
        if self.selected_index == None:
            return 

        def confirm(btn):
            selected = current_scene.gui_level_chain.selected_chain
            self.library.chains[self.selected_index].load(selected.save())
            self.update_chain_library_btns()
            self.update_properities()
            self.library.save()
            current_scene.em.delete(panel)
        def cancel(btn):
            current_scene.em.delete(panel)
       
        panel = gui.ConfirmPanel("Confirm Override Library Chain Data?", confirm, cancel)
        # panel.set_gui_level(current_scene.gui_layer + 1)
        current_scene.em.add(panel)
        panel.show()            

    def on_txt_name(self, txt):
        self.library.chains[self.selected_index].name = txt.value
        self.update_chain_library_btns()
        self.library.save() 
       

    def select_library(self, index):
        self.selected_index = index 
        if index == None:
            self.txt_name.disabled = True 
            self.txt_name.text = ""
            self.txt_coins.text = ""
            self.txt_guns.text = ""
            self.txt_gun.text = ""
            self.txt_upgrades.text = ""
            self.txt_hearts.text = ""
            self.txt_enemy.text = ""
            self.txt_count.text = ""
            self.txt_path_index.text = ""
            self.txt_spacing.text = ""
            self.btn_copy_from_selected.disabled = True 
            self.btn_copy_to_selected.disabled = True 
            self.btn_protected.disabled = True 
            self.btn_protected.toggled = False 
            self.btn_clear.disabled = True 
        else:
            self.update_properities()
        self.update_chain_library_btns()

    def update_properities(self):
        chain = self.library.chains[self.selected_index]
        self.btn_copy_to_selected.disabled = False
        self.txt_name.disabled = False 
        self.btn_protected.disabled = False 
        if self.selected_index in self.library.protected:
            self.btn_protected.toggled = True
            self.btn_clear.disabled = True
            self.btn_copy_from_selected.disabled = True
        else:
            self.btn_copy_from_selected.disabled = False
            self.btn_clear.disabled = False 
            self.btn_protected.toggled = False
        self.txt_name.text = chain.name
        guns = ""
        hearts = ""
        coins = ""
        upgrades = ""
        for i in range(chain.count):
            guns += "\u25CF" if i in chain.guns else "\u25CC"
            hearts += "\u25CF" if i in chain.hearts else "\u25CC"
            upgrades += "\u25CF" if i in chain.upgrades else "\u25CC"
            coins += "\u25CF" if i in chain.coins else "\u25CC"
        self.txt_coins.text = "[{}]".format(coins)
        self.txt_guns.text = "[{}]".format(guns)
        self.txt_upgrades.text = "[{}]".format(upgrades)
        self.txt_hearts.text = "[{}]".format(hearts)
        self.txt_count.text = str(chain.count)
        self.txt_gun.text = str(chain.gun)
        self.txt_spacing.text = str(chain.spacing)
        self.txt_path_index.text = str(chain.path_index)
        self.txt_enemy.text = str(chain.enemy)

    def on_btn_chain_library(self, btn_index):
        self.select_library(btn_index + (self.chain_library_page * 8))
        self.update_chain_library_btns()

    def on_btn_chain_pgup(self, btn):
        if self.chain_library_page > 0:
            self.chain_library_page -= 1
            self.select_library(None)
            self.update_chain_library_btns()

    def on_btn_chain_pgdn(self, btn):
        if self.chain_library_page < 31:
            self.chain_library_page += 1
            self.select_library(None)
            self.update_chain_library_btns()

    def update_chain_library_btns(self):
        for i in range(8):
            btn = self.btns_chain_library[i]
            index = i + (self.chain_library_page * 8)
            chain = self.library.chains[index]
            name = chain.name if chain.name != "" else "---"
            btn.text = "{}: {}".format(index, name)
            if index == self.selected_index:
                btn.toggled = True 
            else:
                btn.toggled = False 

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        s = 2
        for x in [self.btn_chain_pgdn.rect.right + s, self.btn_chain_pgdn.rect.right + s]:
            y = self.pos.y + 34
            pygame.draw.line(surface, (80,80,80), (x, y), (x, self.rect.bottom -2))

class GUILevelChainLibrary(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self.library = ChainLibrary()

    def show(self):
        def on_cancel(panel):
            self.em.delete(panel)

        panel = LibraryPanel(self.library)
        panel.on_cancel.append(on_cancel)
        self.em.add(panel)
        panel.show()
