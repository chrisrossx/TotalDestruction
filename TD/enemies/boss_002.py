from enum import Enum
import pygame 

from TD.particles.explosions import ExplosionMedium, ExplosionSmall, ExplosionSmallFollow
from TD.scenes.level.level_state import LevelState
import random 
from pygame import Vector2

from TD.assetmanager import asset_manager
from TD import current_app, current_scene
from TD.characters import Dialog, Sawyer
from TD.scenes.level.dialog import EnemyDialog
from TD.enemies.boss import BossState, Boss, BossLayeredSprite
from TD.guns.boss_002 import GunBoss002RightGun, GunBoss002LeftGun, GunBoss002Level1Missle001Left, GunBoss002Level1Missle001Right


SPRITE_OFFSET = Vector2(-64,-70) 

class Boss002State(Enum):
    STARTING = 0
    GUNS_STARTING = 1
    GUNS_ALL = 2
    GUNS_ONE = 3
    GUNS_DEAD = 4
    LAUNCHERS_LOADING = 5
    LAUNCHERS_ALL = 6
    LAUNCHERS_ONE = 7
    LAUNCHERS_DEAD = 8
    THRUSTERS_ALL = 9
    THRUSTERS_DEAD = 10
    DEAD = 11


class Boss002Ship(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprite_offset = SPRITE_OFFSET
        self.sprites = asset_manager.sprites["Boss 002"]

    def draw(self, elapsed, surface):
        return super().draw(elapsed, surface)

class Boss002Guns(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 002 guns"]
        self.sprite_offset = SPRITE_OFFSET

class Boss002Launchers(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 002 launchers"]
        self.sprite_offset = SPRITE_OFFSET

class BossState_STARTING(BossState):
    state = Boss002State.STARTING
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.ship_sprite.set_sprite(0, 3, 100)
        self.heading = Vector2(-1, 0)
        self.velocity = 0.11
        # self.parent.laser_sprite.set_sprite(0, 1)
        self.parent.launchers_sprite.set_sprite(0, 1)
        self.parent.guns_sprite.set_sprite(1, 7, 190)
        self.parent.guns_sprite.enabled = False 
        # self.parent.launchers_sprite.enabled = False



    def tick(self, elapsed):
        super().tick(elapsed)
        if self.parent.pos.x <= 900:
            enemy_dialog = EnemyDialog(Sawyer(Dialog.THREAT))
            current_scene.em.add(enemy_dialog)
            self.next_state()



class BossState_GUNSSTARTING(BossState):
    state = Boss002State.GUNS_STARTING
    def __init__(self, parent) -> None:
        super().__init__(parent)
        # self.parent = parent 

    def start(self):
        super().start()
        self.parent.velocity = 0
        self.parent.guns_sprite.set_sprite(1, 7, 190, 1)
        current_app.mixer.play("boss laser 001")
        self.parent.guns_sprite.callback_animation_finished.append(self.on_animation_finished)
        self.parent.guns_sprite.enabled = True 

    def on_animation_finished(self, sender):
        self.next_state()

    def end(self):
        super().end()
        self.parent.guns_sprite.callback_animation_finished.remove(self.on_animation_finished)        


class BossState_GUNS_ALL(BossState):
    state = Boss002State.GUNS_ALL
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True
        self.gun = GunBoss002RightGun(self.parent)

    def start(self):
        super().start()
        self.parent.start_path("boss 001 lasers")
        self.parent.start_path()
        self.parent.guns_sprite.set_sprite(6, 7)
            

class BossState_GUNS_ONE(BossState):
    state = Boss002State.GUNS_ONE
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True
        self.gun = GunBoss002LeftGun(self.parent)

    def start(self):
        super().start()
        self.parent.guns_sprite.set_sprite(7, 10, 200)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(17, 12)))


class BossState_GUNS_DEAD(BossState):
    state = Boss002State.GUNS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.stop_path()
        self.parent.guns_sprite.set_sprite(10, 13, 200)

        #lerp vars
        self.distance = 0
        self.pos_start = self.pos.copy()
        self.pos_finish = Vector2(900,300)
        # Normal Rate is 0.1 pixels per 0.001seconds
        # So if distance is 800 pixels
        # 0.1 at 800 pixels would take 8 seconds 8000
        self.lerp_rate = (1 / self.pos_start.distance_to(self.pos_finish)) * 0.1
        
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-17, 12)))

        enemy_dialog = EnemyDialog(Sawyer(Dialog.PAIN))
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
      

class BossState_LAUNCHERS_LOADING(BossState):
    state = Boss002State.LAUNCHERS_LOADING
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
                # self.parent.launchers_sprite.set_sprite(1, 10, 120, 10)

        self.parent.guns_sprite.set_sprite(13, 14)
        self.parent.launchers_sprite.set_sprite(1, 10, 120, 1)
        self.parent.launchers_sprite.callback_animation_finished.append(self.on_animation_finished)
        current_app.mixer.play("boss servo 002")

    def on_animation_finished(self, sender):
        self.next_state()

    def tick(self, elapsed):
        super().tick(elapsed)

    def end(self):
        super().end()
        self.parent.launchers_sprite.callback_animation_finished.remove(self.on_animation_finished)


