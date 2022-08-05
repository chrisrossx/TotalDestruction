from enum import IntEnum

import pygame
from blinker import signal 

from TD.paths import PathFollower
from TD.utils import fast_round_point, fast_round
from TD.debuging import game_debugger


class EntityType(IntEnum):
    UNASSIGNED = 0
    PARTICLE = 1
    PICKUP = 2
    ENEMY = 3
    PLAYER = 4
    ENEMYBULLET = 5
    PLAYERBULLET = 6


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
            for e in self.entities_by_type[entity_type]:
                e.tick(elapsed)
        else:
            for e in self.entities:
                e.tick(elapsed)

    def draw(self, elapsed, surface, entity_type=None):
        """
        if entity_type=None, then draw all entities
        """
        if entity_type:
            for e in self.entities_by_type[entity_type]:
                e.draw(elapsed, surface)
        else:
            for e in self.entities:
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
        self.deleted = False 

        # Animation Sprite
        self.frames = [] # List of pygame.Surfaces
        self.frame_index = 0 # Which frame to display
        self.frame_elapsed = 0 # Amount of time the frame has been displayed
        self.frame_duration = -1 # Amount of time to display each frame in milliseconds. If less than 0, animation will stop
        self.frame_loop_start = 0 # Frame to loop back to when frame_count loops back, normally zero

        # Position
        self.sprite_offset = [0, 0] # When drawing animation frame, where
        self.x, self.y = [0.0, 0.0]

        # Movement
        # No Movement is provided in Base Entity, will provide two subclasses
        # 1. Simple Vector Velocity
        # 2. Path Follower

        # Hit Boxes
        self._hitbox_x = None # Compare Last self.x to last _hitbox_x to see if needs to update hitbox. avoid update every tick
        self._hitbox_y = None  # Compare Last self.x to last _hitbox_x to see if needs to update hitbox. avoid update every tick
        self.hitboxs = []
        self.hitbox_offsets = []

    @property
    def pos(self):
        return [self.x, self.y]

    def tick(self, elapsed):
        # Update every tick? or check if self.x or self.y changed?
        if self._hitbox_x != self.x or self._hitbox_y != self.y:
            self._hitbox_x = self.x 
            self._hitbox_y = self.y
            for i in range(len(self.hitboxs)):
                self.hitboxs[i].x = self.x + self.hitbox_offsets[i][0]
                self.hitboxs[i].y = self.y + self.hitbox_offsets[i][1]

    def draw(self, elapsed, surface):
        #Should this be in draw or in tick... 
        # Animation Sprite
        if len(self.frames) > 0 and self.frame_duration > 0:
            self.frame_elapsed += elapsed
            if self.frame_elapsed >= self.frame_duration:
                self.frame_elapsed = 0
                self.frame_index += 1
                if self.frame_index == len(self.frames):
                    self.frame_index = self.frame_loop_start
       
        if len(self.frames) > 0:
            x = fast_round(self.x + self.sprite_offset[0])
            y = fast_round(self.y + self.sprite_offset[1])
            surface.blit(self.frames[self.frame_index], (x, y))

        if game_debugger.show_hitboxs:
            for i in range(len(self.hitboxs)):
                pygame.draw.rect(surface, (255,0,0), self.hitboxs[i], 1)


    def delete(self):
        self.deleted = True 
        signal("scene.delete_entity").send(self)

    def add_hitbox(self, rect, offset):
        self.hitboxs.append(pygame.Rect(rect))
        self.hitbox_offsets.append(offset)


class EntityPathFollower(Entity):
    def __init__(self, path_index):
        super().__init__()

        self.path = PathFollower(path_index)
        self.path.on_end_of_path.connect(self.on_end_of_path)
        self.x, self.y = self.path.pos

    def on_end_of_path(self, sender):
        """
        Default Behavior is to delete self when it reaches end of path
        """
        self.delete()

    def tick(self, elapsed):
        if not self.deleted:
            self.x, self.y = self.path.tick(elapsed)
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
        self.heading = [1, 0]   # Direction Vectory
        self.velocity = 0.1     # Pixels Per Milliscond 0.1 = 100 pixels per second

    def tick(self, elapsed):
        self.x += (self.heading[0] * self.velocity) * elapsed
        self.y += (self.heading[1] * self.velocity) * elapsed
        super().tick(elapsed)
