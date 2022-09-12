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


class AssetManager:
    
    def __init__(self):

        self.sprites = {}
        self.fonts = {}

        self.sounds = {}
        self.music = {}

    def load(self):

        self.fonts["xxs"] = pygame.font.Font(Path("TD/assets/BebasNeue-Regular.ttf"), 14)
        self.fonts["xs"] = pygame.font.Font(Path("TD/assets/BebasNeue-Regular.ttf"), 18)
        self.fonts["sm"] = pygame.font.Font(Path("TD/assets/BebasNeue-Regular.ttf"), 24)
        self.fonts["md"] = pygame.font.Font(Path("TD/assets/BebasNeue-Regular.ttf"), 48)
        self.fonts["lg"] = pygame.font.Font(Path("TD/assets/BebasNeue-Regular.ttf"), 96)


        self.sounds["coin pickup"] = pygame.mixer.Sound(str(Path("TD/assets/CoinBrass.wav")))
        self.sounds["heart pickup"] = pygame.mixer.Sound(str(Path("TD/assets/CoinThree.wav")))
        self.sounds["explosion md"] = pygame.mixer.Sound(str(Path("TD/assets/ExploFuel.wav")))
        self.sounds["weapons upgrade"] = pygame.mixer.Sound(str(Path("TD/assets/weapons upgrade.wav")))
        self.sounds["chain lost"] = pygame.mixer.Sound(str(Path("TD/assets/chain lost.wav")))
        self.sounds["health restored"] = pygame.mixer.Sound(str(Path("TD/assets/health restored.wav")))
        
        self.sounds["explosion sm"] = pygame.mixer.Sound(str(Path("TD/assets/Dynamite1.wav")))
        self.sounds["explosion sm"].set_volume(0.5)
        
        self.sounds["explosion player"] = pygame.mixer.Sound(str(Path("TD/assets/ExploBreakage2.wav")))
        self.sounds["player hit"] = pygame.mixer.Sound(str(Path("TD/assets/ExploMetalbits.wav")))
        self.sounds["player collision"] = pygame.mixer.Sound(str(Path("TD/assets/HitMetalBasher.wav")))
        self.sounds["player gun"] = pygame.mixer.Sound(str(Path("TD/assets/GunUp.wav")))
        self.sounds["player gun"].set_volume(0.3)

        self.sounds["enemy hit"] = pygame.mixer.Sound(str(Path("TD/assets/HitMetalDull1.wav")))
        self.sounds["enemy hit"].set_volume(0.3)

        self.sounds["missile launch"] = pygame.mixer.Sound(str(Path("TD/assets/Robot_Weapon_Electricity.wav")))
        self.sounds["missile launch 002"] = pygame.mixer.Sound(str(Path("TD/assets/Robot_Weapon_Recharge_02.wav")))

        self.sounds["boss servo 001"] = pygame.mixer.Sound(str(Path("TD/assets/Robot_Movement_Gesture_4A.wav")))
        self.sounds["boss servo 002"] = pygame.mixer.Sound(str(Path("TD/assets/Robot_Movement_Head_01.wav")))
        
        self.sounds["boss laser 001"] = pygame.mixer.Sound(str(Path("TD/assets/Robot_ON.wav")))
        self.sounds["boss laser 002"] = pygame.mixer.Sound(str(Path("TD/assets/Robot_Weapon_Release_01.wav")))

        self.sounds["menu move"] = pygame.mixer.Sound(str(Path("TD/assets/CatchClose.wav")))
        self.sounds["menu click"] = pygame.mixer.Sound(str(Path("TD/assets/CatchOpen.wav")))
        # self.sounds["menu type"] = pygame.mixer.Sound(str(Path("TD/assets/HitMetalBash.wav")))
        self.sounds["menu type"] = pygame.mixer.Sound(str(Path("TD/assets/UI_Button_Click.wav")))
        self.sounds["menu error"] = pygame.mixer.Sound(str(Path("TD/assets/Tinyclick1.wav")))

        self.sounds["menu score coins"] = pygame.mixer.Sound(str(Path("TD/assets/BonusBeep.wav")))
        self.sounds["menu score 0"] = pygame.mixer.Sound(str(Path("TD/assets/KnockDeep.wav")))
        self.sounds["menu score 1"] = pygame.mixer.Sound(str(Path("TD/assets/SlamCool.wav")))
        self.sounds["menu score 2"] = pygame.mixer.Sound(str(Path("TD/assets/SlamCooltoo.wav")))
        self.sounds["menu score 3"] = pygame.mixer.Sound(str(Path("TD/assets/SlamCooltree.wav")))

        self.sounds["menu error"] = self.sounds["menu score 0"]


        # self.sounds["menu error"].set_volume(0.3)
        


        self.music["menu"] = {"filename": str(Path("TD/assets/sabotage_loop.flac")), "volume": 1}
        self.music["the net"] = {"filename": str(Path("TD/assets/the net.mp3")), "volume": 1}

        self.music["level 001"] = {"filename": str(Path("TD/assets/lootedvillage_orc_vox.mp3")), "volume": 0.2}
        self.music["level 002"] = {"filename": str(Path("TD/assets/battle_zero_2022_remaster_update.mp3")), "volume": 0.2}



        self.sprites["sky layered"] = pygame.image.load(str(Path("TD/assets/layered.jpg")))
        self.sprites["sky layered"] = self.sprites["sky layered"].convert()

        source = pygame.image.load(Path("TD/assets/T8/TD T-8.png"))
        source = source.convert_alpha()
        self.sprites["T8"] = load_sprites_from_sheet(source, [
            (0,0,64,64),
            (64,0,64,64),
            (128,0,64,64),
            (192,0,64,64),
        ])
        # self.sprites["T8"] = scale_sprites(self.sprites["T8"], (128, 128))
     
        source = pygame.image.load(Path("TD/assets/CX5/TD CX-5 2.png"))
        source = source.convert_alpha()
        self.sprites["CX5B"] = load_sprites_from_sheet(source, [
            (0,0,64,64),
            (64,0,64,64),
            (128,0,64,64),
            (192,0,64,64),
        ])

        self.sprites["D2"] = load_sprite_from_files(Path("TD/assets/D2/TD_D2.png"), ["-{}".format(i+1) for i in range(4)])

        self.sprites["BT1"] = load_sprite_from_files(Path("TD/assets/BT1/TD_BT1.png"), ["-{}".format(i+1) for i in range(18)])

        self.sprites["HX7"] = load_sprite_from_files(Path("TD/assets/HX7/TD_HX7.png"), ["-{}".format(i+1) for i in range(5)])

        self.sprites["Boss 001"] = load_sprite_from_files(Path("TD/assets/boss 001/TD_BOSS_001.png"), ["-{}".format(i+1) for i in range(12)])
        self.sprites["Boss 001 laser"] = load_sprite_from_files(Path("TD/assets/boss 001/TD_BOSS_001_Laser.png"), ["-{}".format(i+1) for i in range(17)])
        self.sprites["Boss 001 launchers"] = load_sprite_from_files(Path("TD/assets/boss 001/TD_BOSS_001_Launchers.png"), ["-{}".format(i+1) for i in range(9)])

        self.sprites["Pickup Heart"] = load_sprite_from_files(Path("TD/assets/pickup heart/TD_Pickup_Heart.png"), ["-{}".format(i+1) for i in range(4)])
        self.sprites["Pickup Heart"] = scale_sprites(self.sprites["Pickup Heart"], (48, 48))
        self.sprites["Pickup Coin"] = load_sprite_from_files(Path("TD/assets/pickup coin/TD_Pickup_Star.png"), ["-{}".format(i+1) for i in range(15)])
        self.sprites["Pickup Upgrade"] = load_sprite_from_files(Path("TD/assets/pickup upgrade/TD_Pickup_Upgrade.png"), ["-{}".format(i+1) for i in range(18)])

        self.sprites["Explosion Medium"] = load_sprite_from_files(Path("TD/assets/explosion medium/TD_Explosion_Medium.png"), ["-{}".format(i+1) for i in range(13)])

        self.sprites["Explosion Small"] = load_sprite_from_files(Path("TD/assets/explosion sm/TD_Explosion_SM_001.png"), ["-{}".format(i+1) for i in range(8)])
        self.sprites["Explosion Small"] = scale_sprites(self.sprites["Explosion Small"], (64, 64))

        self.sprites["Bullet 001"] = load_sprite_from_files(Path("TD/assets/Bullet 001/TD_Bullet_Green_Round_001.png"), ["-{}".format(i+1) for i in range(5)])
        self.sprites["Bullet 001"] = scale_sprites(self.sprites["Bullet 001"], (38/2, 84/2))
        self.sprites["Bullet 001"] = rotate_sprites(self.sprites["Bullet 001"], -90)

        self.sprites["Bullet 002"] = load_sprite_from_file(Path("TD/assets/Bullet 002/Bullet 002.png"))

        self.sprites["Bullet 003"] = load_sprite_from_files(Path("TD/assets/Bullet 003/TD_Bullet_003.png"), ["-{}".format(i+1) for i in range(4)])
        self.sprites["Bullet 004"] = load_sprite_from_files(Path("TD/assets/Bullet 004/TD_Bullet_004.png"), ["-{}".format(i+1) for i in range(4)])
        self.sprites["Bullet 004"] = rotate_sprites(self.sprites["Bullet 004"], -90)
        self.sprites["Bullet 005"] = load_sprite_from_files(Path("TD/assets/Bullet 005/TD_Bullet_005.png"), ["-{}".format(i+1) for i in range(4)])

        self.sprites["Missile 001"] = load_sprite_from_files(Path("TD/assets/Missile 001/TD_Missile_001.png"), ["-{}".format(i+1) for i in range(6)])
        self.sprites["Missile 001"] = rotate_sprites(self.sprites["Missile 001"], -90)

        self.sprites["Missile Smoke 004"] =  load_sprite_from_files(Path("TD/assets/missile smoke/TD_Missile_Smoke_004.png"), ["-{}".format(i+1) for i in range(2,8)])
        self.sprites["Missile Smoke 002"] =  load_sprite_from_files(Path("TD/assets/missile smoke/TD_Missile_Smoke_004.png"), ["-{}".format(i+1) for i in range(4,5)])


        self.sprites["Spoof 001"] =  load_sprite_from_files(Path("TD/assets/Spoof 001/TD_Spoof.png"), ["-{}".format(i+1) for i in range(4)])
        self.sprites["Spoof Hit 001"] =  load_sprite_from_files(Path("TD/assets/Spoof Hit 001/TD_Spoof_Hit_002.png"), ["-{}".format(i+1) for i in range(6)])

        self.sprites["enemy speech bubble"] =  load_sprite_from_files(Path("TD/assets/speech bubble/TD_Speech_Bubble.png"), ["-{}".format(i+1) for i in range(8)])
        for surface in self.sprites["enemy speech bubble"]:
            surface.set_alpha(128)

        self.sprites["Menu Cursor Left"] = load_sprite_from_files(Path("TD/assets/menu cursor/TD_Menu_Cursor.png"), ["-{}".format(i+1) for i in range(9)])
        self.sprites["Menu Cursor Left"] = rotate_sprites(self.sprites["Menu Cursor Left"], -90)
        self.sprites["Menu Cursor Right"] = flip_sprites(self.sprites["Menu Cursor Left"], flip_x=True)

        self.sprites["Menu Level Select Cursor"] = load_sprite_from_files(Path("TD/assets/level select/TD_Level_Badge_Select_002.png"), ["-{}".format(i+1) for i in range(8)])
        self.sprites["Menu Level Select Badges"] = load_sprite_from_files(Path("TD/assets/level select/TD_Level_Badge.png"), ["-{}".format(i+1) for i in range(12)])
        self.sprites["Menu Level Select Lines"] = load_sprite_from_file(Path("TD/assets/level select/TD_Level_Select_Lines.png"))

        self.sprites["Menu Level Score Confetti"] = load_sprite_from_files(Path("TD/assets/score confetti/TD_Score_Confetti.png"), ["-{}".format(i+1) for i in range(6)])
        self.sprites["Menu Level Score Confetti 2"] = load_sprite_from_files(Path("TD/assets/score confetti/TD_Score_Confetti.png"), ["-{}".format(i+1) for i in range(6)])
        self.sprites["Menu Level Score Confetti 2"] = rotate_sprites(self.sprites["Menu Level Score Confetti 2"], 130)
        self.sprites["Menu Level Score Confetti 2"] = scale_sprites(self.sprites["Menu Level Score Confetti 2"], (48, 48))

        self.sprites["Menu Level Score Confetti Grey"] = load_sprite_from_files(Path("TD/assets/score confetti/TD_Score_Confetti_Grey.png"), ["-{}".format(i+1) for i in range(6)])
        self.sprites["Menu Level Score Confetti Grey 2"] = load_sprite_from_files(Path("TD/assets/score confetti/TD_Score_Confetti_Grey.png"), ["-{}".format(i+1) for i in range(6)])
        self.sprites["Menu Level Score Confetti Grey 2"] = rotate_sprites(self.sprites["Menu Level Score Confetti Grey 2"], 130)
        self.sprites["Menu Level Score Confetti Grey 2"] = scale_sprites(self.sprites["Menu Level Score Confetti Grey 2"], (48, 48))

        self.sprites["the net"] = load_sprite_from_file(Path("TD/assets/net.png"))


        self.sprites["HUD"] = load_sprite_from_files(Path("TD/assets/HUD/TD_HUD.png"), ["-{}".format(i+1) for i in range(16)])

        self.sprites["HUD Hurt"] = load_sprite_from_file(Path("TD/assets/HUD hurt.png"))
        self.sprites["HUD Hurt"][0].set_alpha(50)
        self.sprites["title"] = load_sprite_from_file(Path("TD/assets/Title_Art_001.png"))

        self.sprites["Sawyer"] = load_sprite_from_file(Path("TD/assets/TD_Sawyer.png"))
        self.sprites["Elle"] = load_sprite_from_file(Path("TD/assets/TD_Elle.png"))
        self.sprites["Christopher"] = load_sprite_from_file(Path("TD/assets/TD_Christopher.png"))
        self.sprites["Mai-Anh"] = load_sprite_from_file(Path("TD/assets/TD_MaiAnh.png"))
        self.sprites["Balloons"] = load_sprite_from_file(Path("TD/assets/TD_Balloons.png"))

# Singleton Pattern - Stinky, but practical for a game environment
asset_manager = AssetManager()
