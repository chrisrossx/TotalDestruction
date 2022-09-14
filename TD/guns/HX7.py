from .guns import AimingGun, GenericGun
from TD.bullets import Bullet004, Bullet005, Missile

class GunHX7Level1Missle001(GenericGun):
    def __init__(self):
        super().__init__()
        x = 500
        self.pattern_rate = [-1000, 1800]
        self.pattern_repeat = 2

    def bullet_factory(self, angle):
        #Generic spot copies from gun_point[0] always
        # b = Bullet004(self.parent.pos + self.parent.gun_points[0], angle)
        b = Missile(self.parent.pos + self.parent.gun_points[0], angle)
        # b.velocity = .45
        return b
