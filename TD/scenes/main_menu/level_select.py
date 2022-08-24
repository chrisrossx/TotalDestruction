import pygame 
from pygame import Vector2

from TD.config import SCREEN_RECT
from TD import gui, current_app, current_scene
from .screen import MenuScreen
from TD.entity import Entity, EntityType
from TD.assetmanager import asset_manager

class StartLevelScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.level = None

    def set_data(self, data):
        self.level = data["level"]

    def activate(self):
        current_scene.play_level({"scene":"play", "level": self.level})

class LevelSelectScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.slot_index = 0

    def render(self):
        lbl_hero = gui.GUILabel("Select Level:", self.font_m, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(SCREEN_RECT)
        lbl_hero.tjust_in_rect(SCREEN_RECT, 100)
        self.em.add(lbl_hero)

        lbl_press_enter = gui.GUILabel("Enter: Select Level", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_enter.rjust_in_rect(SCREEN_RECT, -40)
        lbl_press_enter.tjust_in_rect(SCREEN_RECT, 550)
        self.em.add(lbl_press_enter)

        lbl_press_esc = gui.GUILabel("Esc: Go Back", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(SCREEN_RECT, 40)
        lbl_press_esc.tjust_in_rect(SCREEN_RECT, 550)
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
                current_scene.start_transition(screen_name="select_player", direction="left")
                current_app.mixer.play("menu click")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                current_scene.start_transition(screen_name="start_level", direction="right", data={"level": "CHANGE ME"})
                current_app.mixer.play("menu click")
