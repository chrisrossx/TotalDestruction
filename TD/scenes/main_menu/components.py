from TD.assetmanager import asset_manager
from blinker import signal 
from TD import gui 


class StartButtonGroup(gui.GuiButtonGroup):
    def select(self, name, muted=False):
        super().select(name)
        if not muted:
            signal("mixer.play").send("menu move")

class StartButton(gui.GuiButton):
    def __init__(self, name, size, lbl, lbl_offset=None, lbl_position=None, top=None, bottom=None, left=None, right=None, left_cursor=None, right_cursor=None):
        super().__init__(name, size, lbl, lbl_offset, lbl_position, top, bottom, left, right)
        self.left_cursor = left_cursor
        self.right_cursor = right_cursor

    def on_selected(self):
        self.left_cursor.y = self.pos.y + 14
        self.right_cursor.y = self.pos.y + 14
    

class MuteButton(StartButton):
    def __init__(self, name, size, lbl, lbl_offset=None, lbl_position=None, top=None, bottom=None, left=None, right=None, left_cursor=None, right_cursor=None):
        super().__init__(name, size, lbl, lbl_offset, lbl_position, top, bottom, left, right, left_cursor, right_cursor)
        signal("mixer.mute").connect(self.on_mute)
    
    def render(self, value=None):
        value = signal("mixer.is_muted").send()[0][1] if value == None else value
        if value:
            self.lbl = gui.GUILabel("Unmute", asset_manager.fonts["sm"], (255,255,255), shadow_color=(80,80,80))
        else:
            self.lbl = gui.GUILabel("Mute", asset_manager.fonts["sm"], (255,255,255), shadow_color=(80,80,80))
        return super().render()

    def on_mute(self, value):
        self.render(value)
