from .guns import AimingGun, GenericGun
from TD.bullets import Bullet003, Bullet004, Bullet005, Missile


class GunBoss002RightGun(AimingGun):
    def __init__(self, parent):
        super().__init__(parent)
        self.gun_point = self.parent.gun_points[0]
        self.sound = "enemy laser"
        x = 150
        self.pattern_rate = [0, 1500, x, x, x, x, x, x]

    def bullet_factory(self, angle):
        b = Bullet004(self.parent.pos + self.gun_point, angle)
        b.velocity = 0.56
        return b

class GunBoss002LeftGun(GunBoss002RightGun):
    def __init__(self, parent):
        super().__init__(parent)
        self.gun_point = self.parent.gun_points[1]

class GunBoss002Level1Missle001Right(GenericGun):
    def __init__(self, parent):
        super().__init__(parent=parent)
        x = 350
        self.pattern_rate = [-4000, 5000, x, x, x, x, x, x, ]
        self.pattern_angle = [(e*10)+120 for e in range(len(self.pattern_rate)-1)]
        self.pattern_angle.insert(0, 0)        
        self.gun_point = self.parent.gun_points[2]
        self.sound = "enemy missile"
        
    def bullet_factory(self, angle):
        b = Missile(self.parent.pos + self.gun_point, angle)
        b.velocity = .26
        return b

class GunBoss002Level1Missle001Left(GunBoss002Level1Missle001Right):
    def __init__(self, parent):
        super().__init__(parent)
        self.gun_point = self.parent.gun_points[3]
        