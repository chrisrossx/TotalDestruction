from TD.assetmanager import asset_manager
from TD import gui 
from pygame import Vector2
from TD.globals import current_app

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

