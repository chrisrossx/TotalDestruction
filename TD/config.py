from pathlib import Path 

from pygame import Vector2
from pygame.rect import Rect

PATHS_FILENAME = Path("TD/line_editor.json")
SCREEN_SIZE = Vector2(1024, 600)
SCREEN_RECT = Rect(0, 0, SCREEN_SIZE.x, SCREEN_SIZE.y)
SKY_VELOCITY = 0.1
SAVE_FILENAME = Path("TD/save.json")
