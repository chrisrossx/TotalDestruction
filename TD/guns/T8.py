from .guns import AimingGun, GenericGun
from TD.bullets import Bullet003, Bullet004, Bullet002


class GunT8Level1(GenericGun):
    def __init__(self, parent):
        super().__init__(parent)
        x = 500
        self.pattern_rate = [0, 500]
        self.bullet_angles = [0, -15, 15]
        self.pattern_repeat = 1 
        
        self.sound = "enemy tank"

    def bullet_factory(self, angle):
        #Generic spot copies from gun_point[0] always
        b = Bullet002(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .275
        return b
