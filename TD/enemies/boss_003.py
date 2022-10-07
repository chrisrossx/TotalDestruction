from enum import Enum
import pygame 

from TD.particles.explosions import ExplosionMedium, ExplosionSmall, ExplosionSmallFollow
from TD.scenes.level.level_state import LevelState
import random 
from pygame import Vector2

from TD.assetmanager import asset_manager
from TD import current_app, current_scene
from TD.guns.boss_001 import GunBoss001Level1Missle001Left, GunBoss001Level1Missle001Right, GunBoss001Level1Laser001Left, GunBoss001Level1Laser002Center, GunBoss001Level1Laser003Right
from TD.characters import Dialog, MaiAnh
from TD.scenes.level.dialog import EnemyDialog
from TD.enemies.boss import BossState, Boss, BossLayeredSprite


SPRITE_OFFSET = Vector2(-36, -60) 
LASER_DOT_RATE = 100

class Boss003State(Enum):
    STARTING = 0
    LASERS_STARTING = 1
    LASERS_SIX = 2
    LASERS_FIVE = 3
    LASERS_FOUR = 4
    LASERS_THREE = 5
    LASERS_TWO = 6
    LASERS_ONE = 7
    LASERS_DEAD = 8
    RAILGUN_LOADING = 9
    RAILGUN_FIRING = 10
    RAILGUN_DEAD = 11
    BALLOONS_EIGHT = 12
    BALLOONS_SEVEN = 13
    BALLOONS_SIX = 14
    BALLOONS_FIVE = 15
    BALLOONS_FOUR = 16
    BALLOONS_THREE = 17
    BALLOONS_TWO = 18
    BALLOONS_ONE = 19
    BALLOONS_DEAD = 20
    DEAD = 21

