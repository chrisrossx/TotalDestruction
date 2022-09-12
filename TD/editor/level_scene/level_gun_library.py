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
from TD import guns 



class SelectGunPanel(gui.Panel):
    def __init__(self, on_selected, current_value=None):
        panel_rows = 12
        panel_cols = 6 * 6
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "Choose Gun")

        self.on_selected = on_selected

        #Find Enemies
        # import sys

        enemy_types = [
            # [module, "class name beings with", "icon name"]
            [guns.CX5B, "GunCX5B"],
            [guns.T8, "GunT8"],
            [guns.HX7, "GunHX7"],
            [guns.D2, "GunD2"],
            [guns.BT1, "GunBT1"],
        ]
        
        for c, line in enumerate(enemy_types):
            mod, starts_with = line
            classnames = []
            
            for item in dir(mod):
                if item.startswith(starts_with):
                    classnames.append(item)
            
            lbl = gui.Label("{} Enemy Guns".format(starts_with[3:]), self.grid_pos((c*6), 0), self.grid_size(6, 1))
            self.em.add(lbl)
            for i, name in enumerate(classnames):
                btn = gui.Button(name[3:], self.grid_pos((c*6), 1 + (i*1)), self.grid_size(6, 1))
                if current_value == name:
                    btn.toggled = True
                btn.on_button_1.append(lambda btn, name=name: self.on_btn(name))
                self.em.add(btn)

        btn = gui.Button("None", self.grid_pos(5*6,panel_rows - 1), self.grid_size(6, 1))
        if current_value == None:
            btn.toggled = True
        btn.on_button_1.append(lambda btn: self.on_btn(None))
        self.em.add(btn)

    def on_btn(self, selection):
        self.close()
        self.on_selected(selection)



class GUILevelGunLibrary(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

    def show(self):
        def selected(gun):
            current_scene.gui_level_chain.selected_chain.gun = gun
            current_scene.gui_level_chain.update()
            self.em.delete(panel)
        panel = SelectGunPanel(selected, current_scene.gui_level_chain.selected_chain.gun)
        self.em.add(panel)
        panel.show()

    def showx(self):

        items = {}
        for gun in guns.keys():
            items[gun] = gun 
        items["None"] = None
        def on_choice(panel, value):
            current_scene.gui_level_chain.selected_chain.gun = value 
            current_scene.gui_level_chain.update()
        panel = gui.ChooseListPanel("Select Gun", items, current_scene.gui_level_chain.selected_chain.gun)
        panel.on_choice.append(on_choice)
        current_scene.em.add(panel)
        panel.show()
