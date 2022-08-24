import pygame 
from pygame import Vector2

from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
# from TD.savedata import save_data
from TD.entity import Entity, EntityType
from TD.assetmanager import asset_manager
from TD import current_scene, current_app

class ReturnLevelScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.level = None
        self.level_data = None

    def set_data(self, data):
        self.level_data = data 

    def activate(self): 
        current_scene.start_transition(screen_name="level_score", direction="left", data=self.level_data)

class LevelScoreScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.slot_index = 0

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("Level Score", self.font_m, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 100)
        self.em.add(lbl_hero)

        lbl_press_enter = gui.GUILabel("Enter: Done", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_enter.rjust_in_rect(menu_rect, -40)
        lbl_press_enter.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_enter)

        # lbl_press_esc = gui.GUILabel("Esc: Go Back", self.font_s, (255,255,255), shadow_color=(80,80,80))
        # lbl_press_esc.ljust_in_rect(menu_rect, 40)
        # lbl_press_esc.tjust_in_rect(menu_rect, 550)
        # self.em.add(lbl_press_esc)
        # self.pos = Vector2(0,0)

  
    def deactivate(self):
        pass

    def activate(self):
        pass

    def set_data(self, data):
        print("datax", data)

    def on_event(self, event, elapsed):
        
        if not self.transitioning:
        
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                current_scene.start_transition(screen_name="level_select", direction="left")
                current_app.mixer.play("menu click")
