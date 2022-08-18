import pygame 
from pygame import Vector2
from blinker import signal 

from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
from TD.assetmanager import asset_manager
from TD.scenes.main_menu.components import StartButton, StartButtonGroup, MuteButton


class StartScreen(MenuScreen):

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("[T]otal [D]estruction", self.font_l, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 100)
        self.em.add(lbl_hero)

        lbl_press_esc = gui.GUILabel("Esc: Exit", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(menu_rect, 40)
        lbl_press_esc.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_esc)

        self.left_cursor = gui.MenuCursor()
        self.left_cursor.x = 512-75
        self.em.add(self.left_cursor)
        
        self.right_cursor = gui.MenuCursor(True)
        self.right_cursor.x = 512+75
        self.em.add(self.right_cursor)

        self.btn_group = StartButtonGroup(self.on_button_press)
        self.em.add(self.btn_group)

        y, c = 280, 50        
        lbl = gui.GUILabel("Play", self.font_s, (255,255,255), shadow_color=(80,80,80))
        btn = StartButton("play", lbl.get_rect().size, lbl, bottom="mute", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(menu_rect)
        btn.pos.y = y
        self.btn_group.add(btn)

        size = (lbl.get_rect().w+30, lbl.get_rect().h)  #Same size as previous button to keep same spacing
        btn = MuteButton("mute", size, lbl, top="play", bottom="credits", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(menu_rect)
        btn.pos.y = y + c
        self.btn_group.add(btn)

        lbl = gui.GUILabel("Credits", self.font_s, (255,255,255), shadow_color=(80,80,80))
        btn = StartButton("credits", lbl.get_rect().size, lbl, top="mute", left_cursor=self.left_cursor, right_cursor=self.right_cursor)
        btn.centerx_in_rect(menu_rect)
        btn.pos.y = y + 2 * c
        self.btn_group.add(btn)

        self.btn_group.select("play", muted=True)

        # self.pos = Vector2(0,0)

    def on_button_press(self, name):
        if name == "play":
            signal("menu_screen.start_transition").send(screen_name="select_player", direction="right")
            signal("mixer.play").send("menu click")
        if name == "credits":
            signal("menu_screen.start_transition").send(screen_name="credits_screen", direction="top")
            signal("mixer.play").send("menu click")
        if name == "mute":
            mute = signal("mixer.is_muted").send()[0][1]
            signal("mixer.mute").send(not mute)
            signal("mixer.play").send("menu click")

    def on_event(self, event, elapsed):
        super().on_event(event, elapsed)
        if not self.transitioning:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                signal("mixer.play").send("menu click")
                signal("menu_screen.start_transition").send(screen_name="confirm_exit", direction="bottom")
