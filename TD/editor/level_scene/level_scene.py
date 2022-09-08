from pygame import Vector2
import pygame
from TD import editor
from TD.config import SKY_VELOCITY, SCREEN_RECT
from TD.editor.config import EDITOR_SCREEN_RECT, EDITOR_SCREEN_SIZE

from TD.editor.scene import Scene
from TD.entity import Entity, EntityType
from .sky import Sky
from TD.editor import gui
from TD.editor.config import EDITOR_SCREEN_SIZE
from TD.assetmanager import asset_manager
from .level_size import GUILevelSizeTimeCursor
from .level_chain import GUILevelChainDetails
from .level_file import GUILevelFile
from .level_paths import GUILevelPaths
from .level_new import GUILevelNew
from .level_details import GUILevelDetails
from .level_boss import GUILevelBossDetails
from .level_control import GUILevelControlDetails
from .level_markers import GUILevelMarker
from .level_chain_library import GUILevelChainLibrary
from TD.editor.globals import current_level
from TD.levels.data import LevelData, LevelEntityType


class SceneLevel(Scene):
    def __init__(self, filename):
        super().__init__()

        # self.level = load("level_001.json")  # Level Data
        self.level = LevelData(filename)  # Level Data
        current_level.__wrapped__ = self.level 
        self.level.editor_mode()

        # self.level_renderer = LevelRenderer(self.level)

        self.selected_level_entity = None

        self.sky = Sky()
        self._time = 0.0  # Current Offset of the display/Level
        # self.time_cursor_position = 0.0  # Where the Yellow Time Cursor Triangles are
        self.play_time = False 

        self.badge_rects = [] # Keep track of badge buttons on screen so they can avoid overlapping

        self.window_rect = pygame.Rect(
            100, 100, SCREEN_RECT.w, SCREEN_RECT.h
        )  # Players Game Screen Window

        self.gui_groups["level_size"] = GUILevelSizeTimeCursor(self)
        self.gui_groups["level_chain"] = GUILevelChainDetails(self)
        self.gui_groups["level_file"] = GUILevelFile(self)
        self.gui_groups["level_paths"] = GUILevelPaths(self)
        self.gui_groups["level_new"] = GUILevelNew(self)
        self.gui_groups["level_details"] = GUILevelDetails(self)
        self.gui_groups["level_boss"] = GUILevelBossDetails(self)
        self.gui_groups["level_control"] = GUILevelControlDetails(self)
        self.gui_groups["level_marker"] = GUILevelMarker(self)
        self.gui_groups["level_chain_library"] = GUILevelChainLibrary(self)

        # self.select_level_entity(self.level.level_entities[0])

    def select_level_entity(self, entity):
        if self.selected_level_entity != None:
            if self.selected_level_entity.type == LevelEntityType.ENEMY_CHAIN:
                self.gui_level_chain.select_chain(None)
            if self.selected_level_entity.type == LevelEntityType.BOSS:
                self.gui_level_boss.select_boss(None)
            if self.selected_level_entity.type == LevelEntityType.CONTROL:
                self.gui_level_control.select_control(None)
            self.selected_level_entity = None 
        if entity != None:
            if entity.type == LevelEntityType.ENEMY_CHAIN:
                self.gui_level_chain.select_chain(entity)
            if entity.type == LevelEntityType.BOSS:
                self.gui_level_boss.select_boss(entity)
            if entity.type == LevelEntityType.CONTROL:
                self.gui_level_control.select_control(entity)
            self.selected_level_entity = entity



    def on_event(self, event, elapsed):
        self.level.editor_on_event(event, elapsed)
        super().on_event(event, elapsed)

    @property
    def pixel_offset_with_time(self):
        return ((self._time * SKY_VELOCITY) * -1) + 100

    @property
    def time(self):
        return self._time

    def __getattr__(self, name):
        if name.startswith("gui_"):
            name = name[4:]
        if name in self.gui_groups:
            return self.gui_groups[name]
        raise AttributeError

    @time.setter
    def time(self, value):
        if value < 0:
            value = 0
        if value > (self.level.total_time - (SCREEN_RECT.w / SKY_VELOCITY)):
            value = self.level.total_time - (SCREEN_RECT.w / SKY_VELOCITY)
        value = round(value, 2)
        self._time = value
        self.gui_level_size.update_time_curosr_elements()

    @property
    def max_editor_playable_time(self):
        return self.level.total_time - (SCREEN_RECT.w / SKY_VELOCITY)

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.play_time:
            self.time += elapsed
            self.gui_level_size.set_time_slider_value(self.time)
            if self.time >= self.max_editor_playable_time:
                self.on_btn_play(self.btn_play)
        
        start_time = self.time - (EDITOR_SCREEN_RECT.w / SKY_VELOCITY) 
        end_time = self.time + (EDITOR_SCREEN_RECT.w / SKY_VELOCITY) * 2
        # end_time = self.time + (SCREEN_RECT.w / SKY_VELOCITY) * 1
        self.level.editor_tick(elapsed, start_time, end_time, self.pixel_offset_with_time)

    def draw(self, elapsed):
        self.surface.fill((0, 0, 0))

        # Gret Lines Top and Bottom Sky Rails
        grey = (80, 80, 80)
        pygame.draw.line(self.surface, grey, (0, 100), (EDITOR_SCREEN_SIZE.x, 100))
        pygame.draw.line(self.surface, grey, (0, 700), (EDITOR_SCREEN_SIZE.x, 700))

        pygame.draw.rect(self.surface, (255, 255, 255), self.window_rect, 1)
        # self.sky.draw(elapsed, self.surface, self.time)
        self.gui_level_chain.draw(elapsed, self.surface)
        self.gui_level_file.draw(elapsed, self.surface)
        self.gui_level_marker.draw(elapsed, self.surface)
        self.gui_level_size.draw(elapsed, self.surface)
        self.em.draw(elapsed, self.surface, EntityType.PICKUP)
        self.em.draw(elapsed, self.surface, EntityType.ENEMY)
        self.em.draw(elapsed, self.surface, EntityType.BOSS)
        self.em.draw(elapsed, self.surface, EntityType.PARTICLE)
        self.em.draw(elapsed, self.surface, EntityType.PLAYER)
        self.em.draw(elapsed, self.surface, EntityType.PLAYERBULLET)
        self.em.draw(elapsed, self.surface, EntityType.ENEMYBULLET)

        #Find Enemies that should be drawn
        start_time = self.time - (EDITOR_SCREEN_RECT.w / SKY_VELOCITY) 
        end_time = self.time + (EDITOR_SCREEN_RECT.w / SKY_VELOCITY) * 2
        # self.level.editor_draw(elapsed, self.surface, start_time, end_time, self.pixel_offset_with_time, LevelEntityType.BOSS)
        if self.gui_level_details.btn_show_chains.toggled:
            self.level.editor_draw(elapsed, self.surface, start_time, end_time, self.pixel_offset_with_time, LevelEntityType.ENEMY_CHAIN)
        if self.gui_level_details.btn_show_boss.toggled:
            self.level.editor_draw(elapsed, self.surface, start_time, end_time, self.pixel_offset_with_time, LevelEntityType.BOSS)
        if self.gui_level_details.btn_show_controls.toggled:
            self.level.editor_draw(elapsed, self.surface, start_time, end_time, self.pixel_offset_with_time, LevelEntityType.CONTROL)
        
        self.em.draw(elapsed, self.surface, EntityType.GUI)
        self.em.draw(elapsed, self.surface, EntityType.DIALOG)