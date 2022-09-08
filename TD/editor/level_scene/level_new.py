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


class NewPanel(gui.Panel):
    def __init__(self, on_new):
        panel_rows = 11
        panel_cols = 20
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, "New Level Entity")
        self.on_new = on_new

        self.lbl_control = gui.Label("Control Points", self.grid_pos(0,0), self.grid_size(), "center")
        self.lbl_chains = gui.Label("Enemy Chains", self.grid_pos(6,0), self.grid_size(8, 1), "center")
        self.lbl_boss = gui.Label("Boss", self.grid_pos(14,0), self.grid_size(), "center")
        self.em.add(self.lbl_control)
        self.em.add(self.lbl_chains)
        self.em.add(self.lbl_boss)

        self.btn_new_control = gui.Button("New Control", self.grid_pos(0, 1), self.grid_size())
        self.btn_new_control.on_button_1.append(self.on_new_control)
        self.em.add(self.btn_new_control)

        self.btn_new_boss = gui.Button("New Boss", self.grid_pos(14, 1), self.grid_size())
        self.btn_new_boss.on_button_1.append(self.on_btn_new_boss)
        self.em.add(self.btn_new_boss)

        self.btn_new_chain = gui.Button("New Enemy Chain", self.grid_pos(6, 1), self.grid_size(8, 1))
        self.btn_new_chain.on_button_1.append(self.on_btn_new_chain)
        self.em.add(self.btn_new_chain)

        self.btn_chain_pgup = gui.Button("PgUp", self.grid_pos(6, 2), self.grid_size(4, 1), "center")
        self.btn_chain_pgup.on_button_1.append(self.on_btn_chain_pgup)
        self.em.add(self.btn_chain_pgup)

        self.btn_chain_pgdn = gui.Button("PgDn", self.grid_pos(10, 2), self.grid_size(4, 1), "center")
        self.btn_chain_pgdn.on_button_1.append(self.on_btn_chain_pgdn)
        self.em.add(self.btn_chain_pgdn)

        self.chain_library_page = 0
        self.btns_chain_library = []
        for i in range(8):
            btn = gui.Button("", self.grid_pos(6, 3+i), self.grid_size(8, 1))
            index = i + (self.chain_library_page * 8)
            btn.on_button_1.append(lambda btn, index=index: self.on_btn_library(index))
            self.em.add(btn)
            self.btns_chain_library.append(btn)
        self.update_chain_library_btns()

    def on_btn_library(self, index):
        selected = current_scene.gui_level_chain_library.library.chains[index]
        chain = EnemyChain()
        chain.load(selected.save())
        chain.time = current_scene.gui_level_size.time_cursor
        self.close()
        self.on_new(self, chain)

    def on_new_control(self, btn):
        control = Control()
        control.time = current_scene.gui_level_size.time_cursor
        self.close()
        self.on_new(self, control)

    def on_btn_chain_pgup(self, btn):
        if self.chain_library_page > 0:
            self.chain_library_page -= 1
        self.update_chain_library_btns()

    def on_btn_chain_pgdn(self, btn):
        if self.chain_library_page < 31:
            self.chain_library_page += 1
        self.update_chain_library_btns()

    def update_chain_library_btns(self):
        for i in range(8):
            btn = self.btns_chain_library[i]
            index = i + (self.chain_library_page * 8)
            chain = current_scene.gui_level_chain_library.library.chains[index]
            btn.text = "{}: {}".format(index, chain.name)

    def on_btn_new_boss(self, btn):
        boss = Boss()
        boss.time = current_scene.gui_level_size.time_cursor
        self.close()
        self.on_new(self, boss)

    def on_btn_new_chain(self, btn):
        chain = EnemyChain()
        chain.time = current_scene.gui_level_size.time_cursor
        self.close()
        self.on_new(self, chain)

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        s = 2
        for x in [self.lbl_control.rect.right + s, self.lbl_chains.rect.right + s]:
            y = self.pos.y + 34
            pygame.draw.line(surface, (80,80,80), (x, y), (x, self.rect.bottom -2))


class GUILevelNew(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

        # -------------------------
        self.btn_new = gui.Button("New Entity", self.grid_pos(0, 4), self.grid_size(3, 1))
        self.btn_new.on_button_1.append(self.on_btn_new)
        self.em.add(self.btn_new)

        self.btn_copy = gui.Button("Copy Entity", self.grid_pos(0, 3), self.grid_size(3, 1))
        self.btn_copy.on_button_1.append(self.on_btn_copy)
        self.em.add(self.btn_copy)

        self.btn_paste = gui.Button("Paste Entity", self.grid_pos(3, 3), self.grid_size(3, 1))
        self.btn_paste.on_button_1.append(self.on_btn_paste)
        self.em.add(self.btn_paste)

        self.btn_delete = gui.Button("Delete Entity", self.grid_pos(3, 4), self.grid_size(3, 1))
        self.btn_delete.on_button_1.append(self.on_btn_delete)
        self.em.add(self.btn_delete)

        self.copied_entity = None 


    def on_btn_delete(self, btn):
        if current_scene.selected_level_entity != None:
            def confirm(btn):
                current_scene.selected_level_entity.delete()
                self.em.delete(panel)
                current_scene.select_level_entity(None)
            def cancel(btn):
                self.em.delete(panel)
            panel = gui.ConfirmPanel("Delete Entity?", confirm, cancel)
            self.em.add(panel)
            panel.show()


    def on_btn_copy(self, btn):
        #cache a copy incase we delete the original before paste!
        if current_scene.selected_level_entity != None:
            entity = current_scene.selected_level_entity
            copied = entity.__class__()
            copied.load(entity.save())        
            self.copied_entity = copied

    def on_btn_paste(self, btn):
        if self.copied_entity != None:
            #create another copy because we might paste more than once
            new = self.copied_entity.__class__()
            new.load(self.copied_entity.save())
            new.time = current_scene.gui_level_size.time_cursor
            current_level.add(new)
            current_scene.select_level_entity(new)

    def on_new(self, panel, level_entity):
        self.em.delete(panel)
        current_level.add(level_entity)
        current_scene.select_level_entity(level_entity)


    def on_event(self, event, elapsed):
        super().on_event(event, elapsed)
        if current_scene.gui_layer == 0:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_INSERT:
                self.on_btn_new(None)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                self.on_btn_delete(None)
        

    def on_btn_new(self, btn):
        panel = NewPanel(self.on_new)

        def on_cancel(panel):
            self.em.delete(panel)
        panel.on_cancel.append(on_cancel)
        self.em.add(panel)
        panel.show()
