from pathlib import Path

import pygame


class AssetManager:
    
    def __init__(self):

        self.sprites = {}

    def load(self):

        source = pygame.image.load(Path("TD/assets/TD T-8.png"))
        source.convert()
        self.sprites["T8 001"] = source.subsurface((0,0,64,64))
        self.sprites["T8 002"] = source.subsurface((64,0,64,64))
        self.sprites["T8 003"] = source.subsurface((128,0,64,64))
        self.sprites["T8 004"] = source.subsurface((192,0,64,64))
     
        sky = pygame.image.load(Path("TD/assets/layered.jpg"))
        sky.convert()
        self.sprites["sky layered"] = sky


# Singleton Pattern - Stinky, but practical for a game environment
asset_manager = AssetManager()
