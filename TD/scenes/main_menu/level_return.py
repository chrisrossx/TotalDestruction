import pygame 
from pygame import Vector2

from TD.config import SCREEN_RECT
from TD import gui
from .screen import MenuScreen
# from TD.savedata import save_data
from TD.entity import Entity, EntityType
from TD.assetmanager import asset_manager
from TD import current_scene, current_app
from TD.scenes.level.hud import HUDMedal100, HUDMedal70, HUDMedalHeart
from TD.scenes.main_menu.components import HUDMedalCoin, ScoreDividerBar, ScoreGoldConfetti, ScoreGoldConfetti2, ScoreGreyConfetti, ScoreGreyConfetti2

GOLD = (255, 196, 0)
GREY = (40, 40, 40)
STEP_DELAY = 650

class ReturnLevelScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.level = None
        self.level_data = None

    def set_data(self, data):
        self.level_data = data 

    def activate(self): 
        current_scene.start_transition(screen_name="level_score", direction="left", data=self.level_data)

class LevelScoreScreen(MenuScreen):


    def __init__(self):
        super().__init__()
        self.slot_index = 0
        self.total_elapsed = 0
        self.step = 0
        self.step_elapsed = 0
        self.tick_step = self.tick_step_000

        self._play_score_step = 0
    

    def next_step(self):
        self.step += 1
        self.step_elapsed = 0
        name = "tick_step_{:>03d}".format(self.step)
        if hasattr(self, name):
            self.tick_step = getattr(self, name)
        else:
            self.tick_step = lambda elapsed: None

    def play_score(self):
        if self._play_score_step == 0:
            current_app.mixer.play("menu score 1")
        if self._play_score_step == 1:
            current_app.mixer.play("menu score 2")
        if self._play_score_step >= 2:
            current_app.mixer.play("menu score 3")
        self._play_score_step += 1

    def tick_step_000(self, elapsed):
        
        if self.step_elapsed >= STEP_DELAY + 100:
            if self.level_state["coins"] >= 1.0:
                self.lbl_coins_result.color = GOLD
                self.medal_coin.gold()
                self.goldConfetti(self.medal_coin.pos + Vector2(16, 16))
            else:
                self.lbl_coins_result.color = GREY
                self.medal_coin.valid()
                self.greyConfetti(self.medal_coin.pos + Vector2(16, 16))
            current_app.mixer.play("menu score coins")
            self.lbl_coins_result.enabled = True 
            self.lbl_coins_result.set_text("{:.0%}".format(self.level_state["coins"]))
            self.lbl_coins_result.rjust_in_rect(SCREEN_RECT, 355)

            self.next_step()

    def goldConfetti(self, pos):
        self.em.add(ScoreGoldConfetti(pos))
        self.em.add(ScoreGoldConfetti2(pos + Vector2(8, 12)))
        self.em.add(ScoreGoldConfetti2(pos + Vector2(-11, -5)))

    def greyConfetti(self, pos):
        self.em.add(ScoreGreyConfetti(pos))
        self.em.add(ScoreGreyConfetti2(pos + Vector2(8, 12)))
        self.em.add(ScoreGreyConfetti2(pos + Vector2(-11, -5)))


    def tick_step_001(self, elapsed):
        if self.step_elapsed >= STEP_DELAY:
            if self.level_state["medalHeart"]:
                self.medal_heart.gold()
                self.goldConfetti(self.medal_heart.pos + Vector2(16, 16))
                self.play_score()
            else:
                current_app.mixer.play("menu score 0")
                self.medal_heart.valid()
                self.greyConfetti(self.medal_heart.pos + Vector2(16, 16))
            
            self.next_step()            

    def tick_step_002(self, elapsed):
        if self.step_elapsed >= STEP_DELAY:
            p70 = self.level_state["enemies"] if self.level_state["enemies"] < 0.7 else 0.7
            if p70 >= 0.7:
                self.lbl_70_result.color = GOLD
                self.medal_70.gold()
                self.play_score()
                pos = self.medal_70.pos + Vector2(16, 16)
                self.goldConfetti(self.medal_70.pos + Vector2(16, 16))
            else:
                self.lbl_70_result.color = GREY
                self.medal_70.valid()
                current_app.mixer.play("menu score 0")
                self.greyConfetti(self.medal_70.pos + Vector2(16, 16))
            self.lbl_70_result.set_text("{:.0%}".format(p70))
            self.lbl_70_result.enabled = True 
            self.lbl_70_result.rjust_in_rect(SCREEN_RECT, 355)
            self.next_step()            

    def tick_step_003(self, elapsed):
        if self.step_elapsed >= STEP_DELAY:
            if self.level_state["enemies"] >= 1.0:
                self.lbl_100_result.color = GOLD
                self.medal_100.gold()
                self.play_score()
                pos = self.medal_100.pos + Vector2(16, 16)
                self.goldConfetti(self.medal_100.pos + Vector2(16, 16))
            else:
                self.lbl_100_result.color = GREY
                self.medal_100.valid()
                current_app.mixer.play("menu score 0")
                self.greyConfetti(self.medal_100.pos + Vector2(16, 16))
            self.lbl_100_result.enabled = True 
            self.lbl_100_result.set_text("{:.0%}".format(self.level_state["enemies"]))
            self.lbl_100_result.rjust_in_rect(SCREEN_RECT, 355)

            self.next_step()            

    def tick(self, elapsed):
        self.total_elapsed += elapsed
        self.step_elapsed += elapsed
        self.tick_step(elapsed)
        super().tick(elapsed)

    def clear(self):

        self.step = 0
        self.step_elapsed

        self.medal_coin.valid()
        self.medal_heart.valid()
        self.medal_70.valid()

        self.lbl_70_result.color = GREY
        self.lbl_coins_result.color = GREY
        self.lbl_100_result.color = GREY

        self.lbl_70_result.enabled = False 
        self.lbl_coins_result.enabled = False 
        self.lbl_100_result.enabled = False


    def update(self):
        
        name = current_app.save_data.name
        self.lbl_player_name.set_text("Player: {}".format(name))
        self.lbl_level_name.set_text("LEVEL {:02d}".format(self.level_data["level"] + 1))

        self.level_state = current_app.save_data.get_level_data(self.level_data["level"])
        return self.clear()


    def render(self):
        # menu_rect = SCREEN_RECT.copy()

        self.lbl_player_name = gui.GUILabel("Player:", self.font_s, (255,255,255), shadow_color=(80,80,80))
        self.lbl_player_name.ljust_in_rect(SCREEN_RECT, 40)
        self.lbl_player_name.tjust_in_rect(SCREEN_RECT, 22)
        self.em.add(self.lbl_player_name)

        dark_panel = Entity()
        size = Vector2(420, 400)
        dark_panel.frames = [pygame.Surface(size, pygame.SRCALPHA), ]
        # dark_panel.frames[0].fill((0,0,0,50))
        pygame.draw.rect(dark_panel.surface, (0,0,0,50), dark_panel.get_rect(), 0, 5)
        dark_panel.pos = SCREEN_RECT.center - (size / 2)
        self.em.add(dark_panel)

        lbl = gui.GUILabel("SUMMARY", self.font_m, (255,255,255), shadow_color=(80,80,80))
        lbl.center_in_rect(SCREEN_RECT)
        lbl.y -= 160
        self.em.add(lbl)

        self.lbl_level_name = gui.GUILabel("LEVEL xx", self.font_s, (255,255,255))
        self.lbl_level_name.center_in_rect(SCREEN_RECT)
        self.lbl_level_name.y -= 125
        self.em.add(self.lbl_level_name)

        y_spacing, y_step = 250, 45

        y = y_spacing + y_step * 0
        lbl = gui.GUILabel("COINS COLLECTED", self.font_s, (255,255,255))
        lbl.x, lbl.y = 512-200+20, y
        self.em.add(lbl)
        self.lbl_coins_result = gui.GUILabel("100%", self.font_xs, GOLD)
        self.lbl_coins_result.y = y + 6
        self.lbl_coins_result.rjust_in_rect(SCREEN_RECT, 355)
        self.em.add(self.lbl_coins_result)
        self.medal_coin = HUDMedalCoin(Vector2(512+200-40, y))
        self.em.add(self.medal_coin)

        y = y_spacing + y_step * 1
        lbl = gui.GUILabel("NO DAMAGE", self.font_s, (255,255,255))
        lbl.x, lbl.y = 512-200+20, y
        self.em.add(lbl)
        self.medal_heart = HUDMedalHeart(Vector2(512+200-40, y_spacing + (y_step * 1)))
        self.em.add(self.medal_heart)
        self.em.add(ScoreDividerBar(Vector2(512,y_spacing + (y_step * 1) - 7)))

        y = y_spacing + y_step * 2
        lbl = gui.GUILabel("70% ENEMIES DESTROYED", self.font_s, (255,255,255))
        lbl.x, lbl.y = 512-200+20, y
        self.em.add(lbl)
        self.lbl_70_result = gui.GUILabel("70%", self.font_xs, GREY)
        self.lbl_70_result.y = y + 6
        self.lbl_70_result.rjust_in_rect(SCREEN_RECT, 355)
        self.em.add(self.lbl_70_result)
        self.medal_70 = HUDMedal70(Vector2(512+200-40, y_spacing + (y_step * 2)))
        self.em.add(self.medal_70)
        self.em.add(ScoreDividerBar(Vector2(512,y_spacing + (y_step * 2) - 7)))

        y = y_spacing + y_step * 3
        lbl = gui.GUILabel("100% ENEMIES DESTROYED", self.font_s, (255,255,255))
        lbl.x, lbl.y = 512-200+20, y
        self.em.add(lbl)
        self.lbl_100_result = gui.GUILabel("90%", self.font_xs, GREY)
        self.lbl_100_result.y = y + 6
        self.lbl_100_result.rjust_in_rect(SCREEN_RECT, 355)
        self.em.add(self.lbl_100_result)
        self.medal_100 = HUDMedal100(Vector2(512+200-40, y_spacing + (y_step * 3)))
        self.em.add(self.medal_100)
        self.em.add(ScoreDividerBar(Vector2(512,y_spacing + (y_step * 3) - 7)))


        lbl_press_enter = gui.GUILabel("Enter: Done", self.font_s, (255,255,255), shadow_color=(80,80,80))
        lbl_press_enter.rjust_in_rect(SCREEN_RECT, 40)
        lbl_press_enter.tjust_in_rect(SCREEN_RECT, 550)
        self.em.add(lbl_press_enter)

    def set_data(self, data):
        self.level_data = data 
        self.update()
        # print("datax", data)

    def on_event(self, event, elapsed):
        
        if not self.transitioning:
        
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                current_scene.start_transition(screen_name="level_select", direction="left", data={"level": self.level_data["level"]})
                current_app.mixer.play("menu click")
