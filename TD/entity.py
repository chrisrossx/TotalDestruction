from enum import IntEnum

import pygame
from blinker import signal 

from TD.paths import PathFollower
from TD.utils import fast_round_point, fast_round, fast_round_vector2
from TD.debuging import game_debugger


class EntityType(IntEnum):
    UNASSIGNED = 0
    PARTICLE = 1
    PICKUP = 2
    ENEMY = 3
    PLAYER = 4
    ENEMYBULLET = 5
    PLAYERBULLET = 6
    GUI = 7
    DIALOG = 8


class EntityManager:
    def __init__(self, scene):
        self.scene = scene # Parent Scene 
    def __init__(self):
        self.entities = []
        
        self.entities_by_type = []
        for i in range(len(EntityType)):
            self.entities_by_type.append([])

    def tick(self, elapsed, entity_type=None):
        """
        if entity_type=None, then tick all entities
        """
        if entity_type:
            for e in [e for e in self.entities_by_type[entity_type] if e.enabled]:
                e.tick(elapsed)
        else:
            for e in [e for e in self.entities if e.enabled]:
                e.tick(elapsed)

    def on_event(self, event, elapsed, entity_type=None):
        """
        if entity_type=None, then call all entities
        """
        if entity_type:
            for e in [e for e in self.entities_by_type[entity_type] if e.enabled]:
                if hasattr(e, "on_event"):
                    e.on_event(event, elapsed)
        else:
            for e in [e for e in self.entities if e.enabled]:
                if hasattr(e, "on_event"):
                    e.on_event(event, elapsed)


    def draw(self, elapsed, surface, entity_type=None):
        """
        if entity_type=None, then draw all entities
        """
        if entity_type:
            for e in [e for e in self.entities_by_type[entity_type] if e.enabled]:
                e.draw(elapsed, surface)
        else:
            for e in [e for e in self.entities if e.enabled]:
                e.draw(elapsed, surface)

    def delete(self, entity):
        #https://stackoverflow.com/questions/32917388/python-performance-remove-item-from-list
        self.entities = [e for e in self.entities if e != entity]
        entity_type = entity.type
        self.entities_by_type[entity_type] = [e for e in self.entities_by_type[entity_type] if e != entity]

    def add(self, entity):
        #Should we check that its not already the list?, is this unessary and adding delay for only debugging needs
        if entity in self.entities:
            raise Exception("Entity already added")
        self.entities.append(entity)
        self.entities_by_type[entity.type].append(entity)


    # def collidelist(self, other_hitboxes, callback, entity_type=None):
    #     if entity_type:
    #         entities = self.entities_by_type[entity_type]
    #     else:
    #         entities = self.entities

    #     count = 0    
    #     for entity in [e for e in entities]:
    #         if not entity.deleted:
    #             for hitbox in other_hitboxes:
    #                 if hitbox.collidelist(entity.hitboxes) != -1:
    #                     callback(entity)
    #                     count += 1
    #     return count 

    def collidetypes(self, type_a, type_b, multiple_hits=True):
        """
        multiple_hits: If set to True then type_a can collide with many type_b. If set 
        to false then type_a can only strike the first type_b, then will not hit anymore
        type_bs. Example, if type_a is bullets, only strike first type_b, don't keep kitting type_b
        if there are multiple type_b collisions. 
        """

        # {type_b: [type_a, type_a]},

        collisions = {}

        ignore_type_a = []

        for entity_b in self.entities_by_type[type_b]:
            type_a_hitboxes = [e.hitboxes[0] for e in self.entities_by_type[type_a] if (not e.deleted and e not in ignore_type_a)]
            if not entity_b.deleted:
                for entity_b_hitbox in entity_b.hitboxes:
                    hits = entity_b_hitbox.collidelistall(type_a_hitboxes)
                    if len(hits) > 0:
                        collisions[entity_b] = []
                        entities_a = [self.entities_by_type[type_a][i] for i in hits]
                        for entity_a in entities_a:
                            collisions[entity_b].append(entity_a)
                            if not multiple_hits:
                                ignore_type_a.append(entity_a)
                        break # Don't keep looping through enemy hitboxes because already hit
        return collisions

