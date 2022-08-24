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

    def __init__(self):
        super().__init__(level=1)
        current_app.mixer.play_music("level 001")

        t = 0


        boss = Boss001()
        # boss.pos = Vector2(800, 300)
        self.em.add(boss)
        c = BT1Chain(self, t, path_index="straight 300")
        c.set_guns(ChainGunFactory(AimingGun))
        
        # # c.set_guns(ChainGunFactory(GenericGun))
        # return
        # t += 1400
        # c = BT1Chain(self, t, path_index="straight 100")
        # c = BT1Chain(self, t, path_index="straight 500")
        # c = CX5BChain(self, t, "slant bottom 1")
        # # c.set_guns(ChainGunFactory(Gun))

        # # t += 1000 
        # c = BT1Chain(self, t, "slant bottom 1")
        # # c.set_guns(ChainGunFactory(Gun))

        # c = D2Chain(self, t, path_index="straight")

        # return 
        t = 1000
        c = CX5BChain(self, t, "slant top 1")
        c.add_drops([PickupHeart, ], [2,])
        c.set_guns(ChainGunFactory(AimingGun))
        # c.set_guns(ChainGunFactory(SingleShotGun, delay=1000), [1,])

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

        print("Level Length", t)
        # t += 1200
        # c = T8Chain(self, t, "slant bottom 3")

        # c = T8Chain(self, t, "alpha pattern MX", gun=ChainGunFactory(SingleShotGun, delay=1000))

        # t += 5000

        # c = T8Chain(self, t, 2, gun=ChainGunFactory(SingleShotGun, delay=1000))
