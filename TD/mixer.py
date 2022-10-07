from enum import Enum

import pygame

from TD.assetmanager import asset_manager
from TD import config
from TD.globals import current_app
from TD.mixer_channels import MixerChannels


class Mixer:
    pass

    def __init__(self):
        self.sounds_muted = current_app.save_data.sounds_muted
        self.music_muted = current_app.save_data.music_muted
        self.music_playing = False

        pygame.mixer.set_num_channels(32)
        pygame.mixer.set_reserved(9)
        # print(pygame.mixer.get_num_channels())

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
            MixerChannels.VOICE: pygame.mixer.Channel(
                MixerChannels.VOICE.value
            ),
            MixerChannels.ENEMYFIRE_1: pygame.mixer.Channel(
                MixerChannels.ENEMYFIRE_1.value
            ),
            MixerChannels.ENEMYFIRE_2: pygame.mixer.Channel(
                MixerChannels.ENEMYFIRE_2.value
            ),
            MixerChannels.ENEMYFIRE_3: pygame.mixer.Channel(
                MixerChannels.ENEMYFIRE_3.value
            ),
            MixerChannels.ENEMYFIRE_4: pygame.mixer.Channel(
                MixerChannels.ENEMYFIRE_4.value
            ),
            MixerChannels.EXPLOSION: pygame.mixer.Channel(
                MixerChannels.EXPLOSION.value
            ),
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

        sound = asset_manager.sounds[name]

        if sound.mixer_channel == MixerChannels.COINPICKUP:
            self.channels[MixerChannels.COINPICKUP].play(sound)
        elif sound.mixer_channel == MixerChannels.HEARTPICKUP:
            self.channels[MixerChannels.HEARTPICKUP].play(sound)
        elif sound.mixer_channel == MixerChannels.PLAYERFIRE:
            self.channels[MixerChannels.PLAYERFIRE].play(sound)
        elif sound.mixer_channel == MixerChannels.VOICE:
            # if not self.channels[MixerChannels.VOICE].get_busy():
            self.channels[MixerChannels.VOICE].play(sound)
        elif sound.mixer_channel == MixerChannels.ENEMYFIRE_1:
            self.channels[MixerChannels.ENEMYFIRE_1].play(sound)
        elif sound.mixer_channel == MixerChannels.ENEMYFIRE_2:
            self.channels[MixerChannels.ENEMYFIRE_2].play(sound)
        elif sound.mixer_channel == MixerChannels.ENEMYFIRE_3:
            self.channels[MixerChannels.ENEMYFIRE_3].play(sound)
        elif sound.mixer_channel == MixerChannels.ENEMYFIRE_4:
            self.channels[MixerChannels.ENEMYFIRE_4].play(sound)
        elif sound.mixer_channel == MixerChannels.EXPLOSION:
            self.channels[MixerChannels.EXPLOSION].play(sound)
        else:
            sound.play()
