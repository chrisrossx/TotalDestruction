from .guns import AimingGun, GenericGun
from TD.bullets import Bullet003, Bullet004, Bullet005, Missile



class GunBoss004LargeLaser(GenericGun):
    def __init__(self, parent):
        super().__init__(parent)
        self.gun_point = self.parent.gun_points[1]
        self.sound = "enemy laser"

        x = 20
        s = 100
        # self.pattern_rate = [-1000, 2000] + [s for i in range(x)]
        self.pattern_rate = [-1000, 2000, s, s]
        s = 12
        self.pattern_angle = [0, 0, 10, 18]

        # self.bullet_angles = [0, 90, 180, 270]
        s = 36
        self.bullet_angles = [a * (360/s) for a in range(s)]

    def bullet_factory(self, angle):
        b = Bullet003(self.parent.pos + self.gun_point, angle)
        b.velocity = 0.56
        return b



class GunBoss004LargeLaser(GenericGun):
    def __init__(self, parent):
        super().__init__(parent)
        self.gun_point = self.parent.gun_points[1]
        self.sound = "enemy laser"

        s = 150
        self.pattern_rate = [-1000, 2000, s, s]
        self.pattern_angle = [0, 0, 0, 0]

        # self.bullet_angles = [0, 90, 180, 270]
        s = 36 / 3
        # self.bullet_angles = [a * (360/s) for a in range(s)]
        self.bullet_angles = []
        for i in range(int(s)):
            self.bullet_angles.append(i * (360/s))
            self.bullet_angles.append(i * (360/s)+3)
            self.bullet_angles.append(i * (360/s)+6)

    def bullet_factory(self, angle):
        b = Bullet003(self.parent.pos + self.gun_point, angle)
        b.velocity = 0.56
        return b




class GunBoss004Level1Missle001Right(GenericGun):
    def __init__(self, parent):
        super().__init__(parent=parent)
        x = 300
        self.pattern_rate = [-2400, 3000, x, x, x, x, x, x, x, x ]
        self.pattern_angle = [(e*10)+120 for e in range(len(self.pattern_rate)-1)]
        self.pattern_angle.insert(0, 0)        
        self.gun_point = self.parent.gun_points[2]
        self.sound = "enemy missile"
        
    def bullet_factory(self, angle):
        b = Missile(self.parent.pos + self.gun_point, angle)
        b.velocity = .30
        return b

class GunBoss004Level1Missle001Left(GunBoss004Level1Missle001Right):
    def __init__(self, parent):
        super().__init__(parent)
        self.gun_point = self.parent.gun_points[1]
        

