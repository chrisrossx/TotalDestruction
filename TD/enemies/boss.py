from enum import Enum
import pygame 

from TD.particles.explosions import ExplosionMedium, ExplosionSmall, ExplosionSmallFollow
from TD.scenes.level.level_state import LevelState
import random 
from pygame import Vector2

from TD.entity import EntityVectorMovement, EntityType, Entity
from TD.assetmanager import asset_manager
from TD.paths import PathFollower
from TD.debuging import game_debugger
from TD import current_app, current_scene
from TD.particles.spoofs import SpoofHitFollow

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
    # ALMOST_DEAD = 9
    # DIEING = 10



class Boss001Laser(Entity):
    def __init__(self):
        super().__init__()
        self.sprite_offset = SPRITE_OFFSET

    def on_finished_callback(self, entity):
        pass


class Boss001Launchers(Entity):
    def __init__(self):
        super().__init__()
        self.sprite_offset = SPRITE_OFFSET

    def on_finished_callback(self, entity):
        pass


class BossState:
    state = None
    def __init__(self, parent):
        self.parent = parent 
        self.total_elapsed = 0

    @property
    def laser_sprite(self):
        return self.parent.laser_sprite 

    @property 
    def launchers_sprite(self):
        return self.parent.launchers_sprite
        
    def set_laser_sprite(self, start_frame, end_frame, duration=-1, loop_end=-1):
        self.parent.laser_sprite.frames = asset_manager.sprites["Boss 001 laser"][start_frame:end_frame]
        self.parent.laser_sprite.frame_index = 0
        self.parent.laser_sprite.frame_elapsed = 0
        self.parent.laser_sprite.frame_duration = duration
        self.parent.laser_sprite.frame_loop_start = 0
        self.parent.laser_sprite.frame_loop_count = 0 
        self.parent.laser_sprite.frame_loop_end = loop_end 

    def set_launchers_sprite(self, start_frame, end_frame, duration=-1, loop_end=-1):
        self.parent.launchers_sprite.frames = asset_manager.sprites["Boss 001 launchers"][start_frame:end_frame]
        self.parent.launchers_sprite.frame_index = 0
        self.parent.launchers_sprite.frame_elapsed = 0
        self.parent.launchers_sprite.frame_duration = duration
        self.parent.launchers_sprite.frame_loop_start = 0
        self.parent.launchers_sprite.frame_loop_count = 0 
        self.parent.launchers_sprite.frame_loop_end = loop_end 

    def set_parent_sprite(self, start_frame, end_frame, duration=-1, loop_end=-1):
        self.parent.frames = asset_manager.sprites["Boss 001"][start_frame:end_frame]
        self.parent.frame_index = 0
        self.parent.frame_elapsed = 0
        self.parent.frame_duration = duration
        self.parent.frame_loop_start = 0
        self.parent.frame_loop_count = 0 
        self.parent.frame_loop_end = loop_end 

    @property
    def heading(self):
        return self.parent.heading 

    @heading.setter
    def heading(self, value):
        self.parent.heading = value

    @property
    def velocity(self):
        return self.parent.velocity
    
    @velocity.setter
    def velocity(self, value):
        self.parent.velocity = value 

    @property
    def next_state(self):
        return self.parent.next_state

    @property
    def running_path(self):
        return self.parent.running_path 
    
    @running_path.setter
    def running_path(self, value):
        self.parent.running_path = value 

    @property
    def path(self):
        return self.parent.path 

    def end(self):
        pass

    def draw(self, elapsed, surface):
        pass

    def tick(self, elapsed):
        self.total_elapsed += elapsed

    def start(self):
        self.total_elapsed = 0
        self.health = self.parent.health_by_state[self.state]

    def hit(self, bullet):
        "Called when PlayerBullet Hits Boss"

        if self.health > 0:
            total_damage = bullet.damage
            if total_damage > self.health:
                total_damage = self.health

            self.parent.health -= total_damage    
            self.health -= bullet.damage
            
            if self.health <= 0:
                self.next_state()

    @property
    def killed(self):
        return self.parent.killed

    @property
    def pos(self):
        return self.parent.pos 

    @pos.setter
    def pos(self, value):
        self.parent.pos = value 

    @property
    def start_path(self, index=None):
        self.parent.start_path(index) 
    
    @property
    def stop_path(self):
        return self.parent.stop_path

    def collision(self):
        "Called when Player Collides with Boss"
        return False 



