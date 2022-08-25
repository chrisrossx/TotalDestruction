from TD.entity import Entity, EntityPathFollower, EntityType, EntityVectorMovement
from TD.assetmanager import asset_manager

from pygame import Vector2, Rect


class Sawyer(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Sawyer"]
        self.sprite_offset = Vector2(-33, -33)
        self.add_hitbox(Rect(0,0,40,40), Vector2(-20, -20))
        # self.add_hitbox(Rect(0,0,10,10), Vector2(-5, -85))
        # self.add_hitbox(Rect(0,0,10,10), Vector2(-5, -95))


class Elle(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Elle"]
        self.sprite_offset = Vector2(-33, -33)
        self.add_hitbox(Rect(0,0,40,40), Vector2(-20, -20))
