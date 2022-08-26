import pygame
from TD.config import SCREEN_RECT

from TD.assetmanager import asset_manager
from TD import gui 
from pygame import Vector2
from TD.globals import current_app
from TD.scenes.levels.hud import HUD, HUDMedal100, HUDMedal70, HUDMedalHeart
from TD.entity import Entity, EntityType


class StartButtonGroup(gui.GuiButtonGroup):
    pass


class StartButton(gui.GuiButton):
    def __init__(self, name, size, lbl, lbl_offset=None, lbl_position=None, top=None, bottom=None, left=None, right=None, left_cursor=None, right_cursor=None):
        super().__init__(name, size, lbl, lbl_offset, lbl_position, top, bottom, left, right)
        self.left_cursor = left_cursor
        self.right_cursor = right_cursor

    def on_selected(self):
        self.left_cursor.y = self.pos.y + 14
        self.right_cursor.y = self.pos.y + 14
    

class MusicButton(StartButton):
    def __init__(self, name, size, lbl, lbl_offset=None, lbl_position=None, top=None, bottom=None, left=None, right=None, left_cursor=None, right_cursor=None):
        super().__init__(name, size, lbl, lbl_offset, lbl_position, top, bottom, left, right, left_cursor, right_cursor)
    
    def render(self, value=None):
        value = current_app.mixer.is_music_muted()
        if value:
            self.lbl = gui.GUILabel("Music", asset_manager.fonts["sm"], (155,155,155), shadow_color=(80,80,80), shadow_step=Vector2(2,2))
        else:
            self.lbl = gui.GUILabel("Music", asset_manager.fonts["sm"], (255,255,255), shadow_color=(80,80,80))
        return super().render()

    def on_mute(self, value):
        self.render(value)

    

class SoundsButton(StartButton):
    def __init__(self, name, size, lbl, lbl_offset=None, lbl_position=None, top=None, bottom=None, left=None, right=None, left_cursor=None, right_cursor=None):
        super().__init__(name, size, lbl, lbl_offset, lbl_position, top, bottom, left, right, left_cursor, right_cursor)
    
    def render(self, value=None):
        value = current_app.mixer.is_sounds_muted()
        if value:
            self.lbl = gui.GUILabel("Sounds", asset_manager.fonts["sm"], (155,155,155), shadow_color=(80,80,80), shadow_step=Vector2(2,2))
        else:
            self.lbl = gui.GUILabel("Sounds", asset_manager.fonts["sm"], (255,255,255), shadow_color=(80,80,80))
        return super().render()

    def on_mute(self, value):
        self.render(value)


class LevelSelectLines(gui.GUIEntity):
    def __init__(self):
        super().__init__()
        self.frames = asset_manager.sprites["Menu Level Select Lines"]
        self.center_sprite_offset()


class LevelBadgeCursor(gui.GUIEntity):
    def __init__(self):
        super().__init__()
        self.frames = asset_manager.sprites["Menu Level Select Cursor"]
        for i, a in enumerate([60,60,60,60,45,30,15,0]):
            a = a / 100
            a *= 255
            self.frames[i].set_alpha(a)
        self.frames.append(self.frames[7])
        self.frames.append(self.frames[7])

        self.center_sprite_offset()
        self.sprite_offset.x -= 3
        self.sprite_offset.y -= 3
        self.frame_duration = 1000 / 8


class LevelBadge(gui.GUIEntity):
    def __init__(self, level_index):
        super().__init__()
        self.level_index = level_index
        self.frames = asset_manager.sprites["Menu Level Select Badges"]
        self.center_sprite_offset()
        self.frame_index = (self.level_index * 3) + 1
        p = Vector2(-23, 8)
        self.medal_70 = HUDMedal70(p + Vector2(-27, 0))
        self.medal_100 = HUDMedal100(p + Vector2(0, 0))
        self.medal_heart = HUDMedalHeart(p + Vector2(28, 0))
        self.disabled()

    def update(self):
        level_data = current_app.save_data.get_level_data(self.level_index)
        if level_data["enemies"] >= 0.7:
            self.medal_70.gold()
        else:
            self.medal_70.valid()

        if level_data["enemies"] >= 1.0:
            self.medal_100.gold()
        else:
            self.medal_100.valid()

        if level_data["medalHeart"]:
            self.medal_heart.gold()
        else:
            self.medal_heart.valid()

        if level_data["finished"]:
            self.finished()
        else:
            self.not_finished()


    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        # self.h.draw(surface, elapsed)
        surface.blit(self.medal_heart.surface, self.pos + self.medal_heart.pos)
        surface.blit(self.medal_100.surface, self.pos + self.medal_100.pos)
        surface.blit(self.medal_70.surface, self.pos + self.medal_70.pos)
        # print(self.h.pos)
    
    def disabled(self):
        self.frame_index = (self.level_index * 3) + 0

    def not_finished(self):
        self.frame_index = (self.level_index * 3) + 1

    def finished(self):
        self.frame_index = (self.level_index * 3) + 2



class HUDMedalCoin(HUDMedalHeart):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = [asset_manager.sprites["HUD"][i+7] for i in range(3)]


class ScoreDividerBar(Entity):
    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.GUI
        self.pos = pos.copy()
        self.frames = [pygame.Surface(Vector2(370,2), pygame.SRCALPHA)]
        self.surface.fill((0,0,0,50))
        self.center_sprite_offset()

class ScoreGoldConfetti(Entity):
    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Menu Level Score Confetti"]
        self.frame_duration = 1000/22
        self.frame_loop_end = 1
        self.center_sprite_offset()
        self.pos = pos.copy()

class ScoreGoldConfetti2(ScoreGoldConfetti):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = asset_manager.sprites["Menu Level Score Confetti 2"]
        self.frame_duration = 1000/29
        self.center_sprite_offset()

class ScoreGreyConfetti(ScoreGoldConfetti):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = asset_manager.sprites["Menu Level Score Confetti Grey"]

class ScoreGreyConfetti2(ScoreGoldConfetti2):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = asset_manager.sprites["Menu Level Score Confetti Grey 2"]