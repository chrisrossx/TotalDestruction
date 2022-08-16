from blinker import signal 
from pygame import Vector2

from TD.entity import Entity, EntityType
from TD.assetmanager import asset_manager


class HUD(Entity):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos.copy()
        self.type = EntityType.GUI

class HUDLife(HUD):
    def __init__(self, pos, life_index):
        super().__init__(pos)
        self.frames = [asset_manager.sprites["HUD"][i+2] for i in range(2)]
        self.life_index = life_index
        signal("scene.hud.lives").connect(self.on_lives)

    def on_lives(self, lives):
        if lives >= self.life_index:
            self.frame_index = 0
        else:
            self.frame_index = 1

class Medal(HUD):
    def on_valid(self, valid):
        if valid:
            self.valid()
        else:
            self.invalid()


    def gold(self):
        self.frame_index = 2

    def valid(self):
        self.frame_index = 0
    
    def invalid(self):
        self.frame_index = 1  

class HUDMedal100(Medal):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = [asset_manager.sprites["HUD"][i+13] for i in range(3)]
        signal("scene.hud.medal.100").connect(self.on_valid)
       

class HUDMedal70(Medal):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = [asset_manager.sprites["HUD"][i+10] for i in range(3)]
        signal("scene.hud.medal.70").connect(self.on_valid)


class HUDMedalHeart(Medal):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = [asset_manager.sprites["HUD"][i+4] for i in range(3)]
        signal("scene.hud.medal.heart").connect(self.on_valid)
        