from pygame import Vector2

from TD.entity import EntityType, EntityControl
from TD.assetmanager import asset_manager
from TD.config import SCREEN_RECT
from TD.characters import MaiAnh, Christopher, Sawyer, Elle
from TD.gui import GUILabel
from TD import current_app


class Music(EntityControl):
    def __init__(self, music_key):
        super().__init__()
        self.music_key = music_key

    def tick(self, elapsed):
        current_app.mixer.play_music(self.music_key)
        self.delete()
