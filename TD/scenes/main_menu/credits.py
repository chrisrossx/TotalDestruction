import pygame 
from pygame import Vector2

from TD.paths import path_data
from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
from TD.entity import Entity, EntityType
from TD.assetmanager import asset_manager
from TD.globals import current_app, current_scene

from TD.enemies.BT1 import EnemyBT1 
from TD.enemies.CX5B import EnemyCX5B
from TD.enemies.D2 import EnemyD2
from TD.enemies.T8 import EnemyT8
from TD.enemies.HX7 import EnemyHX7


class CreditScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.slot_index = 0

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("Total Destruction Credits", self.font_m, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 50)
        self.em.add(lbl_hero)

        lbl_press_esc = gui.GUILabel("Esc: Go Back", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(menu_rect, 40)
        lbl_press_esc.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_esc)
        # self.pos = Vector2(0,0)

        dark_panel = Entity()
        size = Vector2(600, 190)
        dark_panel.frames = [pygame.Surface(size, pygame.SRCALPHA), ]
        pygame.draw.rect(dark_panel.frames[0], (0,0,0,50), (0,0,size.x, size.y), 0, 5)
        dark_panel.pos.x = SCREEN_RECT.center[0] - (size.x / 2)
        dark_panel.pos.y = 150
        self.em.add(dark_panel)


        show_enemy_name = Entity()
        show_enemy_name.type = EntityType.PARTICLE
        show_enemy_name.pos = Vector2(512+75, 460)
        show_enemy_name.add_hitbox(pygame.Rect(0, 0, 10, 50), Vector2(-5, 0))
        self.em.add(show_enemy_name)

        lines = ["A Python pygame created by Christopher Ross with love",
                 "for his children Sawyer and Elle!",
                 "Written in 2022",
                 "Produced by: Circuit Nerd Studios"]

        for i, line in enumerate(lines):
            lbl = gui.GUILabel(line, self.font_s, (255,255,255))
            lbl.pos.x = dark_panel.pos.x + 25
            lbl.pos.y = dark_panel.pos.y + 25 + (i * 40)
            self.em.add(lbl)

        def on_end_of_path(entity):
            entity.path.distance = 0

        spacing = path_data["credits"].total_length / 5

        for i, entity in enumerate([EnemyBT1, EnemyHX7, EnemyCX5B, EnemyD2, EnemyT8]):
            instance = entity("credits")
            instance.velocity = 0.1
            instance.path.distance = spacing * i
            instance.path.on_end_of_path.remove(instance.on_end_of_path)
            instance.on_end_of_path = lambda entity=instance: on_end_of_path(entity)
            instance.path.on_end_of_path.append(instance.on_end_of_path)
            self.em.add(instance)

        self.enemy_lables = {}
        for entity, label in [(EnemyBT1, "BT1"), (EnemyHX7, "HX7"), (EnemyCX5B, "CX5B"), (EnemyD2, "D2"), (EnemyT8, "T8")]:
            lbl = gui.GUILabel(label, self.font_s, (255,255,255), shadow_color=(80,80,80))
            lbl.centerx_in_rect(SCREEN_RECT)
            lbl.pos.y = 395
            lbl.surface.set_alpha(0)
            self.em.add(lbl)
            self.enemy_lables[entity] = lbl
            # lbl.enabled = False
            # EnemyBT1: 
        # }
        self.fade_in = 0
        self.fade_in_elapsed = 0
        self.current_enemy_label = None

    def tick(self, elapsed):
        super().tick(elapsed)


        if self.current_enemy_label:

            self.fade_in_elapsed += elapsed
            fd = 500
            fo = 1500
            if self.fade_in_elapsed <= fd:
                t = self.fade_in_elapsed / fd
                t = t * 255
                self.current_enemy_label.surface.set_alpha(t)
            if self.fade_in_elapsed >= fo and self.fade_in_elapsed <= fo + fd:
                t = (self.fade_in_elapsed - fo) / fd
                t = 255 - (t * 255)
                self.current_enemy_label.surface.set_alpha(t)
            if self.fade_in_elapsed >= fo + fd:
                self.current_enemy_label.enabled = False
                self.current_enemy_label = None


        hits = self.em.collidetypes(EntityType.PARTICLE, EntityType.ENEMY)
        if len(hits) > 0:
            for enemy in hits:
                if not self.current_enemy_label:
                    self.enemy_lables[type(enemy)].enabled = True
                    self.enemy_lables[type(enemy)].surface.set_alpha(0)
                    self.fade_in = 0
                    self.fade_in_elapsed = 0
                    self.current_enemy_label = self.enemy_lables[type(enemy)]

    def deactivate(self):
        pass

    def activate(self):
        pass

    def set_data(self, data):
        pass

    def on_event(self, event, elapsed):
        
        if not self.transitioning:
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_app.mixer.play("menu click")
                current_scene.start_transition(screen_name="start_screen", direction="bottom")