class Boss003Ship(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprite_offset = SPRITE_OFFSET
        self.sprites = asset_manager.sprites["Boss 003"]

    def draw(self, elapsed, surface):
        return super().draw(elapsed, surface)

class Boss003LaserPod(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 003 laser pod"]
        # self.sprite_offset = SPRITE_OFFSET
        self.sprite_offset = Vector2(19, 65) + SPRITE_OFFSET

class Boss003RailGun(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 003 rail gun"]
        # self.sprite_offset = SPRITE_OFFSET
        self.sprite_offset = Vector2(25, 44) + SPRITE_OFFSET

class Boss003LaserDot(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 003 laser dot"]
        # self.sprite_offset = SPRITE_OFFSET
        self.sprite_offset = Vector2(19, 71) + SPRITE_OFFSET
        self.laser_on = False 
        self.laser_dead = False 

    def set_sprite(self, start_frame, end_frame, duration=-1, loop_end=-1):
        self.frames = self.sprites[start_frame:end_frame]
        for i in range(8):
            self.frames.append(pygame.Surface((1,1), pygame.SRCALPHA))
        self.frame_duration = duration

class BossState_STARTING(BossState):
    state = Boss003State.STARTING
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.ship_sprite.set_sprite(0, 1)
        self.heading = Vector2(-1, 0)
        self.velocity = 0.11
        self.parent.laser_pod_sprite.set_sprite(0, 1)
        self.parent.rail_gun_sprite.set_sprite(0, 1)

        for laser_dot in self.parent.laser_dots:
            laser_dot.set_sprite(0, 10, LASER_DOT_RATE)
            

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.parent.pos.x <= 900:
            enemy_dialog = EnemyDialog(MaiAnh(Dialog.THREAT))
            current_scene.em.add(enemy_dialog)
            self.next_state()



class BossState_LASERSSTARTING(BossState):
    state = Boss003State.LASERS_STARTING
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.laser_dot_index = 0
        self.elapsed = 0 

    def tick(self, elapsed):
        super().tick(elapsed)
        all_found = True 
        for laser_dot in self.parent.laser_dots:
            if laser_dot.laser_on == False and laser_dot.frame_index == 0:
                laser_dot.laser_on = True 
                laser_dot.set_sprite(10, 20, LASER_DOT_RATE)

        all_found = True 
        for laser_dot in self.parent.laser_dots:
            if laser_dot.laser_on == False:
                all_found = False 
                break

        if all_found:
            self.next_state()

    def start(self):
        super().start()
        self.parent.velocity = 0
        current_app.mixer.play("boss laser 001")


class BossState_LASERS_FIRING(BossState):
    state = Boss003State.LASERS_SIX
    def __init__(self, parent, laser_count):
        if laser_count == 6:
            self.state = Boss003State.LASERS_SIX
        elif laser_count == 5:
            self.state = Boss003State.LASERS_FIVE
        elif laser_count == 4:
            self.state = Boss003State.LASERS_FOUR
        elif laser_count == 3:
            self.state = Boss003State.LASERS_THREE
        elif laser_count == 2:
            self.state = Boss003State.LASERS_TWO
        elif laser_count == 1:
            self.state = Boss003State.LASERS_ONE
        super().__init__(parent)
        self.laser_count = laser_count 

    def start(self):
        super().start()
        if self.laser_count == 6:
            self.parent.start_path("boss 001 lasers")
            self.parent.start_path()

        self.health = self.parent.health_by_state[self.state]

    def end(self):
        super().end()
        for i, laser_dot in enumerate(self.parent.laser_dots):
            if i >= self.laser_count - 1:
                laser_dot.set_sprite(20, 30, LASER_DOT_RATE)
                laser_dot.laser_dead = True 
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, 20)))

  
class BossState_LASERS_DEAD(BossState):
    state = Boss003State.LASERS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        for laser_dot in self.parent.laser_dots:
            self.parent.em.delete(laser_dot)
            laser_dot.enabled = False
        
        self.stop_path()
        
        self.parent.laser_pod_sprite.set_sprite(1, 4, 200)

        #lerp vars
        self.distance = 0
        self.pos_start = self.pos.copy()
        self.pos_finish = Vector2(900, 300)
        # Normal Rate is 0.1 pixels per 0.001seconds
        # So if distance is 800 pixels
        # 0.1 at 800 pixels would take 8 seconds 8000
        self.lerp_rate = (1 / self.pos_start.distance_to(self.pos_finish)) * 0.1
        
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(5, 12)))
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-8, 22)))
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, 20)))

        enemy_dialog = EnemyDialog(MaiAnh(Dialog.PAIN))
        current_scene.em.add(enemy_dialog)

    def tick(self, elapsed):
        super().tick(elapsed)
        self.distance += elapsed * self.lerp_rate

        if self.distance >= 1:
            distance = 1
        else:
            distance = self.distance

        self.pos = Vector2.lerp(self.pos_start, self.pos_finish, distance)

        # Take at least one second if distance was short. 
        if distance >= 1 and self.total_elapsed >= 1000:
            self.next_state()
      

class BossState_RAILGUN_LOADING(BossState):
    state = Boss003State.RAILGUN_LOADING
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.laser_pod_sprite.set_sprite(4, 5)
        self.parent.rail_gun_sprite.set_sprite(1, 11, 200, 1)
        self.parent.rail_gun_sprite.callback_animation_finished.append(self.on_animation_finished)
        current_app.mixer.play("boss servo 002")

    def on_animation_finished(self, sender):
        self.next_state()

    def tick(self, elapsed):
        super().tick(elapsed)

    def end(self):
        super().end()
        self.parent.rail_gun_sprite.callback_animation_finished.remove(self.on_animation_finished)

class BossState_RAILGUN_FIRING(BossState):
    state = Boss003State.RAILGUN_FIRING
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.rail_gun_sprite.set_sprite(10, 11)
        self.parent.start_path("boss 001 launchers")
        # self.parent.hitboxes.pop()
        # self.parent.hitbox_offsets.pop()

