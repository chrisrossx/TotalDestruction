from pygame import Vector2

from TD.bullets import Bullet002, Bullet003
from TD import current_scene


class ConstantFireGun:
    def __init__(self):
        self.firing = True
        self.elapsed = 1000 # Start high so fire right away 
        self.rate = 3
        self.parent = None 

    def fire(self):
        b = Bullet002(self.parent.pos + self.parent.gun_points[0], 0)
        current_scene.em.add(b)

    def tick(self, elapsed):
        self.elapsed += elapsed 
        if self.elapsed >= (1000.0 / self.rate):
            self.elapsed = 0
            self.fire()


class SingleShotGun():

        def __init__(self, delay=1000):
            self.elapsed = 0
            self.fired = False 
            self.delayed_fire = delay
            self.parent = None

        def fire(self):
            b = Bullet002(self.parent.pos + self.parent.gun_points[0], 0)
            current_scene.em.add(b)

        def tick(self, elapsed):
            if not self.fired:
                self.elapsed += elapsed 
                if self.elapsed >= self.delayed_fire:
                    self.fired = True 
                    self.fire()

class GenericGun():
    def __init__(self):
        self.elapsed = 0 # Start high so fire right away 
        self.parent = None # Needed to copy gun_points location
        self.enabled = True # Fire or Not.. Is set to false after pattern completion
        self.fired = 0 # Keep track of how many bullets fired
        self.step = 0 # What step of the pattern 
        self.pattern_count = 0 # How many times has the pattern repeated so far

        self.pattern_repeat = -1 # Set by user, stop repeating pattern after this many times
        # [0] = Initial, only ran once! Does not Fire
        # [1-X] = Step through Pattern, Fire after step pause
        # at X: Go back to 1, Repeate for Pattern repeat counts
        # [1000, 500, 500, 500] Pause 1000 do nothing, Fire every 500ms
        self.pattern_rate = [0, 1000]
        self.pattern_angle = 180

        # Example of Firing a bullet 360degrees every 10degrees )36 bullets)
        # After an initial pause of 5000ms, and then a pause every 1000
        # x = 0
        # self.pattern_rate = [x for e in range(36)]  
        # self.pattern_rate.insert(0, 4000)  #5000 = 4000 initial plus 1000 on first fire for pattern
        # self.pattern_rate[1] = 1000
        # self.pattern_angle = [e*10 for e in range(36)]
        # self.pattern_angle.insert(0, 0)
        

    def bullet_factory(self, angle):
        #Generic spot copies from gun_point[0] always
        return Bullet003(self.parent.pos + self.parent.gun_points[0], angle)

    def get_angle(self):
        if type(self.pattern_angle) == list:
            return self.pattern_angle[self.step]
        else:
            return self.pattern_angle

    def fire(self):
        angle = self.get_angle()
        b = self.bullet_factory(angle)
        current_scene.em.add(b)
        self.fired += 1

    def tick_pattern(self, elapsed):
        if self.enabled:
            self.elapsed += elapsed 
            d = self.pattern_rate[self.step]
            if self.elapsed >= d:
                self.elapsed = 0
                # Dont Fire on First Step of Pattern
                if self.step > 0: 
                    self.fire()
                self.step += 1
                # Check if end of pattern
                if self.step == len(self.pattern_rate):
                    self.step = 1
                    self.pattern_count += 1
                    # Check if Pattern Repeat has been met and disable gun
                    if self.pattern_repeat != -1:
                        if self.pattern_count == self.pattern_repeat:
                            # Reset Gun ready to start again if enabled
                            self.step = 0 
                            self.enabled = False 

    def tick(self, elapsed):
        #Loop through to fire all bullets in the pattern that have 0ms delay
        while True:
            self.tick_pattern(elapsed)
            if self.pattern_rate[self.step] > 0 or self.enabled == False:
                break

class AimingGun(GenericGun):
    def __init__(self):
        super().__init__()
        x = 100
        self.pattern_rate = [1000, 1000, x, x, x, x, x, x]
        self.pattern_rate = [1000, 1000, x, x]

    def get_angle(self):
        player_pos = current_scene.player.get_pos()
        gun_pos = self.parent.pos + self.parent.gun_points[0]
        angle1 = player_pos - gun_pos
        angle1.normalize_ip()
        angle1 = angle1.angle_to((0,0)) * 1
        return angle1

    def bullet_factory(self, angle):
        return Bullet002(self.parent.pos + self.parent.gun_points[0], angle)
