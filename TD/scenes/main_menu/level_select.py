import pygame 
from pygame import Vector2
from blinker import signal 

from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
from TD.savedata import save_data
from TD.entity import Entity, EntityType
from TD.assetmanager import asset_manager

class StartLevelScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.level = None

    def set_data(self, data):
        self.level = data["level"]

    def activate(self):
        signal("scene.play_level").send({"scene":"play", "level": self.level})

class LevelSelectScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.slot_index = 0

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("Select Level:", self.font_m, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 100)
        self.em.add(lbl_hero)

        lbl_press_enter = gui.GUILabel("Enter: Select Level", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_enter.rjust_in_rect(menu_rect, -40)
        lbl_press_enter.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_enter)

        lbl_press_esc = gui.GUILabel("Esc: Go Back", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(menu_rect, 40)
        lbl_press_esc.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_esc)
        self.pos = Vector2(0,0)

    
    def deactivate(self):
        pass

    def activate(self):
        pass

    def set_data(self, data):
        pass

    def on_event(self, event, elapsed):
        
        if not self.transitioning:
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                signal("menu_screen.start_transition").send(screen_name="select_player", direction="left")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                signal("menu_screen.start_transition").send(screen_name="start_level", direction="right", data={"level": 0})