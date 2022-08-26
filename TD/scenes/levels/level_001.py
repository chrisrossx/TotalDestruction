from pygame import Vector2 

from TD.scenes.levels.level import Level
from .level_state import LevelState
from TD.pickups import PickupHeart, PickupCoin
from TD.guns import SingleShotGun, ConstantFireGun, GenericGun, AimingGun
from TD.scenes.levels.level_chains import *
from TD.scenes.levels.enemy_chain import ChainGunFactory
from TD import current_app

from TD.enemies.boss import Boss001

class Level_001(Level):

    level = 1

    def load(self):
        current_app.mixer.play_music("level 001")

        t = 0



        t = 1000
        c = CX5BChain(self, t, "slant top 1")
        c.add_drops([PickupHeart, ], [2,])
        c.set_guns(ChainGunFactory(AimingGun))

        t += 1200 + 100
        c = CX5BChain(self, t, "slant top 2")

        t += 8000
        c = CX5BChain(self, t, "slant bottom 1")
        c.add_drops([PickupHeart, ], [2,])

        t += 1200
        c = CX5BChain(self, t, "slant bottom 2")


        t += 7200
        c = T8Chain(self, t, "bravo loop 1")

        t += 11200
        c = T8Chain(self, t, "bravo loop 1 MY")

        t+= 11200

        boss = Boss001()
        self.add_level_entity(t, boss)

        print("Level Length", t)
