import subprocess
import sys 

from pygame import Vector2
import pygame

from TD.config import SCREEN_SIZE, SKY_VELOCITY, SCREEN_RECT
from TD.editor.config import EDITOR_SCREEN_RECT, EDITOR_SCREEN_SIZE
from TD.editor.scene import Scene, GUIGroup
from TD.entity import EntityType, Entity
from TD.editor import gui
from TD.editor.config import EDITOR_SCREEN_SIZE
from TD.assetmanager import asset_manager
from TD.editor.globals import current_level
from TD.editor.editorassets import editor_assets
from TD.levels.data import LevelEntityType

from .colors import COLORS






class GUILevelPaths(GUIGroup):
    def __init__(self, parent):
        super().__init__(parent)

