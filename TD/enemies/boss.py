from enum import Enum
from functools import total_ordering
from locale import locale_encoding_alias 

import pygame 
from pygame import Vector2
from blinker import signal, Signal

from TD.entity import EntityVectorMovement, EntityType, Entity
from TD.assetmanager import asset_manager
from TD.paths import PathFollower
from TD.debuging import game_debugger

SPRITE_OFFSET = Vector2(-64,-70) 


class Boss001Laser(Entity):
    def __init__(self):
        super().__init__()
        self.sprite_offset = SPRITE_OFFSET

    def animation_finished_callback(self, entity):
        pass


class Boss001Launchers(Entity):
    def __init__(self):
        super().__init__()
        self.sprite_offset = SPRITE_OFFSET

    def animation_finished_callback(self, entity):
        pass


class BossState:
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


class BossState_STARTING(BossState):
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
    def __init__(self, parent) -> None:
        self.parent = parent 

    def start(self):
        super().start()
        self.parent.start_path()
        self.parent.velocity = 0
        self.set_laser_sprite(1, 4, 350, 1)

        self.parent.laser_sprite.signal_animation_finished.connect(self.on_animation_finished)

    def on_animation_finished(self, sender):
        self.next_state()

    def end(self):
        super().end()
        self.parent.laser_sprite.signal_animation_finished.disconnect(self.on_animation_finished)


class BossState_LASER_ALL(BossState):
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_laser_sprite(3, 4)
    
    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            self.next_state()


class BossState_LASER_TWO(BossState):
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_laser_sprite(4, 8, 100)
    
    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            self.next_state()


class BossState_LASER_ONE(BossState):
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_laser_sprite(8, 12, 100)
    
    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            self.next_state()


class BossState_LASER_DEAD(BossState):
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
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_laser_sprite(16, 17)
        self.set_launchers_sprite(0, 7, 250, 1)
        self.launchers_sprite.enabled = True
        self.launchers_sprite.signal_animation_finished.connect(self.on_animation_finished)

    def on_animation_finished(self, sender):
        self.next_state()

    def tick(self, elapsed):
        super().tick(elapsed)

    def end(self):
        super().end()
        self.launchers_sprite.signal_animation_finished.disconnect(self.on_animation_finished)


class BossState_LAUNCHERS_ALL(BossState):
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.parent.start_path("boss 001 launchers")
        self.set_launchers_sprite(6, 7)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            self.next_state()


class BossState_LAUNCHERS_ONE(BossState):
    sprite_start = 7
    sprite_end = 8
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_launchers_sprite(self.sprite_start, self.sprite_end)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            self.next_state()


class BossState_LAUNCHERS_DEAD(BossState):
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_launchers_sprite(8, 9)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            self.next_state()
            # print("finished")


class BossState_THRUSTERS_ALL(BossState):
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        # self.set_launchers_sprite(8, 9)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            self.next_state()
            # print("finished")


class BossState_THRUSTERS_TWO(BossState):
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_parent_sprite(3, 6, 100)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            self.next_state()


class BossState_THRUSTERS_ONE(BossState):
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_parent_sprite(6, 9, 100)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            self.next_state()


class BossState_THRUSTERS_DEAD(BossState):
    def __init__(self, parent):
        super().__init__(parent)

    def start(self):
        super().start()
        self.set_parent_sprite(9, 12, 100)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.total_elapsed >= 2500:
            # self.next_state()
            print("DEAD!")



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


class Boss001(EntityVectorMovement):
    def __init__(self):
        super().__init__()
        self.type = EntityType.ENEMY

        self.add_hitbox((0,0,64,30),Vector2(-32, -10))
        self.add_hitbox((0,0,30,15),Vector2(-15, -25))


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
        self.path.on_end_of_path.connect(self.on_end_of_path)
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

        # self.state = Boss001State.LASER_DEAD
        # self.states[self.state].set_parent_sprite(0,3, 100)
        # self.pos = Vector2(1000,300)

        self.states[self.state].start()

    def killed(self):
        pass

    def on_end_of_path(self, sender):
        self.path.distance = 0
    
    def start_path(self, index=None):
        if index:
            self.path.set_new_path(index)
            self.path.distance = 0
        self.running_path = True 
        self.pos = self.path.pos

    def stop_path(self):
        self.runnin_path = False
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
        if game_debugger.show_paths:
            self.path.draw(elapsed, surface)