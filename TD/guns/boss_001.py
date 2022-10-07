from .guns import AimingGun, GenericGun
from TD.bullets import Bullet003, Bullet004, Bullet005, Missile

class GunBoss001Level1Missle001Left(GenericGun):
    def __init__(self, parent):
        super().__init__(parent=parent)
        x = 350
        self.pattern_rate = [-4000, 5000, x, x, x, x, x, x, ]
        self.pattern_angle = [(e*10)+120 for e in range(len(self.pattern_rate)-1)]
        self.pattern_angle.insert(0, 0)        
        self.gun_point = self.parent.gun_points[3]
        self.sound = "enemy missile"
        
    def bullet_factory(self, angle):
        b = Missile(self.parent.pos + self.gun_point, angle)
        return b

class GunBoss001Level1Missle001Right(GunBoss001Level1Missle001Left):
    def __init__(self, parent):
        super().__init__(parent)
        self.gun_point = self.parent.gun_points[4]
        

class GunBoss001Level1Laser001Left(GenericGun):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.sound = "enemy laser"
        x = 100
        self.pattern_rate = [-4000, 4000, x, x, x, x, x, x, x, x, ]
        self.pattern_angle = [(e*15)+90+30 for e in range(len(self.pattern_rate)-1)]
        self.pattern_angle.insert(0, 0)        
        self.gun_point = self.parent.gun_points[0]

    def bullet_factory(self, angle):
        b = Bullet003(self.parent.pos + self.gun_point, angle)
        return b

class GunBoss001Level1Laser002Center(GunBoss001Level1Laser001Left):
    def __init__(self, parent):
        super().__init__(parent=parent)
        x = 10
        s = 20
        self.pattern_rate = [x for e in range(int(360/s))]  
        self.pattern_rate.insert(0, -2500)  #5000 = 4000 initial plus 1000 on first fire for pattern
        self.pattern_rate[1] = 3000
        self.pattern_angle = [e*s for e in range(int(360/s))]
        self.pattern_angle.insert(0, 0)

        self.gun_point = self.parent.gun_points[1]

class GunBoss001Level1Laser003Right(GunBoss001Level1Laser001Left):
    def __init__(self, parent):
        super().__init__(parent)


        x = 110

        self.pattern_rate = [-4000, 4000, x, x, x, x, x, x, x, x, x, x,]
        self.pattern_angle = [0, 135, 150, 165, 180, 195, 210, 195, 180, 165, 150, 135]
        self.gun_point = self.parent.gun_points[2]