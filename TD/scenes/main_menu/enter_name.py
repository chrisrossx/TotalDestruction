import pygame 
from pygame import Vector2
from blinker import signal 

from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
from TD.savedata import save_data


class EnterPlayerName(MenuScreen):
    def __init__(self) -> None:
        self.lbl_name = None
        self.text_line = ""
        super().__init__()
        self.cursor_elapsed = 0
        self.cursor_shown = True
        self.cursor_rect = pygame.Rect(0,0, 8, 5)

    def activate(self):
        signal("debugger.disable_input").send()

    def deactivate(self):
        self.text_line = ""
        signal("debugger.enable_input").send()

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("Enter Player Name:", self.font_m, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 100)
        self.em.add(lbl_hero)

        self.lbl_name = gui.GUILabel("{}".format(self.text_line), self.font_s, (250,206,72), shadow_color=(100,100,100))
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

    def set_data(self, data):
        self.slot_index = data["slot_index"]

    def tick(self, elapsed):
        super().tick(elapsed)
        self.cursor_elapsed += elapsed
        if self.cursor_elapsed >= 500:
            self.cursor_elapsed = 0
            self.cursor_shown = not self.cursor_shown

    def draw(self, elapsed):
        self.lbl_name.set_text(self.text_line)
        self.lbl_name.centerx_in_rect(SCREEN_RECT)
        super().draw(elapsed)
        # pos = .copy()
        lbl_rect = self.lbl_name.get_rect()
        lbl_rect.topleft = self.lbl_name.pos
        self.cursor_rect.x = lbl_rect.right + 0
        self.cursor_rect.y = lbl_rect.bottom - 8
        
        if self.cursor_shown and not self.transitioning:
            pygame.draw.rect(self.surface, (255,255,255), self.cursor_rect)

    def on_event(self, event, elapsed):
        if not self.transitioning:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    signal("menu_screen.start_transition").send(screen_name="select_player", direction="left")
                elif event.key == pygame.K_RETURN:
                    save_data.slots[self.slot_index].name = self.text_line
                    save_data.index = self.slot_index
                    signal("menu_screen.start_transition").send(screen_name="level_select", direction="right", data={"slot_index": self.slot_index})
                
                # Check for backspace
                elif event.key == pygame.K_BACKSPACE:
                    self.text_line = self.text_line[:-1]
                else:
                    if len(self.text_line) < 15:
                        self.text_line += event.unicode

