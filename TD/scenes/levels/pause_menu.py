from blinker import signal
from pygame import Vector2 
import pygame 

from TD.entity import Entity, EntityType
from TD.gui import GUIPanel, GUILabel, MenuCursor
from TD.assetmanager import asset_manager
from TD.config import SCREEN_RECT


class PauseMenu(GUIPanel):
    def __init__(self, size):
        super().__init__(size)
        self.type = EntityType.DIALOG

        self.pos = SCREEN_RECT.center - (size/2)
        self.background_color = (0,0,0,50)

        p_rect = self.get_rect()
        line = GUILabel("Paused", asset_manager.fonts["md"], (255,255,255))
        line.center_in_rect(p_rect)
        line.pos.y -= 100
        self.em.add(line)

        p_rect = self.get_rect()
        line = GUILabel("Resume", asset_manager.fonts["sm"], (255,255,255))
        line.center_in_rect(p_rect)
        self.em.add(line)

        p_rect = self.get_rect()
        line = GUILabel("Exit Level", asset_manager.fonts["sm"], (255,255,255))
        line.center_in_rect(p_rect)
        line.pos.y += 40
        self.em.add(line)

        dark_panel = Entity()
        size = Vector2(400, 400)
        dark_panel.frames = [pygame.Surface(size, pygame.SRCALPHA), ]
        dark_panel.frames[0].fill((0,0,0,50))
        dark_panel.pos = SCREEN_RECT.center - (size / 2)
        self.em.add(dark_panel)

        self.left_cursor = MenuCursor()
        self.left_cursor.x = 512-70
        self.em.add(self.left_cursor)
        
        self.right_cursor = MenuCursor(True)
        self.right_cursor.x = 512+70
        self.em.add(self.right_cursor)

        self.cursor_index = 0
        self.set_cursor()

        signal("scene.paused").connect(self.on_scene_paused)


    def on_scene_paused(self, paused):
        if paused:
            self.enabled = True 
        else:
            self.enabled = False 

    def set_cursor(self):
        if self.cursor_index == 0:
            y = 300 - 3
        else:
            y = 340 - 3
        self.right_cursor.y = y
        self.left_cursor.y = y 

    def on_event(self, event, elapsed):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.cursor_index += 1
            if self.cursor_index > 1:
                self.cursor_index = 0
            self.set_cursor()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.cursor_index -= 1
            if self.cursor_index < 0:
                self.cursor_index = 1
            self.set_cursor()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            signal("scene.paused").send(False)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.cursor_index == 0:
            signal("scene.paused").send(False)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.cursor_index == 1:
            signal("scene.exit").send({"condition": "exit"})
          
