from pygame import Vector2 
import pygame 

from TD.entity import Entity, EntityType
from TD.gui import GUIPanel, GUILabel, MenuCursor
from TD.assetmanager import asset_manager
from TD.config import SCREEN_RECT
from TD.scenes.main_menu.components import StartButton, StartButtonGroup, SoundsButton, MusicButton
from TD import gui, current_app, current_scene


class PauseMenu(GUIPanel):
    def __init__(self, size):
        super().__init__(size)
        self.type = EntityType.DIALOG

        self.pos = SCREEN_RECT.center - (size/2)
        self.background_color = (0,0,0,50)

        dark_panel = Entity()
        size = Vector2(400, 400)
        dark_panel.frames = [pygame.Surface(size, pygame.SRCALPHA), ]
        dark_panel.frames[0].fill((0,0,0,50))
        dark_panel.pos = SCREEN_RECT.center - (size / 2)
        self.em.add(dark_panel)

        p_rect = self.get_rect()
        line = GUILabel("Paused", asset_manager.fonts["md"], (255,255,255))
        line.center_in_rect(p_rect)
        line.pos.y -= 125
        self.em.add(line)

        self.left_cursor = MenuCursor()
        self.left_cursor.x = 512-70
        self.em.add(self.left_cursor)
        
        self.right_cursor = MenuCursor(True)
        self.right_cursor.x = 512+70
        self.em.add(self.right_cursor)

        self.btn_group = StartButtonGroup(self.on_button_press)
        self.em.add(self.btn_group)

        y, c = 280-25, 50        
        lbl = gui.GUILabel("Resume", asset_manager.fonts["sm"], (255,255,255), shadow_color=(80,80,80))
        btn = StartButton("resume", lbl.get_rect().size, lbl, bottom="sounds", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(SCREEN_RECT)
        btn.pos.y = y
        self.btn_group.add(btn)

        size = (lbl.get_rect().w+30, lbl.get_rect().h)  #Same size as previous button to keep same spacing
        btn = SoundsButton("sounds", size, lbl, top="resume", bottom="music", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(SCREEN_RECT)
        btn.pos.y = y + c
        self.btn_group.add(btn)

        size = (lbl.get_rect().w+30, lbl.get_rect().h)  #Same size as previous button to keep same spacing
        btn = MusicButton("music", size, lbl, top="sounds", bottom="exit", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(SCREEN_RECT)
        btn.pos.y = y + 2 * c
        self.btn_group.add(btn)

        lbl = gui.GUILabel("Exit Level", asset_manager.fonts["sm"], (255,255,255), shadow_color=(80,80,80))
        btn = StartButton("exit", lbl.get_rect().size, lbl, top="music", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(SCREEN_RECT)
        btn.pos.y = y + 3 * c
        self.btn_group.add(btn)

        self.btn_group.select("resume")


    def on_button_press(self, name):
        if name == "resume":
            current_scene.unpause()
        if name == "exit":
            current_scene.exit({"condition": "exit"})
        if name == "sounds":
            mute = current_app.mixer.is_sounds_muted()
            current_app.mixer.mute_sounds(not mute)
            if mute:
                current_app.mixer.play("menu click")
            self.btn_group["sounds"].render()
        if name == "music":
            mute = current_app.mixer.is_music_muted()
            current_app.mixer.mute_music(not mute)
            current_app.mixer.play("menu click")
            self.btn_group["music"].render()            

    def hide(self):
        self.enabled = False

    def show(self):
        self.enabled = True 
        self.btn_group.select("resume")

    def on_event(self, event, elapsed):
        self.em.on_event(event, elapsed, EntityType.GUI)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            current_scene.unpause()
