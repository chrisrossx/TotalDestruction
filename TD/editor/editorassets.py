from pathlib import Path
import pygame 
from pygame import Vector2

from TD.assetmanager import asset_manager, load_sprite_from_file, load_sprite_from_files

def render_entity_badge(letter, color, color_active, color_selected, font_color=(0,0,0)):
    surfaces = []
    lbl = asset_manager.fonts["xs"].render(letter, True, font_color)
    l_rect = lbl.get_rect()
    rect = pygame.Rect(0, 0, 16, 16)
    for c in [color, color_active, color_selected]:
        surface = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(surface, c, rect, 0)
        x = (rect.w / 2) - (l_rect.w / 2)
        y = (rect.h / 2) - (l_rect.h / 2)
        surface.blit(lbl, (x, y))
        surfaces.append(surface)
    return surfaces

class EditorAssets():
    def __init__(self):

        self.sprites = {}

    def load(self):
        self.sprites["icon T8"] = asset_manager.sprites["T8"][0]
        self.sprites["icon CX5B"] = asset_manager.sprites["CX5B"][0]
        self.sprites["icon HX7"] = asset_manager.sprites["HX7"][0].subsurface(pygame.Rect(0,16,64,64-16))
        self.sprites["icon D2"] = pygame.transform.smoothscale(asset_manager.sprites["D2"][0], Vector2(116,64) * 0.7)
        self.sprites["icon BT1"] = pygame.transform.scale(asset_manager.sprites["BT1"][0], (48,48))

        self.sprites["icon Boss 001"] = asset_manager.sprites["Boss 001"][0]
        self.sprites["icon Boss 001"].blit(asset_manager.sprites["Boss 001 laser"][0], (0,0))
        self.sprites["icon Boss 001"] = pygame.transform.smoothscale(self.sprites["icon Boss 001"], Vector2(128,128) * 0.5)

        self.sprites["badge chain"] = render_entity_badge("C", (127, 127, 127), (255, 60, 60), (60, 60, 255))
        self.sprites["icon show white"] = load_sprite_from_file(Path("TD/editor/assets/eye_white.png"))[0]
        self.sprites["icon show black"] = load_sprite_from_file(Path("TD/editor/assets/eye_black.png"))[0]
        self.sprites["btn icon trash"] = load_sprite_from_files(Path("TD/editor/assets/Trash_Icon.png"), ["-1", "-2", "-3"])
        self.sprites["btn icon copy"] = load_sprite_from_files(Path("TD/editor/assets/Copy_Icon.png"), ["-1", "-2", "-3"])
        self.sprites["btn icon paste"] = load_sprite_from_files(Path("TD/editor/assets/Paste_Icon.png"), ["-1", "-2", "-3"])





editor_assets = EditorAssets()
