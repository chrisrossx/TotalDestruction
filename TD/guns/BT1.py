from .guns import AimingGun
from TD.bullets import Bullet004, Bullet005

class GunBT1Level1Bullet004(AimingGun):
    def __init__(self):
        super().__init__()
        x = 500
        self.pattern_rate = [750, 1800]

    def bullet_factory(self, angle):
        #Generic spot copies from gun_point[0] always
        b = Bullet004(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .45
        return b

from .guns import AimingGun
from TD.bullets import Bullet003

class GunBT1Level2Bullet005(AimingGun):
    def __init__(self):
        super().__init__()
        x = 500
        self.pattern_rate = [750, 1800]

    def bullet_factory(self, angle):
        #Generic spot copies from gun_point[0] always
        b = Bullet005(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .35
        return b
