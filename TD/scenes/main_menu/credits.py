import pygame 
from pygame import Vector2
from blinker import signal 

from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
from TD.savedata import save_data
from TD.entity import Entity, EntityType
from TD.assetmanager import asset_manager

from TD.enemies.BT1 import EnemyBT1 
from TD.enemies.CX5B import EnemyCX5B
from TD.enemies.D2 import EnemyD2
from TD.enemies.T8 import EnemyT8


class CreditScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.slot_index = 0

    def render(self):
        menu_rect = SCREEN_RECT.copy()

        lbl_hero = gui.GUILabel("Total Destruction Credits", self.font_m, (255,255,255), shadow_color=(80,80,80), shadow_step=Vector2(6,6))
        lbl_hero.center_in_rect(menu_rect)
        lbl_hero.tjust_in_rect(menu_rect, 100)
        self.em.add(lbl_hero)

        lbl_press_esc = gui.GUILabel("Esc: Go Back", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_esc.ljust_in_rect(menu_rect, 40)
        lbl_press_esc.tjust_in_rect(menu_rect, 550)
        self.em.add(lbl_press_esc)
        self.pos = Vector2(0,0)
    
        # bt1 = EnemyBT1("credits")
        # bt1.velocity = 0
        # bt1.path.distance = 150

        # cx5b = EnemyCX5B("credits")
        # cx5b.velocity = 0
        # cx5b.path.distance = 150+241

        # d2 = EnemyD2("credits")
        # d2.velocity = 0
        # d2.path.distance = 150+241+241

        # t8 = EnemyT8("credits")
        # t8.velocity = 0
        # t8.path.distance = 150+241+241+241
        
        def on_end_of_path(entity):
            entity.path.distance = 0

        v = 0.1
        bt1 = EnemyBT1("credits 2")
        bt1.velocity = v
        bt1.path.distance = 442 * 0
        bt1.path.on_end_of_path.disconnect(bt1.on_end_of_path)
        bt1.on_end_of_path = lambda sender: on_end_of_path(bt1)
        bt1.path.on_end_of_path.connect(bt1.on_end_of_path)

        cx5b = EnemyCX5B("credits 2")
        cx5b.velocity = v
        cx5b.path.distance = 442 * 1
        cx5b.path.on_end_of_path.disconnect(cx5b.on_end_of_path)
        cx5b.on_end_of_path = lambda sender: on_end_of_path(cx5b)
        cx5b.path.on_end_of_path.connect(cx5b.on_end_of_path)

        d2 = EnemyD2("credits 2")
        d2.velocity = v
        d2.path.distance = 442 * 2
        d2.path.on_end_of_path.disconnect(d2.on_end_of_path)
        d2.on_end_of_path = lambda sender: on_end_of_path(d2)
        d2.path.on_end_of_path.connect(d2.on_end_of_path)

        t8 = EnemyT8("credits 2")
        t8.velocity = v
        t8.path.distance = 442 * 3
        t8.path.on_end_of_path.disconnect(t8.on_end_of_path)
        t8.on_end_of_path = lambda sender: on_end_of_path(t8)
        t8.path.on_end_of_path.connect(t8.on_end_of_path)
                
        self.em.add(bt1)
        self.em.add(cx5b)
        self.em.add(d2)
        self.em.add(t8)
        

    def deactivate(self):
        pass

    def activate(self):
        pass

    def set_data(self, data):
        pass

    def on_event(self, event, elapsed):
        
        if not self.transitioning:
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                signal("menu_screen.start_transition").send(screen_name="start_screen", direction="bottom")
                signal("mixer.play").send("menu click")