class Entity:
    """
    Base game object

    #1) Moves
    #2) Hit boxes
    3) Can be deleted
    4) Can be spawned
    #5) Needs to be updated with Tick
    #6) Can be asked to draw itself
    #8) Holds a animated sprite
    #9) Can be different type of game objects
    ?7) Can be a child of another entity
    ?8) Can be a parent of children 
    """

    def __init__(self):

        # Meta / State
        self.type = EntityType.UNASSIGNED
        self.deleted = False # In Process of being deleted, don't collide with anything.
        self.enabled = True # Don't Draw or Tick

        # Animation Sprite
        self.frames = [] # List of pygame.Surfaces
        self.frame_index = 0 # Which frame to display
        self.frame_elapsed = 0 # Amount of time the frame has been displayed
        self.frame_duration = -1 # Amount of time to display each frame in milliseconds. If less than 0, animation will stop
        self.frame_loop_start = 0 # Frame to loop back to when frame_count loops back, normally zero
        self.frame_loop_count = 0 # After x Counts then delete self
        self.frame_loop_end = -1 # If greater than 0 delete self after that many loop

        # Position
        self.sprite_offset = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(0.0, 0.0)

        # Movement
        # No Movement is provided in Base Entity, will provide two subclasses
        # 1. Simple Vector Velocity
        # 2. Path Follower

        # Hit Boxes
        # self._hitbox_last_pos = pygame.Vector2(0,0) # Cache last position and only update hitboxes if Entity has moved. avoid update every tick
        self.hitboxes = []
        self.hitbox_offsets = []


    @property
    def surface(self):
        return self.frames[self.frame_index]
        
    @property
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, v):
        self.pos.x = v

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, v):
        self.pos.y = v

    def get_rect(self):
        return self.frames[self.frame_index].get_rect()

    def animation_finished_callback(self, entity):
        entity.delete()

    def tick(self, elapsed):
        # Animation Sprite
        if len(self.frames) > 0 and self.frame_duration > 0:
            self.frame_elapsed += elapsed
            if self.frame_elapsed >= self.frame_duration:
                self.frame_elapsed = 0
                self.frame_index += 1
                if self.frame_index == len(self.frames):
                    self.frame_index = self.frame_loop_start
                    self.frame_loop_count += 1
                    if self.frame_loop_end >= 0 and self.frame_loop_count >= self.frame_loop_end:
                        # self.delete()
                        self.animation_finished_callback(self)

        #Update Hitbox positions to follow Entity       
        for i in range(len(self.hitboxes)):
            self.hitboxes[i].topleft = self.pos + self.hitbox_offsets[i]

    def draw(self, elapsed, surface):
        if len(self.frames) > 0:
            # TODO is this needed, or wont the blit do roudning anyways? 
            point = fast_round_vector2(self.pos + self.sprite_offset)
            surface.blit(self.frames[self.frame_index], point)

        if game_debugger.show_hitboxes:
            for i in range(len(self.hitboxes)):
                pygame.draw.rect(surface, (255,0,0), self.hitboxes[i], 1)

        if game_debugger.show_bounds:
            if len(self.frames) > 0:
                rect = self.frames[self.frame_index].get_rect()
                rect.topleft = point
                pygame.draw.rect(surface, (100,100,100), rect, 1)
                pygame.draw.circle(surface, (255,255,255), self.pos, 4)


    def delete(self):
        self.deleted = True 
        self.enabled = False 
        signal("scene.delete_entity").send(self)

    def add_hitbox(self, rect, offset):
        self.hitboxes.append(pygame.Rect(rect))
        self.hitbox_offsets.append(offset)


class EntityPathFollower(Entity):
    def __init__(self, path_index):
        super().__init__()

        self.path = PathFollower(path_index)
        self.path.on_end_of_path.connect(self.on_end_of_path)
        self.pos = self.path.pos #this is a reference to a vector2, so update to path will update position of entity. 

    def on_end_of_path(self, sender):
        """
        Default Behavior is to delete self when it reaches end of path
        """
        self.delete()

    def tick(self, elapsed):
        if not self.deleted:
            self.path.tick(elapsed)
        super().tick(elapsed)

    @property
    def velocity(self):
        return self.path.velocity
    
    @velocity.setter
    def velocity(self, value):
        self.path.velocity = value

    def draw(self, elapsed, surface):
        if game_debugger.show_paths:
            self.path.draw(elapsed, surface)
        super().draw(elapsed, surface)



class EntityVectorMovement(Entity):
    def __init__(self):
        super().__init__()

        # Movement
        self.heading = pygame.math.Vector2(1, 0)  # Direction Vector
        self.velocity = 0.1 # Pixels Per Milliscond 0.1 = 100 pixels per second

    def tick(self, elapsed):
        self.pos += self.heading * self.velocity * elapsed 
        super().tick(elapsed)