class BossState_STARTING(BossState):
    state = Boss001State.STARTING
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_parent_sprite(0, 3, 100)
        self.heading = Vector2(-1, 0)
        self.velocity = 0.11
        self.set_laser_sprite(0, 1)
        self.set_launchers_sprite(0, 1)
        self.parent.launchers_sprite.enabled = False

        # self.parent.pos.x = 901

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.parent.pos.x <= 900:
            self.next_state()

class BossState_LASER_STARTING(BossState):
    state = Boss001State.LASER_STARTING
    def __init__(self, parent) -> None:
        self.parent = parent 

    def start(self):
        super().start()
        self.parent.velocity = 0
        self.set_laser_sprite(1, 4, 350, 1)
        current_app.mixer.play("boss laser 001")
        self.laser_sprite.callback_animation_finished.append(self.on_animation_finished)

    def on_animation_finished(self, sender):
        self.next_state()

    def end(self):
        super().end()
        self.laser_sprite.callback_animation_finished.remove(self.on_animation_finished)        


class BossState_LASER_ALL(BossState):
    state = Boss001State.LASER_ALL
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.start_path()
        self.set_laser_sprite(3, 4)
            

class BossState_LASER_TWO(BossState):
    state = Boss001State.LASER_TWO
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-16, 2)))

        super().start()
        self.set_laser_sprite(4, 8, 100)
        
        #TEMP TO KILL BOSS FAST
        # current_scene.em.add(ExplosionMedium(self.pos + Vector2(random.randint(-65,65), random.randint(-65,65))))
        # current_app.mixer.play("explosion md")
        # current_scene.change_state(LevelState.WON)
        # self.killed()
    
class BossState_LASER_ONE(BossState):
    state = Boss001State.LASER_ONE
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_laser_sprite(8, 12, 100)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, 2)))


class BossState_LASER_DEAD(BossState):
    state = Boss001State.LASER_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.stop_path()
        self.set_laser_sprite(12, 16, 100)

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
        self.set_laser_sprite(16, 17)
        self.set_launchers_sprite(0, 7, 120, 1)
        self.launchers_sprite.enabled = True
        self.launchers_sprite.callback_animation_finished.append(self.on_animation_finished)
        current_app.mixer.play("boss servo 002")

    def on_animation_finished(self, sender):
        self.next_state()

    def tick(self, elapsed):
        super().tick(elapsed)

    def end(self):
        super().end()
        self.launchers_sprite.callback_animation_finished.remove(self.on_animation_finished)


class BossState_LAUNCHERS_ALL(BossState):
    state = Boss001State.LAUNCHERS_ALL
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.start_path("boss 001 launchers")
        self.set_launchers_sprite(6, 7)

    # def tick(self, elapsed):
    #     super().tick(elapsed)
    #     if self.total_elapsed >= 2500:
    #         self.next_state()


class BossState_LAUNCHERS_ONE(BossState):
    state = Boss001State.LAUNCHERS_ONE
    sprite_start = 7
    sprite_end = 8
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_launchers_sprite(self.sprite_start, self.sprite_end)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-27, -12)))


    # def tick(self, elapsed):
    #     super().tick(elapsed)
    #     if self.total_elapsed >= 2500:
    #         self.next_state()


class BossState_LAUNCHERS_DEAD(BossState):
    state = Boss001State.LAUNCHERS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_launchers_sprite(8, 9)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(27, -12)))

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 250:
            self.next_state()


class BossState_THRUSTERS_ALL(BossState):
    state = Boss001State.THRUSTERS_ALL
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        # self.set_launchers_sprite(8, 9)

    # def tick(self, elapsed):
    #     super().tick(elapsed)
    #     if self.total_elapsed >= 2500:
    #         self.next_state()
    #         # print("finished")


class BossState_THRUSTERS_TWO(BossState):
    state = Boss001State.THRUSTERS_TWO
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_parent_sprite(3, 6, 100)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(-27, 12)))


class BossState_THRUSTERS_ONE(BossState):
    state = Boss001State.THRUSTERS_ONE
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_parent_sprite(6, 9, 100)
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(27, 12)))


class BossState_THRUSTERS_DEAD(BossState):
    state = Boss001State.THRUSTERS_DEAD
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_parent_sprite(9, 12, 100)
        self.stop_path()
        self.heading = Vector2(0, 1)
        self.velocity = 0.2
        current_app.mixer.play("explosion sm")
        current_scene.em.add(ExplosionSmallFollow(self.parent, Vector2(0, 22)))
        # pygame.draw.circle(surface, (255,0,255),self.pos + Vector2(0,22), 5, 1)

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
            current_scene.change_state(LevelState.WON)
            self.killed()
            current_scene.enemies_killed += 1
            # print("DEAD!")


