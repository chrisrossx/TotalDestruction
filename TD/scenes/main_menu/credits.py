import pygame 
from pygame import Vector2

from TD.paths import path_data
from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
from TD.entity import Entity, EntityType, EntityPathFollower
from TD.particles.particles import ParticleEntityFollower
from TD.assetmanager import asset_manager
from TD.globals import current_app, current_scene

from TD.enemies.BT1 import EnemyBT1 
from TD.enemies.CX5B import EnemyCX5B
from TD.enemies.D2 import EnemyD2
from TD.enemies.T8 import EnemyT8
from TD.enemies.HX7 import EnemyHX7
from TD.characters import SawyerPathFollower, EllePathFollower, MaiAnhPathFollower, ChristopherPathFollower


class XD15(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.ENEMY
        self.add_hitbox(pygame.Rect(0,0,40,40), Vector2(-20, -20))
        pos = Vector2(0, 0)
        for frame in asset_manager.sprites["XD15"]:
            surface = pygame.transform.flip(frame, True, False)
            self.frames.append(surface)
            
        self.sprite_offset = pygame.Vector2(self.get_rect().w / 2, self.get_rect().h / 2) * -1
        self.frame_duration = 120


class B4(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.ENEMY
        self.add_hitbox(pygame.Rect(0,0,40,40), Vector2(-20, -20))
        pos = Vector2(0, 0)

        for i in range(3):
            surface = pygame.Surface((128, 128), pygame.SRCALPHA)
            surface.blit(asset_manager.sprites["Boss 004 top"][0], pos)
            surface.blit(asset_manager.sprites["Boss 004 bottom"][i], pos)
            surface.blit(asset_manager.sprites["Boss 004 missiles"][0], pos)
            self.frames.append(surface)
        self.sprite_offset = Vector2(-64, -64)
        self.frame_duration = 120


class B3(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.ENEMY
        self.add_hitbox(pygame.Rect(0,0,40,40), Vector2(-20, -20))
        pos = Vector2(0, 0)

        a = 0
        b = 4
        c = 8
        for i in range(11):
            surface = pygame.Surface((71, 100), pygame.SRCALPHA)
            surface.blit(asset_manager.sprites["Boss 003"][0], pos)
            surface.blit(asset_manager.sprites["Boss 003 laser pod"][0], pos + Vector2(19, 65))
            surface.blit(asset_manager.sprites["Boss 003 rail gun"][0], pos + Vector2(24, 44))
            a = a + 1 if a < 10 else 0
            surface.blit(asset_manager.sprites["Boss 003 laser dot"][a], pos + Vector2(19, 71))
            b = b + 1 if b < 10 else 0
            surface.blit(asset_manager.sprites["Boss 003 laser dot"][b], pos + Vector2(19, 71))
            c = c + 1 if c < 10 else 0
            surface.blit(asset_manager.sprites["Boss 003 laser dot"][c], pos + Vector2(19, 71))
            self.frames.append(surface)
        
        self.frame_duration = 120
        self.center_sprite_offset()

class B2(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.ENEMY
        self.add_hitbox(pygame.Rect(0,0,40,40), Vector2(-20, -20))
        pos = Vector2(0, 0)

        for i in range(4):
            surface = pygame.Surface((128, 128), pygame.SRCALPHA)
            surface.blit(asset_manager.sprites["Boss 002"][i], pos)
            surface.blit(asset_manager.sprites["Boss 002 launchers"][0], pos)
            self.frames.append(surface)
        self.sprite_offset = Vector2(-64, -64)
        self.frame_duration = 120

class B1(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.ENEMY
        self.add_hitbox(pygame.Rect(0,0,40,40), Vector2(-20, -20))
        pos = Vector2(0, 0)

        for i in range(3):
            surface = pygame.Surface((128, 128), pygame.SRCALPHA)
            surface.blit(asset_manager.sprites["Boss 001"][i], pos)
            surface.blit(asset_manager.sprites["Boss 001 laser"][0], pos)
            self.frames.append(surface)
        self.sprite_offset = Vector2(-64, -64)
        self.frame_duration = 120



class Balloons(ParticleEntityFollower):
    def __init__(self, follow_entity, follow_offset):
        super().__init__(follow_entity, follow_offset)
        self.frames = asset_manager.sprites["Balloons"]
        self.sprite_offset = Vector2(-20, -26)

    def tick(self, elapsed):
        super().tick(elapsed)

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

        lbl_pi = gui.GUILabel("π", self.font_xs, (205,205,205))
        lbl_pi.rjust_in_rect(SCREEN_RECT, 20)
        lbl_pi.bjust_in_rect(SCREEN_RECT, 20)
        self.em.add(lbl_pi)
        self.pi_rect = lbl_pi.surface.get_rect()
        self.pi_rect.x = lbl_pi.x
        self.pi_rect.y = lbl_pi.y
        self.show_the_net = False 

        dark_panel = Entity()
        size = Vector2(600, 190)
        dark_panel.frames = [pygame.Surface(size, pygame.SRCALPHA), ]
        pygame.draw.rect(dark_panel.frames[0], (0,0,0,50), (0,0,size.x, size.y), 0, 5)
        dark_panel.pos.x = SCREEN_RECT.center[0] - (size.x / 2)
        dark_panel.pos.y = 150
        self.em.add(dark_panel)

        lines = ["Created with Love for his family, Ma-ANh, Sawer and Elle.",
                 "Developed by Christopher Ross in the summer of 2022.",
                 "Written in python using the pygame library.",
                 "Circuit Nerd Studios, chris.rossx@gmail.com"]

        for i, line in enumerate(lines):
            lbl = gui.GUILabel(line, self.font_s, (255,255,255))
            lbl.pos.x = dark_panel.pos.x + 25
            lbl.pos.y = dark_panel.pos.y + 25 + (i * 40)
            self.em.add(lbl)

        # Trigger Showing Enemy Name Labels
        self.show_enemy_name = Entity()
        self.show_enemy_name.type = EntityType.PARTICLE
        self.show_enemy_name.pos = Vector2(512+35, 440)
        self.show_enemy_name.add_hitbox(pygame.Rect(0, 0, 10, 50), Vector2(-5, 0))
        self.em.add(self.show_enemy_name)

        enemies = [
            (ChristopherPathFollower, "Christopher"),
            (B4, "Boss 4"),
            (MaiAnhPathFollower, "Mai-Anh"),
            (B3, "Boss 3"),
            (SawyerPathFollower, "Sawyer"), 
            (B2, "Boss 2"),
            (EllePathFollower, "Elle"),
            (B1, "Boss 1"),
            (XD15, "XD15"),
            (EnemyD2, "D2"), 
            (EnemyBT1, "BT1"), 
            (EnemyHX7, "HX7"), 
            (EnemyCX5B, "CX5B"), 
            (EnemyT8, "T8"), 
        ]
        spacing = path_data["credits"].total_length / (len(enemies) + 0)

        for i, entity in enumerate([e[0] for e in enemies]):
            instance = entity("credits")
            instance.velocity = 0.081
            instance.path.distance = spacing * i
            instance.path.on_end_of_path.remove(instance.on_end_of_path)
            instance.on_end_of_path = lambda entity=instance: entity.path.loop()
            instance.path.on_end_of_path.append(instance.on_end_of_path)
            self.em.add(instance)
            if entity in [SawyerPathFollower, EllePathFollower, MaiAnhPathFollower, ChristopherPathFollower]:
                balloons = Balloons(instance, Vector2(-2,-56))
                self.balloons = balloons
                self.em.add(balloons)

        self.enemy_lables = {}
        for entity, label in enemies:
            lbl = gui.GUILabel(label, self.font_s, (255,255,255), shadow_color=(80,80,80))
            lbl.centerx_in_rect(SCREEN_RECT)
            lbl.pos.y = 500
            lbl.surface.set_alpha(0)
            self.em.add(lbl)
            self.enemy_lables[entity] = lbl
            # lbl.enabled = False
            # EnemyBT1: 
        # }
        self.fade_in = 0
        self.fade_in_elapsed = 0
        self.current_enemy_label = None


        self.the_net = gui.Sprite(asset_manager.sprites["the net"])
        self.the_net.center_in_rect(SCREEN_RECT)
        self.the_net.enabled = False
        self.em.add(self.the_net)


    def tick(self, elapsed):
        super().tick(elapsed)

        if self.current_enemy_label:

            self.fade_in_elapsed += elapsed
            fd = 500
            fo = 1250
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


        hits = self.em.collidetype(self.show_enemy_name, EntityType.ENEMY, False)
        hits2 = self.em.collidetype(self.show_enemy_name, EntityType.GUI, False)
        hits = hits + hits2
        if len(hits) > 0:
            for enemy in hits:
                if type(enemy) in self.enemy_lables and not self.current_enemy_label:
                    self.enemy_lables[type(enemy)].enabled = True
                    self.enemy_lables[type(enemy)].surface.set_alpha(0)
                    self.fade_in = 0
                    self.fade_in_elapsed = 0
                    self.current_enemy_label = self.enemy_lables[type(enemy)]

    def deactivate(self):
        if self.show_the_net:
            current_app.mixer.play_music("menu")
            self.show_the_net = False
            self.the_net.enabled = False 

    def activate(self):
        pass

    def set_data(self, data):
        pass

    def on_event(self, event, elapsed):
        
        if not self.transitioning:
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_app.mixer.play("menu click")
                current_scene.start_transition(screen_name="start_screen", direction="bottom")

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.show_the_net == True:
                    self.the_net.enabled = False 
                    self.show_the_net = False
                    current_app.mixer.play_music("menu")
                if self.pi_rect.collidepoint(event.pos) and self.show_the_net == False and pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    current_app.mixer.play_music("the net")
                    self.the_net.enabled = True 
                    self.show_the_net = True 

