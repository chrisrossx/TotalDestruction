from enum import Enum
import pygame 

import random 
from pygame import Vector2

from TD.entity import EntityVectorMovement, EntityType, Entity, EntityManager
from TD.assetmanager import asset_manager
from TD.paths import PathFollower
from TD.debuging import game_debugger
from TD import current_app, current_scene
from TD.particles.spoofs import SpoofHitFollow
from TD.pickups import PickupCoin

class BossState:
    state = None
    def __init__(self, parent):
        self.parent = parent 
        self.total_elapsed = 0
        self.gun = None
        self.drop_coins = False 

    # @property
    # def laser_sprite(self):
    #     return self.parent.laser_sprite 

    # @property 
    # def launchers_sprite(self):
    #     return self.parent.launchers_sprite
        
    @property
    def heading(self):
        return self.parent.heading 

    @heading.setter
    def heading(self, value):
        self.parent.heading = value
    
    @property
    def delete(self):
        return self.parent.delete

    @property
    def velocity(self):
        return self.parent.velocity
    
    @velocity.setter
    def velocity(self, value):
        self.parent.velocity = value 

    @property
    def next_state(self):

        if self.drop_coins:
            r = (random.randint(0, 40)**2)/500
            r = round(r, 0)
            print("counts", r)

            for i in range(int(r)):
                p = PickupCoin(self.pos)
                current_scene.em.add(p)

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
        if self.gun:
            self.gun.tick(elapsed)

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


class Boss(EntityVectorMovement):
    def __init__(self):
        super().__init__()
        self.type = EntityType.BOSS
        self.em = EntityManager()

        self.health = 0
        
        self.pos = Vector2(1024+60, 300)
        self.velocity = 0

        self.path = PathFollower(0)
        self.path.on_end_of_path.append(self.on_end_of_path)
        self.path.velocity = 0.11
        self.running_path = False 

        self.state = None 
        self.states = {}
        self.health_by_state = {}

    def start(self, start_state):
        self.state = start_state
        for h in self.health_by_state.values():
            if h > 0:
                self.health += h

        self.states[self.state].start()        

    def hit(self, bullet):
        l = (bullet.pos.lerp(self.pos, 0.8) - bullet.pos) * -1
        current_scene.em.add(SpoofHitFollow(self, l))
        current_app.mixer.play("enemy hit")
        self.states[self.state].hit(bullet)

    def killed(self):
        for i in range(42):
            p = PickupCoin(self.pos, big_explosion=True)
            current_scene.em.add(p)
        self.velocity = 0
        self.stop_path()
        self.pos = Vector2(2000,0)
        
    def delete(self):
        current_scene.em.delete(self)

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
        self.state = self.state_enum(self.state.value + 1)
        self.states[self.state].start()

    def tick(self, elapsed):
        self.states[self.state].tick(elapsed)
        super().tick(elapsed)
        self.em.tick(elapsed) 
        for e in self.em.entities:
            e.pos = self.pos 

        if not self.deleted and self.running_path:
            self.path.tick(elapsed)

    def draw(self, elapsed, surface):
        self.states[self.state].draw(elapsed, surface)
        self.em.draw(elapsed, surface)

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

            for i in range(len(self.gun_points)):
                pygame.draw.circle(surface, (0,255,0), self.pos + self.gun_points[i], 5, 1)

            for i in range(len(self.hitboxes)):
                pygame.draw.rect(surface, (255, 0, 0), self.hitboxes[i], 1)


class BossLayeredSprite(Entity):
    def __init__(self):
        super().__init__()
        self.type == EntityType.BOSS
        self.sprites = []

    def on_finished_callback(self, entity):
        # Don't do default behavor of deleting on end of animation
        pass        

    def set_sprite(self, start_frame, end_frame, duration=-1, loop_end=-1):
        self.frames = self.sprites[start_frame:end_frame]
        self.frame_index = 0
        self.frame_elapsed = 0
        self.frame_duration = duration
        self.frame_loop_start = 0
        self.frame_loop_count = 0 
        self.frame_loop_end = loop_end 

