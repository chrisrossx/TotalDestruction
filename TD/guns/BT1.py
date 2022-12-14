from .guns import AimingGun, GenericGun
from TD.bullets import Bullet004, Bullet005

from .guns import AimingGun
from TD.bullets import Bullet003


class GunBT1Level2Bullet005(GenericGun):
    pass
    def __init__(self, parent):
        super().__init__(parent)
        self.pattern_rate = [0, 1000, 100, 100, 100]
        self.pattern_angle = [0, 180, 190, 200, 210]
        self.bullet_angles = [0, -45, 45]

    def bullet_factory(self, angle):
        b = Bullet005(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .45
        return b



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


class GunBT1Level2Bullet005_Wall_Up(GenericGun):
    pass
    def __init__(self, parent):
        super().__init__(parent)
        self.sound = "enemy tank"
        x = 200
        self.pattern_rate = [0, 600, x, x, x, x, x, x, x, x, x, x, x, x, x, x]
        self.pattern_angle = 102.5
        # self.bullet_angles = [0, -45, 45]

    def bullet_factory(self, angle):
        b = Bullet005(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .45
        return b

class GunBT1Level2Bullet005_Wall_Down(GunBT1Level2Bullet005_Wall_Up):
    pass
    def __init__(self, parent):
        super().__init__(parent)
        self.pattern_angle = 270 - 12.5


class GunBT1Level3Bullet005(GenericGun):
    pass
    def __init__(self, parent):
        super().__init__(parent)
        s = 150
        self.pattern_rate = [-1000, 2000] + [s for i in range(9)]
        s = 10
        self.pattern_angle = [0, 180] + [180+s + (i*s) for i in range(9)]
        # self.pattern_rate = [-1000, 2000, s, s, s, s, s, s, s, s, s]
        # self.pattern_angle = [0, 180, 190, 200, 210]
        # self.pattern_angle = [0, 180, 190, 200, 210]
        self.bullet_angles = [0, 90, 180, 270]

    def bullet_factory(self, angle):
        b = Bullet005(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .35
        return b


class GunBT1Level4Bullet005_DiagDown(GenericGun):
    pass
    def __init__(self, parent):
        super().__init__(parent)
        self.sound = "enemy tank"
        x = 200
        self.pattern_rate = [0, 600, x, x, x, x, x, x, x, x, x, x, x, x, x, x]
        self.pattern_angle = 180+30
        # self.bullet_angles = [0, -45, 45]

    def bullet_factory(self, angle):
        b = Bullet005(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .45
        return b

class GunBT1Level4Bullet005_DiagUp(GenericGun):
    pass
    def __init__(self, parent):
        super().__init__(parent)
        self.sound = "enemy tank"
        x = 200
        self.pattern_rate = [0, 600, x, x, x, x, x, x, x, x, x, x, x, x, x, x]
        self.pattern_angle = 180-30
        # self.bullet_angles = [0, -45, 45]

    def bullet_factory(self, angle):
        b = Bullet005(self.parent.pos + self.parent.gun_points[0], angle)
        b.velocity = .45
        return b
