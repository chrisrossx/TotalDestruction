import pygame 
from pygame import Vector2
from blinker import signal 

from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen


class StartScreen(MenuScreen):

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("[T]otal [D]estruction", self.font_l, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 100)
        self.em.add(lbl_hero)

        lbl_press_enter = gui.GUILabel("Enter: Start Game", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_enter.center_in_rect(menu_rect)
        lbl_press_enter.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_enter)

        lbl_press_esc = gui.GUILabel("Esc: Exit", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(menu_rect, 40)
        lbl_press_esc.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_esc)

        lbl_press_delete = gui.GUILabel("?: Credits", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_delete.rjust_in_rect(menu_rect, -40)
        lbl_press_delete.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_delete)

        self.pos = Vector2(0,0)

    def on_event(self, event, elapsed):
        if not self.transitioning:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                signal("menu_screen.start_transition").send(screen_name="select_player", direction="right")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                signal("menu_screen.start_transition").send(screen_name="confirm_exit", direction="bottom")
            if event.type == pygame.KEYDOWN and event.unicode == "?":
                signal("menu_screen.start_transition").send(screen_name="credits_screen", direction="top")




