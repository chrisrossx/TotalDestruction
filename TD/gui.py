import pygame
from pygame import Vector2

from TD.assetmanager import asset_manager
from TD.entity import Entity, EntityType, EntityManager


class GUIPanel(Entity):
    def __init__(self, size):
        super().__init__()
        self.type = EntityType.GUI
        self.size = size 
        self.frames = [pygame.Surface(self.size, pygame.SRCALPHA), ]
        self.background_color = (0,0,0,255)
        self.em = EntityManager()
        # self.redraw = True

    def tick(self, elapsed):
        super().tick(elapsed)
        self.em.tick(elapsed)

    def draw(self, elapsed, surface):
        # if self.redraw:
        self.frames[0].fill(self.background_color)
        self.em.draw(elapsed, self.frames[0])
        # self.redraw = False

        super().draw(elapsed, surface)


class GUIEntity(Entity):
    def bjust_in_rect(self, rect, offset=0):
        surface_rect = self.get_rect()
        self.y = rect.h + offset - surface_rect.h

    def tjust_in_rect(self, rect, offset=0):
        surface_rect = self.get_rect()
        self.y = rect.y + offset 

    def rjust_in_rect(self, rect, offset=0):
        surface_rect = self.get_rect()
        self.x = rect.w + offset - surface_rect.w

    def ljust_in_rect(self, rect, offset=0):
        surface_rect = self.get_rect()
        self.x = rect.x + offset 

    def centerx_in_rect(self, rect):
        surface_rect = self.get_rect()
        self.pos.x = rect.centerx - (surface_rect.w/2)

    def centery_in_rect(self, rect):
        surface_rect = self.get_rect()
        self.pos.y = rect.centery - (surface_rect.h/2)

    def center_in_rect(self, rect):
        surface_rect = self.get_rect()
        self.pos.x = rect.centerx - (surface_rect.w/2)
        self.pos.y = rect.centery - (surface_rect.h/2)



class GUILabel(GUIEntity):

    shadow_step = Vector2(3, 3)

    def __init__(self, text, font, color, pos=None, shadow_color=None, shadow_step=None):
        super().__init__()
        self.type = EntityType.GUI
        self.pos = pos.copy() if pos != None else Vector2(0,0)
        self.text = text
        self.font = font
        self.color = color
        self.shadow_color = shadow_color
        self.shadow_step = shadow_step if shadow_step != None else self.shadow_step

        self.render()
    
    def set_text(self, new_text):
        self.text = new_text
        self.render()

    def render(self):
        line = self.font.render(self.text, True, self.color)
        rect = line.get_rect()
        w = rect.w 
        h = rect.h 
        if self.shadow_color != None:
            w += self.shadow_step.x
            h += self.shadow_step.y
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        if self.shadow_color != None:
            shadow_line = self.font.render(self.text, True, self.shadow_color)
            if len(self.shadow_color) == 4:
                shadow_line.set_alpha(self.shadow_color[3])
            surface.blit(shadow_line, self.shadow_step)
        surface.blit(line, (0,0))

        self.frames = [surface,]


class MenuCursor(GUIEntity):
    def __init__(self, flip_x=False):
        super().__init__()
        self.type = EntityType.GUI
        self.frame_duration = 77
        if flip_x:
            self.frames = asset_manager.sprites["Menu Cursor Right"]
            self.sprite_offset = [-8, -16]
        else:
            self.frames = asset_manager.sprites["Menu Cursor Left"]
            self.sprite_offset = [-24, -16]

class GUISprite(GUIEntity):
    def __init__(self, frames):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = frames 
