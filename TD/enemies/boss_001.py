from enum import Enum
import pygame 

from TD.particles.explosions import ExplosionMedium, ExplosionSmall, ExplosionSmallFollow
from TD.scenes.level.level_state import LevelState
import random 
from pygame import Vector2

from TD.assetmanager import asset_manager
from TD import current_app, current_scene
from TD.guns.boss_001 import GunBoss001Level1Missle001Left, GunBoss001Level1Missle001Right, GunBoss001Level1Laser001Left, GunBoss001Level1Laser002Center, GunBoss001Level1Laser003Right
from TD.characters import Christopher, Dialog, Elle, MaiAnh, Sawyer
from TD.scenes.level.dialog import EnemyDialog
from TD.enemies.boss import BossState, Boss, BossLayeredSprite


SPRITE_OFFSET = Vector2(-64,-70) 

class Boss001State(Enum):
    STARTING = 0
    LASER_STARTING = 1
    LASER_ALL = 2
    LASER_TWO = 3
    LASER_ONE = 4
    LASER_DEAD = 5
    LAUNCHERS_LOADING = 6
    LAUNCHERS_ALL = 7
    LAUNCHERS_ONE = 8
    LAUNCHERS_DEAD = 9
    THRUSTERS_ALL = 10
    THRUSTERS_TWO = 11
    THRUSTERS_ONE = 12
    THRUSTERS_DEAD = 13
    DEAD = 14
    # ALMOST_DEAD = 9
    # DIEING = 10


class Boss001Ship(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprite_offset = SPRITE_OFFSET
        self.sprites = asset_manager.sprites["Boss 001"]

    def draw(self, elapsed, surface):
        return super().draw(elapsed, surface)

class Boss001Laser(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 001 laser"]
        self.sprite_offset = SPRITE_OFFSET

class Boss001Launchers(BossLayeredSprite):
    def __init__(self):
        super().__init__()
        self.sprites = asset_manager.sprites["Boss 001 launchers"]
        self.sprite_offset = SPRITE_OFFSET

class BossState_STARTING(BossState):
    state = Boss001State.STARTING
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.ship_sprite.set_sprite(0, 3, 100)
        self.heading = Vector2(-1, 0)
        self.velocity = 0.11
        self.parent.laser_sprite.set_sprite(0, 1)
        self.parent.launchers_sprite.set_sprite(0, 1)
        self.parent.launchers_sprite.enabled = False


    def tick(self, elapsed):
        super().tick(elapsed)
        if self.parent.pos.x <= 900:
            enemy_dialog = EnemyDialog(Elle(Dialog.THREAT))
            current_scene.em.add(enemy_dialog)
            self.next_state()

class BossState_LASER_STARTING(BossState):
    state = Boss001State.LASER_STARTING
    def __init__(self, parent) -> None:
        super().__init__(parent)
        # self.parent = parent 

    def start(self):
        super().start()
        self.parent.velocity = 0
        self.parent.laser_sprite.set_sprite(1, 4, 350, 1)
        current_app.mixer.play("boss laser 001")
        self.parent.laser_sprite.callback_animation_finished.append(self.on_animation_finished)

    def on_animation_finished(self, sender):
        self.next_state()

    def end(self):
        super().end()
        self.parent.laser_sprite.callback_animation_finished.remove(self.on_animation_finished)        


class BossState_LASER_ALL(BossState):
    state = Boss001State.LASER_ALL
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True
        self.gun = self.gun = GunBoss001Level1Laser001Left(self.parent)

    def start(self):
        super().start()
        self.parent.start_path("boss 001 lasers")
        self.parent.start_path()
        self.parent.laser_sprite.set_sprite(3, 4)
            

class BossState_LASER_TWO(BossState):
    state = Boss001State.LASER_TWO
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True
        self.gun = self.gun = GunBoss001Level1Laser002Center(self.parent)

    def start(self):
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-16, 2)))

        super().start()
        self.parent.laser_sprite.set_sprite(4, 8, 100)
        

class BossState_LASER_ONE(BossState):
    state = Boss001State.LASER_ONE
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True
        self.gun = self.gun = GunBoss001Level1Laser003Right(self.parent)

    def start(self):
        super().start()
        self.parent.laser_sprite.set_sprite(8, 12, 100)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, 2)))


class BossState_LASER_DEAD(BossState):
    state = Boss001State.LASER_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.stop_path()
        self.parent.laser_sprite.set_sprite(12, 16, 100)

        #lerp vars
        self.distance = 0
        self.pos_start = self.pos.copy()
        self.pos_finish = Vector2(900,300)
        # Normal Rate is 0.1 pixels per 0.001seconds
        # So if distance is 800 pixels
        # 0.1 at 800 pixels would take 8 seconds 8000
        self.lerp_rate = (1 / self.pos_start.distance_to(self.pos_finish)) * 0.1
        
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(16, 2)))

        enemy_dialog = EnemyDialog(Elle(Dialog.PAIN))
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
    state = Boss001State.LAUNCHERS_LOADING
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.laser_sprite.set_sprite(16, 17)
        self.parent.launchers_sprite.set_sprite(0, 7, 120, 1)
        self.parent.launchers_sprite.enabled = True
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
    state = Boss001State.LAUNCHERS_ALL
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True 
        self.gun = GunBoss001Level1Missle001Left(self.parent)

    def start(self):
        super().start()
        self.parent.start_path("boss 001 launchers")
        self.parent.launchers_sprite.set_sprite(6, 7)


