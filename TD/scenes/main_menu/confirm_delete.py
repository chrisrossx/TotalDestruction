import pygame 
from pygame import Vector2
from blinker import signal 

from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
from TD.savedata import save_data


class ConfirmDeletePlayer(MenuScreen):
    def __init__(self) -> None:
        self.lbl_name = None
        self.player_name = ""
        super().__init__()

    def deactivate(self):
        player_name = ""
        self.lbl_name.set_text("\"{}\"".format(player_name))
        self.lbl_name.centerx_in_rect(SCREEN_RECT)

    def set_data(self, data):
        self.slot_index = data["slot_index"]
        player_name = save_data.slots[self.slot_index].name
        self.lbl_name.set_text("\"{}\"".format(player_name))
        self.lbl_name.centerx_in_rect(SCREEN_RECT)

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("Confirm Player Data Delete?", self.font_m, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 100)
        self.em.add(lbl_hero)

        self.lbl_name = gui.GUILabel("\"{}\"".format(self.player_name), self.font_s, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        self.lbl_name.center_in_rect(menu_rect)
        self.lbl_name.tjust_in_rect(menu_rect, 200)
        self.em.add(self.lbl_name)

        lbl_press_esc = gui.GUILabel("Esc: Go Back", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(menu_rect, 40)
        lbl_press_esc.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_esc)

        lbl_press_delete = gui.GUILabel("Enter: Confirm", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_delete.rjust_in_rect(menu_rect, -40)
        lbl_press_delete.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_delete)

        self.pos = Vector2(0,0)

    def on_event(self, event, elapsed):
        if not self.transitioning:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                signal("menu_screen.start_transition").send(screen_name="select_player", direction="top")
                print("CONFIRED DELETE")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                signal("menu_screen.start_transition").send(screen_name="select_player", direction="top")

