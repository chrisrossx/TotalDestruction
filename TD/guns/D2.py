from .guns import AimingGun
from TD.bullets import Bullet003, Bullet004

class GunD2Level1(AimingGun):
    def __init__(self):
        super().__init__()
        x = 500
        self.pattern_rate = [750, 1800]

    def bullet_factory(self, angle):
        #Generic spot copies from gun_point[0] always
        b = Bullet004(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .45
        return b
