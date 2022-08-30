from enum import Enum 

from TD.entity import Entity, EntityPathFollower, EntityType, EntityVectorMovement
from TD.assetmanager import asset_manager

from pygame import Vector2, Rect


class Dialog(Enum):
    TAUNT_1 = 0
    THREAT = 1
    PAIN = 2
    DYING = 3


class Sawyer(Entity):
    def __init__(self, dialog):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Sawyer"]
        self.sprite_offset = Vector2(-33, -33)

        self.dialog = dialog 

    def get_text(self):
        if self.dialog == Dialog.TAUNT_1:
            return ("You will be no challenge to me!", "hahaha")
        if self.dialog == Dialog.THREAT:
            return ("I will defeat you!",)
        if self.dialog == Dialog.PAIN:
            return ("Ouch!", )
        if self.dialog == Dialog.DYING:
            return ("I was supposed to win!", "meow!")

    def play_sound(self):
        if self.dialog == Dialog.TAUNT_1:
            pass
        if self.dialog == Dialog.THREAT:
            pass
        if self.dialog == Dialog.PAIN:
            pass
        if self.dialog == Dialog.DYING:
            pass

class Elle(Entity):
    def __init__(self, dialog):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Elle"]
        self.sprite_offset = Vector2(-33, -33)

        self.dialog = dialog

    def get_text(self):
        if self.dialog == Dialog.TAUNT_1:
            return ("I will defeat you", "hahaha")
        if self.dialog == Dialog.THREAT:
            return ("You can't get me!",)
        if self.dialog == Dialog.PAIN:
            return ("Ouch!", )
        if self.dialog == Dialog.DYING:
            return ("How could you!", "ahhhhhhh!")

    def play_sound(self):
        if self.dialog == Dialog.TAUNT_1:
            pass
        if self.dialog == Dialog.THREAT:
            pass
        if self.dialog == Dialog.PAIN:
            pass
        if self.dialog == Dialog.DYING:
            pass


class MaiAnh(Entity):
    def __init__(self):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Mai-Anh"]
        self.sprite_offset = Vector2(-33, -33)


class Christopher(Entity):
    def __init__(self):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Christopher"]
        self.sprite_offset = Vector2(-33, -33)


class SawyerPathFollower(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Sawyer"]
        self.sprite_offset = Vector2(-33, -33)
        self.add_hitbox(Rect(0, 0, 40, 40), Vector2(-20, -20))


class MaiAnhPathFollower(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Mai-Anh"]
        self.sprite_offset = Vector2(-33, -33)
        self.add_hitbox(Rect(0, 0, 40, 40), Vector2(-20, -20))


class EllePathFollower(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Elle"]
        self.sprite_offset = Vector2(-33, -33)
        self.add_hitbox(Rect(0, 0, 40, 40), Vector2(-20, -20))


class ChristopherPathFollower(EntityPathFollower):
    def __init__(self, path_index):
        super().__init__(path_index)
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Christopher"]
        self.sprite_offset = Vector2(-33, -33)
        self.add_hitbox(Rect(0, 0, 40, 40), Vector2(-20, -20))
