from enum import Enum

import pygame

from TD.assetmanager import asset_manager
from TD import config
from TD.globals import current_app


class MixerChannels(Enum):
    PLAYERFIRE = 0
    COINPICKUP = 1
    HEARTPICKUP = 2
    VOICE = 3


class Mixer:
    pass

    def __init__(self):
        self.sounds_muted = current_app.save_data.sounds_muted
        self.music_muted = current_app.save_data.music_muted
        self.music_playing = False

        pygame.mixer.set_num_channels(16)
        pygame.mixer.set_reserved(4)

        self.channels = {
            MixerChannels.PLAYERFIRE: pygame.mixer.Channel(
                MixerChannels.PLAYERFIRE.value
            ),
            MixerChannels.COINPICKUP: pygame.mixer.Channel(
                MixerChannels.COINPICKUP.value
            ),
            MixerChannels.HEARTPICKUP: pygame.mixer.Channel(
                MixerChannels.HEARTPICKUP.value
            ),
            MixerChannels.VOICE: pygame.mixer.Channel(MixerChannels.VOICE.value),
        }

    def play_music(self, file):
        pygame.mixer.music.load(asset_manager.music[file]["filename"])
        pygame.mixer.music.set_volume(asset_manager.music[file]["volume"])
        self.music_playing = True
        if not self.music_muted:
            pygame.mixer.music.play(loops=-1)

    def stop_music(self):
        self.music_playing = False
        pygame.mixer.music.stop()

    def is_sounds_muted(self):
        return self.sounds_muted

    def is_music_muted(self):
        return self.music_muted

    def mute_sounds(self, value):
        self.sounds_muted = value
        current_app.save_data.save()

    def mute_music(self, value):
        # self.sounds_muted = value
        self.music_muted = value
        if self.music_playing:
            if self.music_muted:
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.play(loops=-1)

        current_app.save_data.save()

    def play(self, name):
        if self.sounds_muted:
            return

        if name == "coin pickup":
            self.channels[MixerChannels.COINPICKUP].play(asset_manager.sounds[name])
        elif name == "heart pickup":
            self.channels[MixerChannels.HEARTPICKUP].play(asset_manager.sounds[name])
        elif name == "player gun":
            self.channels[MixerChannels.PLAYERFIRE].play(asset_manager.sounds[name])
        elif name in ["weapons upgrade", "chain lost"]:
            if not self.channels[MixerChannels.VOICE].get_busy():
                self.channels[MixerChannels.VOICE].play(asset_manager.sounds[name])
        else:
            asset_manager.sounds[name].play()
