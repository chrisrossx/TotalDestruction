import pygame 
from pygame import Vector2

from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
# from TD.savedata import save_data
from TD.entity import Entity, EntityType
from TD.assetmanager import asset_manager
from TD.globals import current_app, current_scene


class PlayerSlot(Entity):
    def __init__(self, index):
        super().__init__()
        self.type = EntityType.GUI

        self.frames = [pygame.Surface((300, 30), pygame.SRCALPHA),]
        self.selected = False
        self.font_s = asset_manager.fonts["sm"]
       
        self.index = index 
        self.player_slot = current_app.save_data.slots[index]
        

        self.render()

        # self.cursor_elapsed = 0
        # self.cursor_shown = True

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        # if self.cursor_shown and self.selected:
        #     s_rect = self.frames[0].get_rect()
        #     s_rect.topleft = self.pos
        #     pygame.draw.rect(surface, (255,255, 0, 155), s_rect, 2, 3)

    def tick(self, elapsed):
        super().tick(elapsed)
        # self.cursor_elapsed += elapsed
        # if self.cursor_elapsed >= 350:
            # self.cursor_elapsed = 0
            # self.cursor_shown = not self.cursor_shown

    def update(self):
        self.render()

    def render(self):
        surface = self.frames[0]
        # pygame.draw.rect(surface, (0,0,0,0), s_rect)
        surface.fill((255,255,255,0))
        s_rect = surface.get_rect()

        pygame.draw.rect(surface, (0,0,0,50), s_rect, 0, 3)
        p_rect = pygame.Rect(s_rect.w-77,0,77, s_rect.h)
        pygame.draw.rect(surface,(0,0,0,70), p_rect, 0, -1, 0, 3, 0, 3)
        if self.player_slot.name == None:
            name = "New Player"
            percent = "-- %"
        else:
            name = self.player_slot.name 
            percent = "{:.1%}".format(self.player_slot.percent)
        
        line = self.font_s.render(name, True, (255,255,255))
        surface.blit(line, (10, 2))
        line = self.font_s.render(percent, True, (225,225,225))
        p_rect = line.get_rect()
        surface.blit(line, (s_rect.w - p_rect.w - 10, 2))
       


class SelectPlayerScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.slot_index = 0

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("Select Player:", self.font_m, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 100)
        self.em.add(lbl_hero)

        lbl_press_enter = gui.GUILabel("Enter: Select Player", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_enter.center_in_rect(menu_rect)
        lbl_press_enter.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_enter)

        lbl_press_esc = gui.GUILabel("Esc: Go Back", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(menu_rect, 40)
        lbl_press_esc.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_esc)

        lbl_press_delete = gui.GUILabel("Delete: Delete Player", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_delete.rjust_in_rect(menu_rect, 40)
        lbl_press_delete.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_delete)

        self.left_cursor = gui.MenuCursor()
        self.left_cursor.x = 512-175
        self.left_cursor.y = 175 + (0 * 40) + 15
        self.em.add(self.left_cursor)
        
        self.right_cursor = gui.MenuCursor(True)
        self.right_cursor.x = 512+175
        self.right_cursor.y = 175 + (0 * 40) + 15
        self.em.add(self.right_cursor)

        self.player_slots = []
        x = 512 - 150
        y = 175
        for i, save_slot in enumerate(current_app.save_data.slots):
            player_slot = PlayerSlot(i)
            player_slot.pos = Vector2(x, y)
            y += player_slot.get_rect().h + 10
            self.player_slots.append(player_slot)
            self.em.add(player_slot)

        self.pos = Vector2(0,0)

    def update(self):
        for i, save_slot in enumerate(self.player_slots):
            save_slot.update()

    def update_select_slot(self):
        pass
        y = 175 + (self.slot_index * 40) + 15
        self.left_cursor.y = y
        self.right_cursor.y = y
    
    def deactivate(self):
        for i, save_slot in enumerate(self.player_slots):
            save_slot.selected = False 
        
    def activate(self):
        """Called after screen transition starts"""
        self.update_select_slot()

    def set_data(self, data):
        "Called before screen transition starts"
        self.update()

    def on_event(self, event, elapsed):
        
        if not self.transitioning:
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                if current_app.save_data.slots[self.slot_index].name != None:
                    current_scene.start_transition(screen_name="confirm_delete_player", direction="bottom", data={"slot_index": self.slot_index})
                    current_app.mixer.play("menu click")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_scene.start_transition(screen_name="start_screen", direction="left")
                current_app.mixer.play("menu click")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if current_app.save_data.slots[self.slot_index].name == None:
                    current_scene.start_transition(screen_name="enter_player_name", direction="right", data={"slot_index": self.slot_index})
                    current_app.mixer.play("menu click")
                else:
                    current_app.save_data.index = self.slot_index
                    current_scene.start_transition(screen_name="level_select", direction="right", data={"slot_index": self.slot_index})
                    current_app.mixer.play("menu click")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.slot_index += 1
                if self.slot_index >= len(current_app.save_data.slots):
                    self.slot_index = len(current_app.save_data.slots) - 1
                    current_app.mixer.play("menu error")
                else:
                    current_app.mixer.play("menu move")
                self.update_select_slot()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.slot_index -= 1
                if self.slot_index < 0:
                    self.slot_index = 0
                    current_app.mixer.play("menu error")
                else:
                    current_app.mixer.play("menu move")
                self.update_select_slot()
