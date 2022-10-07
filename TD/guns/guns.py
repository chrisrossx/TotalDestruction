from pygame import Vector2

from TD.bullets import Bullet002, Bullet003, Bullet005
from TD import current_scene
from TD.config import SCREEN_RECT
from TD.globals import current_app


class GenericGun():
    def __init__(self, parent):
        self.sound = None
        self.elapsed = 0 # Start high so fire right away 
        self.parent = parent # Needed to copy gun_points location
        self.enabled = True # Fire or Not.. Is set to false after pattern completion
        self.fired = 0 # Keep track of how many bullets fired
        self.step = 0 # What step of the pattern 
        self.pattern_count = 0 # How many times has the pattern repeated so far, Not set by user

        self.pattern_repeat = -1 # Set by user, stop repeating pattern after this many times
        # [0] = Initial, only ran once! Does not Fire. If step [0] is negative then subtract from Step 1
        # [1-X] = Step through Pattern, Fire after step pause
        # at X: Go back to 1, Repeate for Pattern repeat counts
        # [1000, 500, 500, 500] Pause 1000 do nothing, Fire every 500ms
        self.pattern_rate = [0, 1000]
        self.pattern_angle = 180

        # self.bullet_angles = [0, 90, 180, 270] # Each Firing offset this number of bullets by the given angels
        self.bullet_angles = [0, ] # Each Firing offset this number of bullets by the given angels

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


#     def bullet_factory(self, angle):
#         #Generic spot copies from gun_point[0] always
#         # self.bullet_angles = [0, 90, 180, 270]
#         base_angle = angle 
#         bullets = []
#         for angle_offset in self.bullet_angles:
#             new_angle = base_angle + angle_offset
#             b = Bullet005(self.parent.pos + self.parent.gun_points[0], new_angle)
#             bullets.append(b)
#         return bullets


    def fire(self):
        #Paths go off screen, don't fire bullets if enemy pos is off screen
        if SCREEN_RECT.collidepoint(self.parent.pos):
            base_angle = self.get_angle()
            for angle_offset in self.bullet_angles:
                new_angle = base_angle + angle_offset
                b = self.bullet_factory(new_angle)
                current_scene.em.add(b)

                self.fired += 1
            #Only fire sound once per step of bullet firing. If 10 bullets are fired at 0ms offset, only play sound once. 
            if self.sound != None:
                current_app.mixer.play(self.sound)

    def tick_pattern(self, elapsed):
        if self.enabled:
            self.elapsed += elapsed
            d = self.pattern_rate[self.step]
            if self.step == 0 and d < 0:
                self.step += 1
                self.elapsed = -d
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
    def __init__(self, parent):
        super().__init__(parent=parent)
        x = 100
        self.pattern_rate = [1000, 1000, x, x, x, x, x, x]
        self.pattern_rate = [1000, 1000, x, x]

    def get_angle(self):
        player_pos = current_scene.player.get_pos()
        gun_pos = self.parent.pos + self.parent.gun_points[0]
        angle1 = player_pos - gun_pos
        angle1.normalize_ip()
        angle1 = angle1.angle_to((0,0)) #* 1
        return angle1

    def bullet_factory(self, angle):
        return Bullet002(self.parent.pos + self.parent.gun_points[0], angle)


# class RadialGun(GenericGun):
#     def __init__(self, parent=None):
#         super().__init__(parent)

        

#     def bullet_factory(self, angle):
#         #Generic spot copies from gun_point[0] always
#         # self.bullet_angles = [0, 90, 180, 270]
#         base_angle = angle 
#         bullets = []
#         for angle_offset in self.bullet_angles:
#             new_angle = base_angle + angle_offset
#             b = Bullet005(self.parent.pos + self.parent.gun_points[0], new_angle)
#             bullets.append(b)
#         return bullets

#     def fire(self):
#         #Paths go off screen, don't fire bullets if enemy pos is off screen
#         if SCREEN_RECT.collidepoint(self.parent.pos):
#             angle = self.get_angle()
#             bullets = self.bullet_factory(angle)
#             for b in bullets:
#                 current_scene.em.add(b)
#             self.fired += 1
#             if self.sound != None:
#                 current_app.mixer.play(self.sound)
