from enum import Enum 

import pygame


class MixerChannels(Enum):
    PLAYERFIRE = 0
    COINPICKUP = 1

class Channels:
    def __init__(self):
        self.channels = {}

    def load(self):
        # pygame.mixer.set_num_channels(16)
        pygame.mixer.set_reserved(4)
        # print(pygame.mixer.get_num_channels())

        self.channels[MixerChannels.PLAYERFIRE] = pygame.mixer.Channel(MixerChannels.PLAYERFIRE.value)
        self.channels[MixerChannels.COINPICKUP] = pygame.mixer.Channel(MixerChannels.COINPICKUP.value)

        # pygame.mixer.

    def __getitem__(self, key):
        return self.channels[key]

channels = Channels()

