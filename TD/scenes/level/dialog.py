from pygame import Vector2

from TD.entity import EntityType, Entity
from TD.assetmanager import asset_manager
from TD.config import SCREEN_RECT
from TD.characters import MaiAnh, Christopher, Sawyer, Elle
from TD.gui import GUILabel
from TD.globals import current_app


class EnemyDialog(Entity):
    slide_duraiton = 500
    fade_duration = 300
    def __init__(self, character, t1="", t2="", color_line_1=(255,255,255), color_line_2=(255,255,255)):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["enemy speech bubble"]
        self.frame_index = 7
        # self.frame_duration = 75
        self.center_sprite_offset()
        self.sprite_offset.x = -self.surface.get_rect().w
        self.pos = Vector2(SCREEN_RECT.w, SCREEN_RECT.h - 100)
        self.step = 0 
        self.step_elapsed = 0
        self.slidein_frame_elapsed = 0
        self.slideout_frame_elapsed = 0
        self.character = character
           
        self.character_offset = Vector2(-50,0)

        t1, t2 = self.character.get_text()
        if t1 and t2:
            line_1_pos = self.pos + Vector2(-300, -24)
            line_2_pos = self.pos + Vector2(-300, -2)
        else:
            line_1_pos = self.pos + Vector2(-300, -13)
            line_2_pos = self.pos + Vector2(-300, -13)

        if t1:
            self.line_1 = GUILabel(t1, asset_manager.fonts["sm"], color_line_1, line_1_pos)
            self.line_1.surface.set_alpha(0)
        else:
            self.line_1 = None
        if t2:
            self.line_2 = GUILabel(t2, asset_manager.fonts["sm"], color_line_2, line_2_pos)
            self.line_2.surface.set_alpha(0)
        else:
            self.line_2 = None

        

    def tick_slidein(self, elapsed):
        slidein_duration = self.slide_duraiton
        slidein_frame_duration = slidein_duration / 8

        self.slidein_frame_elapsed += elapsed
        if self.step_elapsed >= slidein_duration:
            self.next_step()
            delta_x = 0
        else:
            delta_x = 366 - (366 * (self.step_elapsed / slidein_duration))
        self.pos.x = SCREEN_RECT.w + delta_x

        if self.slidein_frame_elapsed >= slidein_frame_duration and self.frame_index > 0:
            self.slidein_frame_elapsed = 0
            self.frame_index -= 1

    def tick_slideout(self, elapsed):
        slideout_duration = self.slide_duraiton
        slideout_frame_duration = slideout_duration / 8

        self.slideout_frame_elapsed += elapsed
        if self.step_elapsed >= slideout_duration:
            self.delete()
            delta_x = 366
        else:
            delta_x = (366 * (self.step_elapsed / slideout_duration))
        self.pos.x = SCREEN_RECT.w + delta_x
        # print(self.frame_index)
        if self.slideout_frame_elapsed >= slideout_frame_duration and self.frame_index < 7:
            self.slideout_frame_elapsed = 0
            self.frame_index += 1

    def tick_fadein(self, elapsed):
        fadein_duration = self.fade_duration
        d = self.step_elapsed / fadein_duration
        if d >= 1.0:
            d = 1.0
            self.character.play_sound()
            self.next_step()
        if self.line_1:
            self.line_1.surface.set_alpha(d * 255)
        if self.line_2:
            self.line_2.surface.set_alpha(d * 255)

    def tick_fadeout(self, elapsed):
        fadeout_duration = self.fade_duration
        d = 1.0 - (self.step_elapsed / fadeout_duration)
        if d <= 0.0:
            d = 0.0
            self.next_step()
        if self.line_1:
            self.line_1.surface.set_alpha(d * 255)
        if self.line_2:
            self.line_2.surface.set_alpha(d * 255)

    def next_step(self):
        self.step += 1
        self.step_elapsed = 0

    def tick(self, elapsed):
        super().tick(elapsed)
        self.step_elapsed += elapsed
        

        step_2_duration = 1200


        if self.step == 0:
            self.tick_slidein(elapsed)
            self.line_1.enabled = True 
        
        if self.step == 1:
            self.tick_fadein(elapsed)

        if self.step == 2:
            if self.step_elapsed >= step_2_duration:
                self.next_step()

        if self.step == 3:
            self.tick_fadeout(elapsed)

        if self.step == 4:
            self.tick_slideout(elapsed)
            # self.line_1.enabled = False 

        self.character.tick(elapsed)
        self.character.pos = self.pos.copy() + self.character_offset

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        self.character.draw(elapsed, surface)
        if self.line_1:
            self.line_1.draw(elapsed, surface)
        if self.line_2:
            self.line_2.draw(elapsed, surface)
            

