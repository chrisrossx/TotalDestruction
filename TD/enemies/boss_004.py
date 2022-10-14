from enum import Enum
import pygame 

from TD.particles.explosions import ExplosionMedium, ExplosionSmall, ExplosionSmallFollow
from TD.scenes.level.level_state import LevelState
import random 
from pygame import Vector2

from TD.assetmanager import asset_manager
from TD import current_app, current_scene
from TD.characters import Dialog, MaiAnh, Christopher
from TD.scenes.level.dialog import EnemyDialog
from TD.enemies.boss import BossState, Boss, BossLayeredSprite
from TD.guns.boss_004 import GunBoss004LargeLaser, GunBoss004Level1Missle001Left, GunBoss004Level1Missle001Right


SPRITE_OFFSET = Vector2(-64, -64) 
LASER_DOT_RATE = 100

class Boss004State(Enum):
    STARTING = 0
    OPENING_BODY = 1
    LASER_STARTING = 2
    LASER_FIRING = 3
    LASER_DEAD = 4
    CLOSING_BODY = 5
    LAUNCHERS_LOADING = 6
    LAUNCHERS_TWO = 7
    LAUNCHERS_ONE = 8
    LAUNCHERS_DEAD = 9
    THRUSTERS_TWO = 10
    THRUSTERS_ONE = 11
    THRUSTERS_DEAD = 12
    DEAD = 13

class Boss004Top(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprite_offset = SPRITE_OFFSET.copy()
        self.sprites = asset_manager.sprites["Boss 004 top"]

    def draw(self, elapsed, surface):
        return super().draw(elapsed, surface)

class Boss004Laser(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 004 laser"]
        self.sprite_offset = SPRITE_OFFSET.copy()
        # self.sprite_offset = Vector2(19, 65) + SPRITE_OFFSET

class Boss004Missiles(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 004 missiles"]
        self.sprite_offset = SPRITE_OFFSET.copy()
        # self.sprite_offset = Vector2(25, 44) + SPRITE_OFFSET

class Boss004Bottom(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 004 bottom"]
        self.sprite_offset = SPRITE_OFFSET.copy()
        # self.sprite_offset = Vector2(19, 71) + SPRITE_OFFSET
        # self.laser_on = False 
        # self.laser_dead = False 

    # def set_sprite(self, start_frame, end_frame, duration=-1, loop_end=-1):
    #     self.frames = self.sprites[start_frame:end_frame]
    #     for i in range(8):
    #         self.frames.append(pygame.Surface((1,1), pygame.SRCALPHA))
    #     self.frame_duration = duration

class BossState_STARTING(BossState):
    state = Boss004State.STARTING
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.ship_top.set_sprite(0, 1)
        self.parent.ship_bottom.set_sprite(0, 3, 120)
        self.parent.ship_laser.set_sprite(0, 1)
        self.parent.ship_missiles.set_sprite(0, 1)
        # self.parent.ship_sprite.set_sprite(0, 1)
        self.heading = Vector2(-1, 0)
        self.velocity = 0.11
        # self.parent.laser_pod_sprite.set_sprite(0, 1)
        # self.parent.rail_gun_sprite.set_sprite(0, 1)
            
    def tick(self, elapsed):
        super().tick(elapsed)
        if self.parent.pos.x <= 900:
            enemy_dialog = EnemyDialog(Christopher(Dialog.THREAT))
            current_scene.em.add(enemy_dialog)
            self.next_state()



class BossState_OPENINGBODY(BossState):
    state = Boss004State.OPENING_BODY
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.elapsed = 0 

    def tick(self, elapsed):
        super().tick(elapsed)
        velocity = 0.01
        self.parent.ship_top.sprite_offset.y -= velocity * elapsed
        self.parent.ship_missiles.sprite_offset.y = self.parent.ship_top.sprite_offset.y
        self.parent.ship_bottom.sprite_offset.y += velocity * elapsed
        y = 7 
        if self.parent.ship_top.sprite_offset.y <= -64 - y:
            self.parent.ship_top.sprite_offset.y = -64 - y
            self.parent.ship_missiles.sprite_offset.y = self.parent.ship_top.sprite_offset.y
            self.parent.ship_bottom.sprite_offset.y = -64 + y
            self.parent.hitbox_offsets[0].y -= y
            self.parent.hitbox_offsets[1].y += y
            self.next_state()

    def start(self):
        super().start()
        self.parent.velocity = 0
        current_app.mixer.play("boss servo 002")

class BossState_LASER_STARTING(BossState):
    state = Boss004State.LASER_STARTING
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        current_app.mixer.play("boss laser 001")
        self.parent.ship_laser.set_sprite(1, 7, 120, 1)
        self.parent.ship_laser.callback_animation_finished.append(self.on_animation_finished)

    def on_animation_finished(self, sender):
        self.next_state()

    def tick(self, elapsed):
        super().tick(elapsed)

    def end(self):
        super().end()
        self.parent.ship_laser.callback_animation_finished.remove(self.on_animation_finished)



class BossState_LASER_FIRING(BossState):
    state = Boss004State.LASER_FIRING
    def __init__(self, parent):
        super().__init__(parent)
        self.gun = GunBoss004LargeLaser(self.parent)

    def start(self):
        super().start()
        self.parent.start_path("boss 001 lasers")
        self.parent.start_path()
        self.parent.ship_laser.set_sprite(6, 7)

    def end(self):
        super().end()
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, 20)))

  
class BossState_LASER_DEAD(BossState):
    state = Boss004State.LASER_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
       
        self.stop_path()
        
        self.parent.ship_laser.set_sprite(7, 10, 200)

        #lerp vars
        self.distance = 0
        self.pos_start = self.pos.copy()
        self.pos_finish = Vector2(900, 300)
        # Normal Rate is 0.1 pixels per 0.001seconds
        # So if distance is 800 pixels
        # 0.1 at 800 pixels would take 8 seconds 8000
        self.lerp_rate = (1 / self.pos_start.distance_to(self.pos_finish)) * 0.1
        
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(5, 0)))
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-8, 4)))
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, -2)))

        enemy_dialog = EnemyDialog(Christopher(Dialog.PAIN))
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

