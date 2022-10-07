from enum import Enum 

from TD.entity import Entity, EntityPathFollower, EntityType, EntityVectorMovement
from TD.assetmanager import asset_manager

from pygame import Vector2, Rect
from TD.globals import current_app


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
            return ("I will defeat you!", None)
        if self.dialog == Dialog.PAIN:
            return ("Ouch!", None)
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
            return ("You can't get me!", None)
        if self.dialog == Dialog.PAIN:
            return ("Ouch!", None)
        if self.dialog == Dialog.DYING:
            return ("How could you!", "ahhhhhhh!")

    def play_sound(self):
        if self.dialog == Dialog.TAUNT_1:
            current_app.mixer.play("elle taunt_1")
        if self.dialog == Dialog.THREAT:
            current_app.mixer.play("elle threat")
        if self.dialog == Dialog.PAIN:
            current_app.mixer.play("elle pain")
        if self.dialog == Dialog.DYING:
            current_app.mixer.play("elle dying")


class MaiAnh(Entity):
    def __init__(self, dialog):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Mai-Anh"]
        self.sprite_offset = Vector2(-33, -33)

        self.dialog = dialog

    def get_text(self):
        if self.dialog == Dialog.TAUNT_1:
            return ("You have not been Calm!", "You will regret this!")
        if self.dialog == Dialog.THREAT:
            return ("You!!!!", "Leave My Room")
        if self.dialog == Dialog.PAIN:
            return ("Ouchhhhhh!", None)
        if self.dialog == Dialog.DYING:
            return ("I am going to bed", "Leave me alone!")

    def play_sound(self):
        if self.dialog == Dialog.TAUNT_1:
            current_app.mixer.play("elle taunt_1")
        if self.dialog == Dialog.THREAT:
            current_app.mixer.play("elle threat")
        if self.dialog == Dialog.PAIN:
            current_app.mixer.play("elle pain")
        if self.dialog == Dialog.DYING:
            current_app.mixer.play("elle dying")



class Christopher(Entity):
    def __init__(self, dialog):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = asset_manager.sprites["Christopher"]
        self.sprite_offset = Vector2(-33, -33)

        self.dialog = dialog


    def get_text(self):
        if self.dialog == Dialog.TAUNT_1:
            return ("Get out of Here!", None)
        if self.dialog == Dialog.THREAT:
            return ("Grrrrr Get out!", None)
        if self.dialog == Dialog.PAIN:
            return ("Ouch!", None)
        if self.dialog == Dialog.DYING:
              return ("How could you do this", "to me. You Win!")

    def play_sound(self):
        if self.dialog == Dialog.TAUNT_1:
            current_app.mixer.play("christopher taunt_1")
        if self.dialog == Dialog.THREAT:
            current_app.mixer.play("christopher threat")
        if self.dialog == Dialog.PAIN:
            current_app.mixer.play("christopher pain")
        if self.dialog == Dialog.DYING:
            current_app.mixer.play("christopher dying")



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
