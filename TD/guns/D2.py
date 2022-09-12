from .guns import AimingGun
from TD.bullets import Bullet003

class GunD2Level1(AimingGun):
    def __init__(self):
        super().__init__()
        x = 500
        self.pattern_rate = [750, 1800]

    def bullet_factory(self, angle):
        #Generic spot copies from gun_point[0] always
        b = Bullet003(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .5
        return b

class GunD2Level2(AimingGun):
    pass

# class GunD2Level2BXXX(AimingGun):
#     pass

