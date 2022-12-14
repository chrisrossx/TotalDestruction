from pathlib import Path 

from pygame import Vector2
from pygame.rect import Rect

PATHS_FILENAME = Path("line_editor.json")
SCREEN_SIZE = Vector2(1024, 600)
SCREEN_RECT = Rect(0, 0, SCREEN_SIZE.x, SCREEN_SIZE.y)
SKY_VELOCITY = 0.1
SAVE_FILENAME = Path("TD/save.json")


NUMBER_OF_LEVELS = 4

LEVEL_001_FILENAME = Path("001/Level_001sf.005.json")
LEVEL_002_FILENAME = Path("002/Level_002.001.json")
LEVEL_003_FILENAME = Path("003/Level_003.001.json")
LEVEL_004_FILENAME = Path("004/Level_004.001.json")