class BossState_LAUNCHERS_ALL(BossState):
    state = Boss002State.LAUNCHERS_ALL
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True 
        self.gun = GunBoss002Level1Missle001Right(self.parent)

    def start(self):
        super().start()
        self.parent.start_path("boss 001 launchers")
        self.parent.launchers_sprite.set_sprite(9, 10)


class BossState_LAUNCHERS_ONE(BossState):
    state = Boss002State.LAUNCHERS_ONE
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True
        self.gun = GunBoss002Level1Missle001Left(self.parent)
        # self.gun = GunBoss001Level1Missle001Right(self.parent)

    def start(self):
        super().start()
        self.parent.launchers_sprite.set_sprite(10,13,120)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(12, -15)))


class BossState_LAUNCHERS_DEAD(BossState):
    state = Boss002State.LAUNCHERS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()

        self.parent.launchers_sprite.set_sprite(13, 16, 120)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-12, -15)))
        enemy_dialog = EnemyDialog(Sawyer(Dialog.PAIN))
        current_scene.em.add(enemy_dialog)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 250:
            pass
            self.next_state()
            # print("next")


class BossState_THRUSTERS_ALL(BossState):
    state = Boss002State.THRUSTERS_ALL
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True

    def start(self):
        super().start()
        # self.parent.launchers_sprite.set_sprite(16, 17)
 
class BossState_THRUSTERS_DEAD(BossState):
    state = Boss002State.THRUSTERS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.ship_sprite.set_sprite(6, 9, 100)
        self.stop_path()
        self.heading = Vector2(0, 1)
        self.velocity = 0.2
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, 22)))
        enemy_dialog = EnemyDialog(Sawyer(Dialog.DYING))
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
    state = Boss002State.DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 4550:
            current_scene.change_state(LevelState.WON)
            self.delete()


class Boss002(Boss):


    state_enum = Boss002State

    def __init__(self):
        super().__init__()

        self.sprite_offset = SPRITE_OFFSET

        self.add_hitbox((0,0,60,28),Vector2(-30, -28))
        self.add_hitbox((0,0,24,23),Vector2(-12, 0))

        self.gun_points = [
            Vector2(23, 12),
            Vector2(-23, 12),
            Vector2(15, -20),
            Vector2(-15, -20),
            ]

        self.guns_sprite = Boss002Guns()
        self.em.add(self.guns_sprite)
        self.ship_sprite = Boss002Ship()
        self.em.add(self.ship_sprite)
        # self.laser_sprite = Boss001Laser()
        # self.em.add(self.laser_sprite)
        self.launchers_sprite = Boss002Launchers()
        self.em.add(self.launchers_sprite)

        self.states = {
            Boss002State.STARTING: BossState_STARTING(self),
            Boss002State.GUNS_STARTING: BossState_GUNSSTARTING(self),
            Boss002State.GUNS_ALL: BossState_GUNS_ALL(self),
            Boss002State.GUNS_ONE: BossState_GUNS_ONE(self),
            Boss002State.GUNS_DEAD: BossState_GUNS_DEAD(self),
            Boss002State.LAUNCHERS_LOADING: BossState_LAUNCHERS_LOADING(self),
            Boss002State.LAUNCHERS_ALL: BossState_LAUNCHERS_ALL(self),
            Boss002State.LAUNCHERS_ONE: BossState_LAUNCHERS_ONE(self),
            Boss002State.LAUNCHERS_DEAD: BossState_LAUNCHERS_DEAD(self),
            Boss002State.THRUSTERS_ALL: BossState_THRUSTERS_ALL(self),
            Boss002State.THRUSTERS_DEAD: BossState_THRUSTERS_DEAD(self),
            Boss002State.DEAD: BossState_DEAD(self),
        }

        self.health_by_state = {
            Boss002State.STARTING: -1,
            Boss002State.GUNS_STARTING: -1,
            Boss002State.GUNS_ALL: 25,#25,
            Boss002State.GUNS_ONE: 25,#25,
            Boss002State.GUNS_DEAD: -1,
            Boss002State.LAUNCHERS_LOADING: -1,
            Boss002State.LAUNCHERS_ALL: 30,#25,
            Boss002State.LAUNCHERS_ONE: 30,#25,
            Boss002State.LAUNCHERS_DEAD: -1,
            Boss002State.THRUSTERS_ALL: 30,#15,
            Boss002State.THRUSTERS_DEAD: -1,
            Boss002State.DEAD: -1,
        }

        self.start(Boss002State.STARTING)