class BossState_RAILGUN_DEAD(BossState):
    state = Boss003State.RAILGUN_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()

        self.parent.rail_gun_sprite.set_sprite(11, 14, 100)     
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, )))
        enemy_dialog = EnemyDialog(MaiAnh(Dialog.PAIN))
        current_scene.em.add(enemy_dialog)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 250:
            self.next_state()


class BossState_BALLONS(BossState):
    def __init__(self, parent, balloon_count):
        self.state = [
            Boss003State.BALLOONS_EIGHT,
            Boss003State.BALLOONS_SEVEN,
            Boss003State.BALLOONS_SIX,
            Boss003State.BALLOONS_FIVE,
            Boss003State.BALLOONS_FOUR,
            Boss003State.BALLOONS_THREE,
            Boss003State.BALLOONS_THREE,
            Boss003State.BALLOONS_ONE,
        ][balloon_count - 1]
        super().__init__(parent)
        self.balloon_count = balloon_count 

    def start(self):
        super().start()
        if self.balloon_count == 8:
            self.parent.hitboxes = []
            self.parent.hitbox_offsets = []
            self.parent.add_hitbox((0,0,60,35),Vector2(-30, -56))
        start = 8 - self.balloon_count
        self.parent.ship_sprite.set_sprite(start, start+1)
        self.health = self.parent.health_by_state[self.state]

    def end(self):
        super().end()
        if self.balloon_count == 8:
            offset = Vector2(20, -30)
        elif self.balloon_count == 7:
            offset = Vector2(-20, -30)
        elif self.balloon_count == 6:
            offset = Vector2(20, -30)
        elif self.balloon_count == 5:
            offset = Vector2(-20, -30)
        elif self.balloon_count == 4:
            offset = Vector2(20, -30)
        elif self.balloon_count == 3:
            offset = Vector2(-20, -30)
        elif self.balloon_count == 2:
            offset = Vector2(20, -30)
        elif self.balloon_count == 1:
            offset = Vector2(-20, -30)
        current_scene.em.add(ExplosionSmallFollow(self.parent, offset))
        current_app.mixer.play("explosion sm")

 
class BossState_BALLOONS_DEAD(BossState):
    state = Boss003State.BALLOONS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.ship_sprite.set_sprite(8, 9)
        self.stop_path()
        self.heading = Vector2(0, 1)
        self.velocity = 0.2
        # current_app.mixer.play("explosion sm")
        # current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, 0)))
        enemy_dialog = EnemyDialog(MaiAnh(Dialog.DYING))
        current_scene.em.add(enemy_dialog)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 350:
            current_scene.em.add(ExplosionMedium(self.pos))
            current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-35,35), random.randint(-35,35))))
            current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-35,35), random.randint(-35,35))))
            current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-35,35), random.randint(-35,35))))
            current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-35,35), random.randint(-35,35))))
            current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-35,35), random.randint(-35,35))))
            current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-35,35), random.randint(-35,35))))
            current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-65,65), random.randint(-65,65))))
            current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-65,65), random.randint(-65,65))))
            current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-65,65), random.randint(-65,65))))
            current_app.mixer.play("explosion md")

            self.killed()
            current_scene.enemies_killed += 1
            self.next_state()


class BossState_DEAD(BossState):
    state = Boss003State.DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 4550:
            current_scene.change_state(LevelState.WON)
            self.delete()