class BossState_CLOSINGBODY(BossState):
    state = Boss004State.CLOSING_BODY
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.elapsed = 0 

    def tick(self, elapsed):
        super().tick(elapsed)
        velocity = 0.01
        self.parent.ship_top.sprite_offset.y += velocity * elapsed
        self.parent.ship_missiles.sprite_offset.y = self.parent.ship_top.sprite_offset.y
        self.parent.ship_bottom.sprite_offset.y -= velocity * elapsed
        if self.parent.ship_top.sprite_offset.y >= -64:
            self.parent.ship_top.sprite_offset.y = -64
            self.parent.ship_missiles.sprite_offset.y = self.parent.ship_top.sprite_offset.y
            self.parent.ship_bottom.sprite_offset.y = -64
            y = 7
            self.parent.hitbox_offsets[0].y += y
            self.parent.hitbox_offsets[1].y -= y
            self.next_state()

    def start(self):
        super().start()
        self.parent.velocity = 0
        current_app.mixer.play("boss servo 002")

class BossState_LAUNCHERS_LOADING(BossState):
    state = Boss004State.LAUNCHERS_LOADING
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.ship_missiles.set_sprite(1, 7, 120, 1)
        self.parent.ship_missiles.callback_animation_finished.append(self.on_animation_finished)
        current_app.mixer.play("boss servo 002")

    def on_animation_finished(self, sender):
        self.next_state()

    def tick(self, elapsed):
        super().tick(elapsed)

    def end(self):
        super().end()
        self.parent.ship_missiles.callback_animation_finished.remove(self.on_animation_finished)


class BossState_LAUNCHERS_TWO(BossState):
    state = Boss004State.LAUNCHERS_TWO
    def __init__(self, parent):
        super().__init__(parent)
        self.gun = GunBoss004Level1Missle001Left(self.parent)

    def start(self):
        super().start()
        self.parent.start_path("boss 001 launchers")
        self.parent.ship_missiles.set_sprite(6, 7)


class BossState_LAUNCHERS_ONE(BossState):
    state = Boss004State.LAUNCHERS_ONE
    def __init__(self, parent):
        super().__init__(parent)
        self.gun = GunBoss004Level1Missle001Right(self.parent)

    def start(self):
        super().start()
        self.parent.ship_missiles.set_sprite(7, 10, 120)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-8, -7)))