class Boss001(EntityVectorMovement):
    def __init__(self):
        super().__init__()
        self.type = EntityType.BOSS

        self.add_hitbox((0,0,64,30),Vector2(-32, -10))
        self.add_hitbox((0,0,30,15),Vector2(-15, -25))

        self.health = 0

        # self.frames = asset_manager.sprites["Boss 001"][3:6]
        # print(len(self.frames))
        # self.frame_duration = 100
        self.sprite_offset = SPRITE_OFFSET
        self.pos = Vector2(1024+60, 300)
        # self.po
        self.velocity = 0
        self.laser_sprite = Boss001Laser()
        self.launchers_sprite = Boss001Launchers()
        # self.main_sprite = 

        self.path = PathFollower("boss 001 lasers")
        self.path.on_end_of_path.append(self.on_end_of_path)
        self.path.velocity = 0.11
        self.running_path = False 

        self.state = Boss001State.STARTING
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
        }

        self.health_by_state = {
            Boss001State.STARTING: -1,
            Boss001State.LASER_STARTING: -1,
            Boss001State.LASER_ALL: 5,
            Boss001State.LASER_TWO: 5,
            Boss001State.LASER_ONE: 5,
            Boss001State.LASER_DEAD: -1,
            Boss001State.LAUNCHERS_LOADING: -1,
            Boss001State.LAUNCHERS_ALL: 5,
            Boss001State.LAUNCHERS_ONE: 5,
            Boss001State.LAUNCHERS_DEAD: -1,
            Boss001State.THRUSTERS_ALL: 5,
            Boss001State.THRUSTERS_TWO: 5,
            Boss001State.THRUSTERS_ONE: 5,
            Boss001State.THRUSTERS_DEAD: -1,
        }
        for h in self.health_by_state.values():
            if h > 0:
                self.health += h

        # self.state = Boss001State.LASER_DEAD
        # self.states[self.state].set_parent_sprite(0,3, 100)
        # self.pos = Vector2(1000,300)

        self.states[self.state].start()

    def hit(self, bullet):
        l = (bullet.pos.lerp(self.pos, 0.8) - bullet.pos) * -1
        current_scene.em.add(SpoofHitFollow(self, l))
        current_app.mixer.play("enemy hit")
        self.states[self.state].hit(bullet)

    def killed(self):
        self.delete()

    def collision(self):
        """Collision with Player"""
        pass

    def on_end_of_path(self):
        # self.path.distance = 0
        self.path.loop()
    
    def start_path(self, index=None):
        if index:
            self.path.set_new_path(index)
            self.path.distance = 0
            self.path.velocity = 0.11
        self.running_path = True 
        self.pos = self.path.pos

    def stop_path(self):
        self.runnin_path = False
        self.path.velocity = 0
        self.pos = self.path.pos.copy()

    def next_state(self):
        self.states[self.state].end()
        self.state = Boss001State(self.state.value + 1)
        self.states[self.state].start()

    def tick(self, elapsed):
        self.states[self.state].tick(elapsed)
        super().tick(elapsed)
        self.laser_sprite.tick(elapsed)
        self.laser_sprite.pos = self.pos
        self.launchers_sprite.tick(elapsed)
        self.launchers_sprite.pos = self.pos 

        if not self.deleted and self.running_path:
            self.path.tick(elapsed)

    def draw(self, elapsed, surface):
        self.states[self.state].draw(elapsed, surface)
        super().draw(elapsed, surface)
        self.laser_sprite.draw(elapsed, surface)
        self.launchers_sprite.draw(elapsed, surface)


        # pygame.draw.circle(surface, (255,0,255),self.pos + Vector2(-27,12), 5, 1)
        # pygame.draw.circle(surface, (255,0,255),self.pos + Vector2(27,12), 5, 1)
        # pygame.draw.circle(surface, (255,0,255),self.pos + Vector2(0,22), 5, 1)


        if game_debugger.show_paths:
            self.path.draw(elapsed, surface)
        if game_debugger.show_hitboxes:
            line = asset_manager.fonts["xxs"].render("[  H={}  ]".format(self.health), True, (255,0,0))
            pos = self.pos + self.sprite_offset
            pos.y -= line.get_rect().h
            surface.blit(line, pos)

            line = asset_manager.fonts["xxs"].render("[  S={}, S={}  ]".format(self.state.name, self.states[self.state].health), True, (255,0,0))
            pos = self.pos + self.sprite_offset
            pos.y -= line.get_rect().h
            pos.y -= 20
            surface.blit(line, pos)