class BossState_LAUNCHERS_ONE(BossState):
    state = Boss001State.LAUNCHERS_ONE
    sprite_start = 7
    sprite_end = 8
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True
        self.gun = GunBoss001Level1Missle001Right(self.parent)

    def start(self):
        super().start()
        self.parent.launchers_sprite.set_sprite(self.sprite_start, self.sprite_end)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-27, -12)))


class BossState_LAUNCHERS_DEAD(BossState):
    state = Boss001State.LAUNCHERS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.launchers_sprite.set_sprite(8, 9)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(27, -12)))
        enemy_dialog = EnemyDialog(Elle(Dialog.PAIN))
        current_scene.em.add(enemy_dialog)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 250:
            self.next_state()


class BossState_THRUSTERS_ALL(BossState):
    state = Boss001State.THRUSTERS_ALL
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True

    def start(self):
        super().start()
        # self.set_launchers_sprite(8, 9)

class BossState_THRUSTERS_TWO(BossState):
    state = Boss001State.THRUSTERS_TWO
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True

    def start(self):
        super().start()
        self.parent.ship_sprite.set_sprite(3, 6, 100)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-27, 12)))


class BossState_THRUSTERS_ONE(BossState):
    state = Boss001State.THRUSTERS_ONE
    def __init__(self, parent):
        super().__init__(parent)
        self.drop_coins = True

    def start(self):
        super().start()
        self.parent.ship_sprite.set_sprite(6, 9, 100)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(27, 12)))


class BossState_THRUSTERS_DEAD(BossState):
    state = Boss001State.THRUSTERS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.ship_sprite.set_sprite(9, 12, 100)
        self.stop_path()
        self.heading = Vector2(0, 1)
        self.velocity = 0.2
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, 22)))
        # pygame.draw.circle(surface, (255,0,255),self.pos + Vector2(0,22), 5, 1)
        enemy_dialog = EnemyDialog(Elle(Dialog.DYING))
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
            # current_scene.change_state(LevelState.WON)

            self.killed()
            current_scene.enemies_killed += 1
            self.next_state()

class BossState_DEAD(BossState):
    state = Boss001State.DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 4550:
            current_scene.change_state(LevelState.WON)
            self.delete()


class Boss001(Boss):


    state_enum = Boss001State

    def __init__(self):
        super().__init__()

        self.sprite_offset = SPRITE_OFFSET

        self.add_hitbox((0,0,64,30),Vector2(-32, -10))
        self.add_hitbox((0,0,30,15),Vector2(-15, -25))

        self.gun_points = [
            Vector2(-15, 2),
            Vector2(0, 2),
            Vector2(15, 2),
            Vector2(-32, -25),
            Vector2(27, -25),
            ]

        self.ship_sprite = Boss001Ship()
        self.em.add(self.ship_sprite)
        self.laser_sprite = Boss001Laser()
        self.em.add(self.laser_sprite)
        self.launchers_sprite = Boss001Launchers()
        self.em.add(self.launchers_sprite)

        self.states = {
            Boss001State.STARTING: BossState_STARTING(self),
            Boss001State.LASER_STARTING: BossState_LASER_STARTING(self),
            Boss001State.LASER_ALL: BossState_LASER_ALL(self),
            Boss001State.LASER_TWO: BossState_LASER_TWO(self),
            Boss001State.LASER_ONE: BossState_LASER_ONE(self),
            Boss001State.LASER_DEAD: BossState_LASER_DEAD(self),
            Boss001State.LAUNCHERS_LOADING: BossState_LAUNCHERS_LOADING(self),
            Boss001State.LAUNCHERS_ALL: BossState_LAUNCHERS_ALL(self),
            Boss001State.LAUNCHERS_ONE: BossState_LAUNCHERS_ONE(self),
            Boss001State.LAUNCHERS_DEAD: BossState_LAUNCHERS_DEAD(self),
            Boss001State.THRUSTERS_ALL: BossState_THRUSTERS_ALL(self),
            Boss001State.THRUSTERS_TWO: BossState_THRUSTERS_TWO(self),
            Boss001State.THRUSTERS_ONE: BossState_THRUSTERS_ONE(self),
            Boss001State.THRUSTERS_DEAD: BossState_THRUSTERS_DEAD(self),
            Boss001State.DEAD: BossState_DEAD(self),
        }

        self.health_by_state = {
            Boss001State.STARTING: -1,
            Boss001State.LASER_STARTING: -1,
            Boss001State.LASER_ALL: 25,
            Boss001State.LASER_TWO: 25,
            Boss001State.LASER_ONE: 25,
            Boss001State.LASER_DEAD: -1,
            Boss001State.LAUNCHERS_LOADING: -1,
            Boss001State.LAUNCHERS_ALL: 25,
            Boss001State.LAUNCHERS_ONE: 25,
            Boss001State.LAUNCHERS_DEAD: -1,
            Boss001State.THRUSTERS_ALL: 15,
            Boss001State.THRUSTERS_TWO: 15,
            Boss001State.THRUSTERS_ONE: 15,
            Boss001State.THRUSTERS_DEAD: -1,
            Boss001State.DEAD: -1,
        }

        self.start(Boss001State.STARTING)
