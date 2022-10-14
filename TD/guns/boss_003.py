from .guns import AimingGun, GenericGun
from TD.bullets import Bullet003, Bullet004, Bullet005, Missile


class GunBoss003LaserPod(AimingGun):
    def __init__(self, parent):
        super().__init__(parent)
        self.gun_point = self.parent.gun_points[0]
        self.sound = "enemy laser"
        x = 50
        self.pattern_rate = [-750, 1000] + [x for i in range(12)]

    def bullet_factory(self, angle):
        b = Bullet003(self.parent.pos + self.gun_point, angle)
        b.velocity = 0.56
        return b



class GunBoss003LargeLaser(GenericGun):
    def __init__(self, parent):
        super().__init__(parent)
        self.gun_point = self.parent.gun_points[1]
        self.sound = "enemy laser"

        x = 20
        s = 100
        self.pattern_rate = [-1000, 2000] + [s for i in range(x)]
        s = 12
        self.pattern_angle = [0, 180] + [180+s + (i*s) for i in range(x)]
        self.bullet_angles = [0, 90, 180, 270]

    def bullet_factory(self, angle):
        b = Bullet003(self.parent.pos + self.gun_point, angle)
        b.velocity = 0.56
        return b


