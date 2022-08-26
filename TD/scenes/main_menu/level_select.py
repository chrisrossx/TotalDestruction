import pygame 
from pygame import Vector2

from TD.config import SCREEN_RECT
from TD import gui, current_app, current_scene
from .screen import MenuScreen
from TD.entity import Entity, EntityType
from TD.assetmanager import asset_manager
from TD.scenes.main_menu.components import LevelBadge, LevelBadgeCursor, LevelSelectLines

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
        # self.slot_index = 0
        self.cursor_index = 0

    def activate(self):
        self.update()
        
    def update(self):
        name = current_app.save_data.name
        self.lbl_player_name.set_text("Player: {}".format(name))
        self.cursor.enabled = True 
        self.cursor.frame_index = 1
        self.set_badges()

    def set_badges(self):
        b1 = self.badges[0]
        b1.update()

        b2 = self.badges[1]
        b2.update()

        # for i in range(2, 4):
        #     b = self.badges[i]
        #     b.disabled()

    def render(self):

        self.lbl_player_name = gui.GUILabel("Player:", self.font_s, (255,255,255), shadow_color=(80,80,80))
        self.lbl_player_name.ljust_in_rect(SCREEN_RECT, 40)
        self.lbl_player_name.tjust_in_rect(SCREEN_RECT, 22)
        self.em.add(self.lbl_player_name)

        lbl_press_enter = gui.GUILabel("Enter: Select Level", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_enter.rjust_in_rect(SCREEN_RECT, 40)
        lbl_press_enter.tjust_in_rect(SCREEN_RECT, 550)
        self.em.add(lbl_press_enter)

        lbl_press_esc = gui.GUILabel("Esc: Go Back", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(SCREEN_RECT, 40)
        lbl_press_esc.tjust_in_rect(SCREEN_RECT, 550)
        self.em.add(lbl_press_esc)
        self.pos = Vector2(0,0)

        lines = LevelSelectLines()
        lines.centerx_in_rect(SCREEN_RECT)
        lines.y = 360
        self.em.add(lines)

        self.cursor = LevelBadgeCursor()
        self.cursor.pos = Vector2(150, 300)
        self.em.add(self.cursor)

        self.badge_pos = [
            Vector2(150, 300),
            Vector2(395, 340),
            Vector2(640, 285),
            Vector2(875, 180),
        ]

        self.badges = []
        for i in range(4):
            badge = LevelBadge(i)
            badge.pos = self.badge_pos[i]
            badge.disabled()
            self.badges.append(badge)
            self.em.add(badge)
    
    def set_data(self, data):
        # print(data)
        if data and "level" in data:
            self.set_cursor(data["level"])
        self.cursor.enabled = False
        self.update()
        pass

    def set_cursor(self, index):
        self.cursor_index = index 
        self.cursor.frame_index = 0
        self.cursor.pos = self.badge_pos[self.cursor_index].copy()

    def on_event(self, event, elapsed):
        
        if not self.transitioning:
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_scene.start_transition(screen_name="select_player", direction="left")
                current_app.mixer.play("menu click")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.cursor_index < 2:
                    current_scene.start_transition(screen_name="start_level", direction="right", data={"level": self.cursor_index})
                    current_app.mixer.play("menu click")
                else:
                    current_app.mixer.play("menu error")
                    

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                index = self.cursor_index - 1
                if index < 0:
                    index = 0
                    current_app.mixer.play("menu error")
                else:
                    current_app.mixer.play("menu move")
                self.set_cursor(index)
                

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                index = self.cursor_index + 1
                if index == 4:
                    index = 3
                    current_app.mixer.play("menu error")
                else:
                    current_app.mixer.play("menu move")
                self.set_cursor(index)
