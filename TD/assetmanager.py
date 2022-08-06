from pathlib import Path

import pygame


def load_sprite_from_files(base_filename, steps):
    sprites = []
    for i, step in enumerate(steps):
        filename = base_filename.parent / Path(base_filename.stem + step + base_filename.suffix)
        sprite = pygame.image.load(filename)
        sprite.convert
        sprites.append(sprite)
    return sprites


def load_sprites_from_sheet(source, rects):
    sprites = []
    for rect in rects:
        sprite = source.subsurface(rect)
        sprites.append(sprite)
    return sprites


def scale_sprites(source, size):
        sprites = []
        for sprite in source:
            new_sprite = pygame.transform.scale(sprite, size)
            sprites.append(new_sprite)
        return sprites


class AssetManager:
    
    def __init__(self):

        self.sprites = {}

    def load(self):

        self.sprites["sky layered"] = pygame.image.load(Path("TD/assets/layered.jpg"))
        self.sprites["sky layered"].convert()

        source = pygame.image.load(Path("TD/assets/TD T-8.png"))
        source.convert()
        self.sprites["T8"] = load_sprites_from_sheet(source, [
            (0,0,64,64),
            (64,0,64,64),
            (128,0,64,64),
            (192,0,64,64),
        ])
        # self.sprites["T8"] = scale_sprites(self.sprites["T8"], (128, 128))
     
        source = pygame.image.load(Path("TD/assets/TD CX-5 2.png"))
        source.convert()
        self.sprites["CX5"] = load_sprites_from_sheet(source, [
            (0,0,64,64),
            (64,0,64,64),
            (128,0,64,64),
            (192,0,64,64),
        ])

        self.sprites["D2"] = load_sprite_from_files(Path("TD/assets/TD D-2 .png"), ["001", "002", "003", "004"])
        self.sprites["powerup heart"] = load_sprite_from_files(Path("TD/assets/TD_Powerups_002.png"), ["-1", "-2", "-3", "-4", "-5", "-6", "-7"])
        self.sprites["powerup heart"] = scale_sprites(self.sprites["powerup heart"], (64, 64))

        source = pygame.image.load(Path("TD/assets/TD Powerups 001.png"))

        source = pygame.image.load(Path("TD/assets/TD Explosion M 001.png"))
        self.sprites["Explosion Medium"] = load_sprites_from_sheet(source, [
            (0,0,64,64),
            (64,0,64,64),
            (128,0,64,64),
            (192,0,64,64),
            (192+64,0,64,64),
            (192+128,0,64,64),
        ])
        self.sprites["Explosion Medium"] = scale_sprites(self.sprites["Explosion Medium"], (128,128))

        self.sprites["Explosion Medium 002"] = load_sprite_from_files(Path("TD/assets/explosion medium/TD_Explosion_Medium.png"), ["-{}".format(i+1) for i in range(13)])



# Singleton Pattern - Stinky, but practical for a game environment
asset_manager = AssetManager()