class Boss003(Boss):


    state_enum = Boss003State

    def __init__(self):
        super().__init__()

        self.sprite_offset = SPRITE_OFFSET

        self.add_hitbox((0,0,50,21),Vector2(-25, -12))
        self.add_hitbox((0,0,32,14),Vector2(-16, 8))

        self.gun_points = [
            Vector2(0, 17),
            Vector2(6, -3),
            ]

        self.ship_sprite = Boss003Ship()
        self.em.add(self.ship_sprite)
        self.laser_pod_sprite = Boss003LaserPod()
        self.em.add(self.laser_pod_sprite)
        self.rail_gun_sprite = Boss003RailGun()
        self.em.add(self.rail_gun_sprite)

        self.laser_dots = []
        c = 6
        for i in range(c):
            laser_dot = Boss003LaserDot()
            laser_dot.frame_index = int((18/c) * i)
            self.laser_dots.append(laser_dot)
            self.em.add(laser_dot)



        # self.laser_sprite = Boss001Laser()
        # self.em.add(self.laser_sprite)
        # self.launchers_sprite = Boss003Launchers()
        # self.em.add(self.launchers_sprite)

        self.states = {
            Boss003State.STARTING: BossState_STARTING(self),
            Boss003State.LASERS_STARTING: BossState_LASERSSTARTING(self),
            Boss003State.LASERS_SIX: BossState_LASERS_FIRING(self, 6),
            Boss003State.LASERS_FIVE: BossState_LASERS_FIRING(self, 5),
            Boss003State.LASERS_FOUR: BossState_LASERS_FIRING(self, 4),
            Boss003State.LASERS_THREE: BossState_LASERS_FIRING(self, 3),
            Boss003State.LASERS_TWO: BossState_LASERS_FIRING(self, 2),
            Boss003State.LASERS_ONE: BossState_LASERS_FIRING(self, 1),
            Boss003State.LASERS_DEAD: BossState_LASERS_DEAD(self),
            Boss003State.RAILGUN_LOADING: BossState_RAILGUN_LOADING(self),
            Boss003State.RAILGUN_FIRING: BossState_RAILGUN_FIRING(self),
            Boss003State.RAILGUN_DEAD: BossState_RAILGUN_DEAD(self),
            Boss003State.BALLOONS_EIGHT: BossState_BALLONS(self, 8),
            Boss003State.BALLOONS_SEVEN: BossState_BALLONS(self, 7),
            Boss003State.BALLOONS_SIX: BossState_BALLONS(self, 6),
            Boss003State.BALLOONS_FIVE: BossState_BALLONS(self, 5),
            Boss003State.BALLOONS_FOUR: BossState_BALLONS(self, 4),
            Boss003State.BALLOONS_THREE: BossState_BALLONS(self, 3),
            Boss003State.BALLOONS_TWO: BossState_BALLONS(self, 2),
            Boss003State.BALLOONS_ONE: BossState_BALLONS(self, 1),
            Boss003State.BALLOONS_DEAD: BossState_BALLOONS_DEAD(self),
            Boss003State.DEAD: BossState_DEAD(self),
        }

        self.health_by_state = {
            Boss003State.STARTING: -1,
            Boss003State.LASERS_STARTING: -1,
            Boss003State.LASERS_SIX: 1,
            Boss003State.LASERS_FIVE: 1,
            Boss003State.LASERS_FOUR: 1,
            Boss003State.LASERS_THREE: 1,
            Boss003State.LASERS_TWO: 1,
            Boss003State.LASERS_ONE: 1,
            Boss003State.LASERS_DEAD: -1,
            Boss003State.RAILGUN_LOADING: -1,
            Boss003State.RAILGUN_FIRING: 1,
            Boss003State.RAILGUN_DEAD: -1,
            Boss003State.BALLOONS_EIGHT: 1,
            Boss003State.BALLOONS_SEVEN: 1,
            Boss003State.BALLOONS_SIX: 1,
            Boss003State.BALLOONS_FIVE: 1,
            Boss003State.BALLOONS_FOUR: 1,
            Boss003State.BALLOONS_THREE: 1,
            Boss003State.BALLOONS_TWO: 1,
            Boss003State.BALLOONS_ONE: 1,
            Boss003State.BALLOONS_DEAD: -1,
            Boss003State.DEAD: -1,
        }

        self.start(Boss003State.STARTING)
