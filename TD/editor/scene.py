from enum import Enum

import pygame

from TD.entity import EntityType, EntityManager
from TD.editor.config import EDITOR_SCREEN_SIZE
from TD.editor.gui import grid_pos, grid_size


class Scene:
    def __init__(self):
        self.em = EntityManager()
        self.surface = pygame.Surface(EDITOR_SCREEN_SIZE)
        self.active_text_box = None
        self.gui_layer = 0
        self.widget_size = (6, 1)
        self.gui_groups = {}

    def pressed(self, pressed, elapsed):
        for group in self.gui_groups.values():
            group.pressed(pressed, elapsed)

    def on_event(self, event, elapsed):
        self.em.on_event(event, elapsed, EntityType.GUI)
        self.em.on_event(event, elapsed, EntityType.DIALOG)
        for group in self.gui_groups.values():
            group.on_event(event, elapsed)

    def activate(self):
        pass

    def deactivate(self):
        if self.active_text_box:
            self.active_text_box.deactivate()

    def on_start(self):
        pass

    def on_delete(self):
        pass

    def tick(self, elapsed):
        self.em.tick(elapsed)
        for group in self.gui_groups.values():
            group.tick(elapsed)

    def draw(self, elapsed):
        self.surface.fill((0, 0, 0))
        self.em.draw(elapsed, self.surface, EntityType.PICKUP)
        self.em.draw(elapsed, self.surface, EntityType.ENEMY)
        self.em.draw(elapsed, self.surface, EntityType.BOSS)
        self.em.draw(elapsed, self.surface, EntityType.PARTICLE)
        self.em.draw(elapsed, self.surface, EntityType.PLAYER)
        self.em.draw(elapsed, self.surface, EntityType.PLAYERBULLET)
        self.em.draw(elapsed, self.surface, EntityType.ENEMYBULLET)
        self.em.draw(elapsed, self.surface, EntityType.GUI)
        for group in self.gui_groups.values():
            group.draw(elapsed, self.surface)
        self.em.draw(elapsed, self.surface, EntityType.DIALOG)

    def grid_size(self, width=None, height=None):
        width = width if width != None else 6
        height = height if height != None else 1
        size = grid_size(width, height)
        return size

    def grid_pos(self, col, row):
        pos = grid_pos(col, row)
        grid_left = 3
        grid_top = 830
        pos += (grid_left, grid_top)
        return pos


class GUIGroup:
    def __init__(self, parent):
        """
        Instead of using mixins, use this class to put groups of GUI controls into a sperate class that gets
        updated into the scene. Can be accessed via key work attributes
        scene.gui_this_key_name from the key used when adding the group scene.gui_groups["this_key_name"]
        """
        self.parent = parent

    def on_event(self, event, elapsed):
        pass

    def pressed(self, pressed, elapsed):
        pass

    def on_event(self, event, elapsed):
        pass

    def tick(self, elapsed):
        pass

    def draw(self, elapsed, surface):
        pass

    @property
    def em(self):
        return self.parent.em

    @property
    def grid_size(self):
        return self.parent.grid_size

    @property
    def grid_pos(self):
        return self.parent.grid_pos

    @property
    def time(self):
        return self.parent.time

    @time.setter
    def time(self, value):
        self.parent.time = value

    # @property
    # def time_cursor_position(self):
    #     return self.parent.time_cursor_position

    # @time_cursor_position.setter
    # def time_cursor_position(self, value):
    #     self.parent.time_cursor_position = value

    @property
    def gui_layer(self):
        return self.parent.gui_layer

    @property
    def level(self):
        return self.parent.level

    @property
    def surface(self):
        return self.parent.surface
