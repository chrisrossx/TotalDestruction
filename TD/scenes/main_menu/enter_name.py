import pygame 
from pygame import Vector2

from TD.config import SCREEN_RECT
from TD import gui, current_app, current_scene
from .screen import MenuScreen
from TD.debuging import game_debugger
from TD.entity import Entity

class EnterPlayerName(MenuScreen):
    def __init__(self) -> None:
        self.lbl_name = None
        self.text_line = ""
        super().__init__()
        self.cursor_elapsed = 0
        self.cursor_shown = True
        self.cursor_rect = pygame.Rect(0,0, 10, 5)

    def activate(self):
        game_debugger.disable_input()

    def deactivate(self):
        self.text_line = ""
        game_debugger.enable_input()

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("Enter Player Name:", self.font_m, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 100)
        self.em.add(lbl_hero)

        dark_panel = Entity()
        size = Vector2(400, 50)
        dark_panel.frames = [pygame.Surface(size, pygame.SRCALPHA), ]
        # dark_panel.frames[0].fill((0,0,0,50))
        rect = (0,0,size.x, size.y)
        pygame.draw.rect(dark_panel.frames[0], (0,0,0,50),rect,0,5)
        dark_panel.pos = SCREEN_RECT.center - (size / 2)
        dark_panel.pos.y = 200-10
        self.em.add(dark_panel)

        # color = (250,206,72)
        # scolor = (100,100,100)
        # color = (255, 255, 255)
        color = (212, 175, 28)
        scolor = (0,0,0)
        self.lbl_name = gui.GUILabel("{}".format(self.text_line), self.font_s, color, shadow_color=scolor)
        self.lbl_name.center_in_rect(menu_rect)
        self.lbl_name.tjust_in_rect(menu_rect, 200)
        self.em.add(self.lbl_name)

        lbl_press_esc = gui.GUILabel("Esc: Go Back", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(menu_rect, 40)
        lbl_press_esc.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_esc)

        lbl_press_delete = gui.GUILabel("Enter: Confirm", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_delete.rjust_in_rect(menu_rect, 40)
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
        lbl_rect = self.lbl_name.get_rect()
        lbl_rect.topleft = self.lbl_name.pos
        self.cursor_rect.x = lbl_rect.right + 2
        self.cursor_rect.y = lbl_rect.bottom - 8
        
        if self.cursor_shown and not self.transitioning:
            pygame.draw.rect(self.surface, (255,255,255), self.cursor_rect)

    def on_event(self, event, elapsed):
        if not self.transitioning:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_scene.start_transition(screen_name="select_player", direction="left")
                    current_app.mixer.play("menu click")
                elif event.key == pygame.K_RETURN:
                    current_app.save_data.slots[self.slot_index].name = self.text_line
                    current_app.save_data.index = self.slot_index
                    current_app.save_data.save()
                    current_scene.start_transition(screen_name="level_select", direction="right")
                    current_app.mixer.play("menu click")
                
                # Check for backspace
                elif event.key == pygame.K_BACKSPACE:
                    self.text_line = self.text_line[:-1]
                    current_app.mixer.play("menu type")
                else:
                    if len(self.text_line) < 22:
                        self.text_line += event.unicode
                        current_app.mixer.play("menu type")

