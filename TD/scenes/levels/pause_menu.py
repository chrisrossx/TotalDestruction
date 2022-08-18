from blinker import signal
from pygame import Vector2 
import pygame 

from TD.entity import Entity, EntityType
from TD.gui import GUIPanel, GUILabel, MenuCursor
from TD.assetmanager import asset_manager
from TD.config import SCREEN_RECT
from TD.scenes.main_menu.components import StartButton, StartButtonGroup, MuteButton
from TD import gui 


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

        self.btn_group = StartButtonGroup(self.on_button_press)
        self.em.add(self.btn_group)

        y, c = 280, 50        
        lbl = gui.GUILabel("Resume", asset_manager.fonts["sm"], (255,255,255), shadow_color=(80,80,80))
        btn = StartButton("resume", lbl.get_rect().size, lbl, bottom="mute", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(SCREEN_RECT)
        btn.pos.y = y
        self.btn_group.add(btn)

        size = (lbl.get_rect().w+30, lbl.get_rect().h)  #Same size as previous button to keep same spacing
        btn = MuteButton("mute", size, lbl, top="resume", bottom="exit", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(SCREEN_RECT)
        btn.pos.y = y + c
        self.btn_group.add(btn)

        lbl = gui.GUILabel("Exit Level", asset_manager.fonts["sm"], (255,255,255), shadow_color=(80,80,80))
        btn = StartButton("exit", lbl.get_rect().size, lbl, top="mute", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(SCREEN_RECT)
        btn.pos.y = y + 2 * c
        self.btn_group.add(btn)

        self.btn_group.select("resume", muted=True)

        signal("scene.paused").connect(self.on_scene_paused)

    def on_button_press(self, name):
        if name == "resume":
            signal("scene.paused").send(False)
        if name == "exit":
            signal("scene.exit").send({"condition": "exit"})
        if name == "mute":
            mute = signal("mixer.is_muted").send()[0][1]
            signal("mixer.mute").send(not mute)
            signal("mixer.play").send("menu click")

    def on_scene_paused(self, paused):
        if paused:
            self.enabled = True 
            self.btn_group.select("resume")
        else:
            self.enabled = False 

    def on_event(self, event, elapsed):
        self.em.on_event(event, elapsed, EntityType.GUI)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            signal("scene.paused").send(False)
