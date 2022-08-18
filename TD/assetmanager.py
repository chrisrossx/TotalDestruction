from pathlib import Path

import pygame

def load_sprite_from_file(filename):
    sprite = pygame.image.load(filename)
    sprite = sprite.convert_alpha()
    return [sprite, ]


def load_sprite_from_files(base_filename, steps):
    sprites = []
    for i, step in enumerate(steps):
        filename = base_filename.parent / Path(base_filename.stem + step + base_filename.suffix)
        sprite = pygame.image.load(filename)
        sprite = sprite.convert_alpha()
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


def rotate_sprites(source, angle):
        sprites = []
        for sprite in source:
            new_sprite = pygame.transform.rotate(sprite, angle)
            sprites.append(new_sprite)
        return sprites

def flip_sprites(source, flip_x=False, flip_y=False):
        sprites = []
        for sprite in source:
            new_sprite = pygame.transform.flip(sprite, flip_x, flip_y)
            sprites.append(new_sprite)
        return sprites


def create_rotations(store, source, angles):
    for angle in angles:
        store[angle] = rotate_sprites(source, angle)


class AssetManager:
    
    def __init__(self):

        self.sprites = {}
        self.fonts = {}

        self.sounds = {}

    def load(self):

        self.fonts["sm"] = pygame.font.Font(Path("TD/assets/BebasNeue-Regular.ttf"), 24)
        self.fonts["md"] = pygame.font.Font(Path("TD/assets/BebasNeue-Regular.ttf"), 48)
        self.fonts["lg"] = pygame.font.Font(Path("TD/assets/BebasNeue-Regular.ttf"), 96)


        self.sounds["coin pickup"] = pygame.mixer.Sound(str(Path("TD/assets/CoinBrass.wav")))
        self.sounds["heart pickup"] = pygame.mixer.Sound(str(Path("TD/assets/CoinThree.wav")))
        self.sounds["explosion md"] = pygame.mixer.Sound(str(Path("TD/assets/ExploFuel.wav")))
        self.sounds["explosion player"] = pygame.mixer.Sound(str(Path("TD/assets/ExploBreakage2.wav")))
        self.sounds["player hit"] = pygame.mixer.Sound(str(Path("TD/assets/ExploMetalbits.wav")))
        self.sounds["player collision"] = pygame.mixer.Sound(str(Path("TD/assets/HitMetalBasher.wav")))
        self.sounds["player gun"] = pygame.mixer.Sound(str(Path("TD/assets/GunUp.wav")))
        self.sounds["player gun"].set_volume(0.3)

        self.sounds["menu move"] = pygame.mixer.Sound(str(Path("TD/assets/CatchClose.wav")))
        self.sounds["menu click"] = pygame.mixer.Sound(str(Path("TD/assets/CatchOpen.wav")))
        self.sounds["menu type"] = pygame.mixer.Sound(str(Path("TD/assets/HitMetalBash.wav")))
        



        self.sprites["sky layered"] = pygame.image.load(str(Path("TD/assets/layered.jpg")))
        self.sprites["sky layered"] = self.sprites["sky layered"].convert()

        source = pygame.image.load(Path("TD/assets/TD T-8.png"))
        source = source.convert_alpha()
        self.sprites["T8"] = load_sprites_from_sheet(source, [
            (0,0,64,64),
            (64,0,64,64),
            (128,0,64,64),
            (192,0,64,64),
        ])
        # self.sprites["T8"] = scale_sprites(self.sprites["T8"], (128, 128))
     
        source = pygame.image.load(Path("TD/assets/TD CX-5 2.png"))
        source = source.convert_alpha()
        self.sprites["CX5"] = load_sprites_from_sheet(source, [
            (0,0,64,64),
            (64,0,64,64),
            (128,0,64,64),
            (192,0,64,64),
        ])

        self.sprites["D2"] = load_sprite_from_files(Path("TD/assets/TD D-2 .png"), ["001", "002", "003", "004"])

        self.sprites["Pickup Heart"] = load_sprite_from_files(Path("TD/assets/pickup heart/TD_Pickup_Heart.png"), ["-{}".format(i+1) for i in range(4)])
        self.sprites["Pickup Heart"] = scale_sprites(self.sprites["Pickup Heart"], (48, 48))
        self.sprites["Pickup Star"] = load_sprite_from_files(Path("TD/assets/star shadow/TD_Pickup_Star.png"), ["-{}".format(i+1) for i in range(15)])
        

        # source = pygame.image.load(Path("TD/assets/TD Powerups 001.png"))

        source = pygame.image.load(Path("TD/assets/TD Explosion M 001.png"))
        source = source.convert_alpha()
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

        self.sprites["Bullet Green Round 001"] = {}
        self.sprites["Bullet Green Round 001"][0] = load_sprite_from_files(Path("TD/assets/bullet green round 001/TD_Bullet_Green_Round_001.png"), ["-{}".format(i+1) for i in range(5)])
        self.sprites["Bullet Green Round 001"][0] = scale_sprites(self.sprites["Bullet Green Round 001"][0], (38/2, 84/2))
        self.sprites["Bullet Green Round 001"][0] = rotate_sprites(self.sprites["Bullet Green Round 001"][0], -90)
        create_rotations(self.sprites["Bullet Green Round 001"], self.sprites["Bullet Green Round 001"][0], [-15, 15,180])

        self.sprites["Bullet Blue Round 001"] = {}
        self.sprites["Bullet Blue Round 001"][0] = load_sprite_from_file(Path("TD/assets/bullet blue round 001.png"))

        self.sprites["Menu Cursor Left"] = load_sprite_from_files(Path("TD/assets/menu cursor/TD_Menu_Cursor.png"), ["-{}".format(i+1) for i in range(9)])
        self.sprites["Menu Cursor Left"] = rotate_sprites(self.sprites["Menu Cursor Left"], -90)
        self.sprites["Menu Cursor Right"] = flip_sprites(self.sprites["Menu Cursor Left"], flip_x=True)

        self.sprites["HUD"] = load_sprite_from_files(Path("TD/assets/HUD/TD_HUD.png"), ["-{}".format(i+1) for i in range(16)])

        self.sprites["HUD Hurt"] = load_sprite_from_file(Path("TD/assets/HUD hurt.png"))
        self.sprites["HUD Hurt"][0].set_alpha(50)

# Singleton Pattern - Stinky, but practical for a game environment
asset_manager = AssetManager()
