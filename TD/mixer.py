from enum import Enum 

import pygame
from blinker import signal

from TD.assetmanager import asset_manager
from TD import config 
from TD.savedata import save_data

class MixerChannels(Enum):
    PLAYERFIRE = 0
    COINPICKUP = 1
    HEARTPICKUP = 2

class Mixer:
    pass 
    def __init__(self):
        self.muted = save_data.muted
       
        pygame.mixer.set_num_channels(16)
        pygame.mixer.set_reserved(3)

        self.channels = {
            MixerChannels.PLAYERFIRE: pygame.mixer.Channel(MixerChannels.PLAYERFIRE.value),
            MixerChannels.COINPICKUP: pygame.mixer.Channel(MixerChannels.COINPICKUP.value),
            MixerChannels.HEARTPICKUP: pygame.mixer.Channel(MixerChannels.COINPICKUP.value),
        }
        signal("mixer.play").connect(self.on_play)
        signal("mixer.mute").connect(self.on_mute)
        signal("mixer.is_muted").connect(self.on_is_muted)

    def on_is_muted(self, sender):
        return self.muted

    def on_mute(self, value):
        self.muted = value
        signal("savedata.save").send()

    def on_play(self, name):
        if self.muted:
            return

        if name == "coin pickup":
            self.channels[MixerChannels.COINPICKUP].play(asset_manager.sounds[name])
        elif name == "heart pickup":
            self.channels[MixerChannels.HEARTPICKUP].play(asset_manager.sounds[name])
        elif name == "player gun":
            self.channels[MixerChannels.PLAYERFIRE].play(asset_manager.sounds[name])
        else:
            asset_manager.sounds[name].play()
