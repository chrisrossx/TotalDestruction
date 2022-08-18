import pygame
from pygame import Vector2

from TD.assetmanager import asset_manager
from TD.entity import Entity, EntityType, EntityManager
from blinker import signal


class GUIEntity(Entity):
    def __init__(self):
        super().__init__()
        self.type = EntityType.GUI

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



class GUIPanel(GUIEntity):
    def __init__(self, size):
        super().__init__()
        self.size = size 
        self.frames = [pygame.Surface(self.size, pygame.SRCALPHA), ]
        self.background_color = (0,0,0,255)
        self.em = EntityManager()

    def tick(self, elapsed):
        super().tick(elapsed)
        self.em.tick(elapsed)

    def draw(self, elapsed, surface):
        self.frames[0].fill(self.background_color)
        self.em.draw(elapsed, self.frames[0])
        super().draw(elapsed, surface)


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



class Neighbors:
    def __init__(self):
        self.top = None
        self.bottom = None 
        self.left = None
        self.right = None 


class GuiButtonGroup(GUIEntity):
    def __init__(self, pressed_callback=None):
        super().__init__()
        self.pressed_callback = pressed_callback
        self.em = EntityManager()
        self.selected = None 
        self.buttons = {}

    def select(self, name):
        self.selected = name 
        self.buttons[self.selected].on_selected()

    def on_event(self, event, elapsed):

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.selected and self.pressed_callback:
                self.pressed_callback(self.selected)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if self.buttons[self.selected].left:
                self.select(self.buttons[self.selected].left)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if self.buttons[self.selected].right:
                self.select(self.buttons[self.selected].right)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if self.buttons[self.selected].bottom:
                self.select(self.buttons[self.selected].bottom)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if self.buttons[self.selected].top:
                self.select(self.buttons[self.selected].top)
    
    def draw(self, elapsed, surface):
        self.em.draw(elapsed, surface)

    def tick(self, elapsed):
        self.em.tick(elapsed)

    def add(self, btn):
        self.em.add(btn)
        self.buttons[btn.name] = btn


class GuiButton(GUIEntity):
    """
    if lbl_position is not given, then lbl will center itsel.
    """
    def __init__(self, name, size, lbl, lbl_offset=None, lbl_position=None, top=None, bottom=None, left=None, right=None):
        super().__init__()
        self.name = name
        self.background_color = (0,0,0,0)
        self.frames = [pygame.Surface(size, pygame.SRCALPHA),]
        self.lbl = lbl 
        self.lbl_position = lbl_position
        self.lbl_offset = Vector2(0,0) if lbl_offset == None else lbl_offset
        self.top = top
        self.bottom = bottom 
        self.left = left
        self.right = right 
        self.selected = False
        self.render()

    def on_event(self, event, elapsed):
        if not self.selected:
            return

    def on_selected(self):
        pass 

    def on_deselected(self):
        pass 

    def render(self):
        
        self.surface.fill(self.background_color)
        if self.lbl_position == None:
            s_rect = self.surface.get_rect()
            l_rect = self.lbl.get_rect()
            x = (s_rect.w / 2) - (l_rect.w / 2) + self.lbl_offset.x 
            y = (s_rect.h / 2) - (l_rect.h / 2) + self.lbl_offset.y 
        else:
            x, y = self.lbl_position.x + self.lbl_offset.x, self.lbl_position.y + self.lbl_offset.y
        self.surface.blit(self.lbl.surface, (x,y))