class BossState_LAUNCHERS_DEAD(BossState):
    state = Boss004State.LAUNCHERS_DEAD
    def __init__(self, parent):
        super().__init__(parent)


    def start(self):
        super().start()
        self.parent.ship_missiles.set_sprite(10, 13, 120)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(8, -7)))
        enemy_dialog = EnemyDialog(Christopher(Dialog.PAIN))
        current_scene.em.add(enemy_dialog)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 250:
            self.next_state()

class BossState_THRUSTERS_TWO(BossState):
    state = Boss004State.THRUSTERS_TWO
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True

    def start(self):
        super().start()

class BossState_THRUSTERS_ONE(BossState):
    state = Boss004State.THRUSTERS_ONE
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True

    def start(self):
        super().start()
        self.parent.ship_bottom.set_sprite(3, 6, 120)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-17, 19)))


class BossState_THRUSTERS_DEAD(BossState):
    state = Boss004State.THRUSTERS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.ship_bottom.set_sprite(6, 9, 120)
        self.parent.ship_top.set_sprite(1, 2)
        self.stop_path()
        self.heading = Vector2(0, 1)
        self.velocity = 0.2
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(17, 19)))
        enemy_dialog = EnemyDialog(Christopher(Dialog.DYING))
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
    state = Boss004State.DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 4550:
            current_scene.change_state(LevelState.WON)
            self.delete()


class Boss004(Boss):


    state_enum = Boss004State

    def __init__(self):
        super().__init__()

        self.sprite_offset = SPRITE_OFFSET

        self.add_hitbox((0,0,36,20),Vector2(-18, -20))
        self.add_hitbox((0,0,36,20),Vector2(-18, 0))
        self.add_hitbox((0,0,24,20), Vector2(-12,-10))

        self.gun_points = [
            Vector2(0, 3),
            Vector2(-8, -7),
            Vector2(8, -7),
            ]

        self.ship_top = Boss004Top()
        self.ship_bottom = Boss004Bottom()
        self.ship_missiles = Boss004Missiles()
        self.ship_laser = Boss004Laser()
        self.em.add(self.ship_laser)
        self.em.add(self.ship_bottom)
        self.em.add(self.ship_top)
        self.em.add(self.ship_missiles)

        self.states = {
            Boss004State.STARTING: BossState_STARTING(self),
            Boss004State.OPENING_BODY: BossState_OPENINGBODY(self),
            Boss004State.LASER_STARTING: BossState_LASER_STARTING(self),
            Boss004State.LASER_FIRING: BossState_LASER_FIRING(self),
            Boss004State.LASER_DEAD: BossState_LASER_DEAD(self),
            Boss004State.CLOSING_BODY: BossState_CLOSINGBODY(self),
            Boss004State.LAUNCHERS_LOADING: BossState_LAUNCHERS_LOADING(self),
            Boss004State.LAUNCHERS_TWO: BossState_LAUNCHERS_TWO(self),
            Boss004State.LAUNCHERS_ONE: BossState_LAUNCHERS_ONE(self),
            Boss004State.LAUNCHERS_DEAD: BossState_LAUNCHERS_DEAD(self),
            Boss004State.THRUSTERS_TWO: BossState_THRUSTERS_TWO(self),
            Boss004State.THRUSTERS_ONE: BossState_THRUSTERS_ONE(self),
            Boss004State.THRUSTERS_DEAD: BossState_THRUSTERS_DEAD(self),
            Boss004State.DEAD: BossState_DEAD(self),
        }

        self.health_by_state = {
            Boss004State.STARTING: -1,
            Boss004State.OPENING_BODY: -1,
            Boss004State.LASER_STARTING: -1,
            Boss004State.LASER_FIRING: 35,
            Boss004State.LASER_DEAD: -1,
            Boss004State.CLOSING_BODY: -1,
            Boss004State.LAUNCHERS_LOADING: -1,
            Boss004State.LAUNCHERS_TWO: 15,
            Boss004State.LAUNCHERS_ONE: 15, 
            Boss004State.LAUNCHERS_DEAD: -1,
            Boss004State.THRUSTERS_TWO: 15,
            Boss004State.THRUSTERS_ONE: 15,
            Boss004State.THRUSTERS_DEAD: -1,
            Boss004State.DEAD: -1,
        }

        self.start(Boss004State.STARTING)
