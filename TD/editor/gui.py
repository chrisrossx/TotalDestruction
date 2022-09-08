from re import S
import pygame
from pygame import Vector2

from TD.entity import Entity, EntityType, EntityManager
from TD.assetmanager import asset_manager
from TD.editor.globals import current_app, current_scene
from TD.editor.config import EDITOR_SCREEN_RECT, EDITOR_SCREEN_SIZE
from TD.editor.editorassets import editor_assets

SEGMENT_A = 29  #Width of 1 Cell
SEGMENT_B = 6   #Width of Col Spacer
SEGMENT_C = 24  #Height of 1 Cell
SEGMENT_D = 5   #Height of Row Spacer
# GRID_TOP = 830

def multi_line_text_render(text, font, color, align="left", vertical_spacing=4):
    lines = text.split("\n")
    surfaces = []
    size = Vector2(0, 0)
    for line in lines:
        surface = font.render(line, True, color)
        surfaces.append(surface)
        size.y += surface.get_rect().h
        if surface.get_rect().w > size.x:
            size.x = surface.get_rect().w
    
    size.y += (len(lines) - 1) * vertical_spacing

    output = pygame.Surface(size, pygame.SRCALPHA)
    y = 0
    for surface in surfaces:
        x = 0
        output.blit(surface, (x, y))
        y += surface.get_rect().h + vertical_spacing

    return output


def grid_pos(col, row):
    left = SEGMENT_B + (col * (SEGMENT_A + SEGMENT_B))
    top = SEGMENT_D + (row * (SEGMENT_C + SEGMENT_D))
    return Vector2(left, top)


def grid_size(width, height):
    # width, height = size
    pixel_width = (width * SEGMENT_A) + ((width - 1) * SEGMENT_B)
    pixel_height = (height * SEGMENT_C) + ((height - 1) * SEGMENT_D)
    return Vector2(pixel_width, pixel_height)


class GUIEntityManager(EntityManager):
    def __init__(self, gui_layer):
        super().__init__()
        self._gui_layer = gui_layer

    def add(self, entity):
        super().add(entity)
        entity.gui_layer = self._gui_layer


class Panel(Entity):
    default_widget_size = Vector2(6, 1)
    def __init__(self, pos, size, title):
        super().__init__()
        self.type = EntityType.DIALOG
        self.frames = [
            pygame.Surface(size, pygame.SRCALPHA),
        ]

        self.mask = pygame.Surface(EDITOR_SCREEN_SIZE, pygame.SRCALPHA)
        self.mask.fill((255,255,255))
        # self.mask.fill((0,0,0))
        self.mask.set_alpha(80)

        self.pos = Vector2(pos)  # .copy()
        self._disabled = False
        self._hovered = False
        self._rect = None
        self.enabled = True
        self._title = title

        self.background_color = (20, 20, 20)
        self.border_color = (220, 220, 220)
        self.em = GUIEntityManager(gui_layer = 1)
        self.render()

        self.btn_close = Button("X", Vector2(0, 0), Vector2(24, 24), align="center" )
        self.btn_close.rjust_in_rect(self.rect, 5)
        self.btn_close.tjust_in_rect(self.rect, 5)
        self.btn_close.on_button_1.append(self._cancel_button)
        self.em.add(self.btn_close)

        self.on_cancel = []

    def grid_size(self, width=None, height=None):
        width = width if width != None else 6
        height = height if height != None else 1
        size = grid_size(width, height)
        return size

    
    def grid_pos(self, col, row):
        pos = grid_pos(col, row)
        grid_left = 4
        grid_top = 40
        pos += (grid_left, grid_top)
        pos += self.pos
        return pos

    def get_panel_size_by_grid(self, cols, rows):
        pixel_width = (cols * SEGMENT_A) + ((cols + 1) * SEGMENT_B)
        pixel_height = (rows * SEGMENT_C) + ((rows + 1) * SEGMENT_D)
        size = Vector2(pixel_width, pixel_height)
        
        size += Vector2(8, 4) #border
        size.y += 40 #title bar
        return size

    def set_gui_level(self, level):
        for entity in self.em.entities:
            entity.gui_layer = level 


    def _cancel_button(self, btn):
        for cb in self.on_cancel:
            cb(self)
        self.close()


    def on_event(self, event, elapsed):
        self.em.on_event(event, elapsed, EntityType.GUI)

    def render(self):
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, self.background_color, self.get_rect(), 0, 8)
        pygame.draw.rect(self.surface, self.border_color, self.get_rect(), 2, 8)
        pygame.draw.line(self.surface, self.border_color, (0, 32), (self.get_rect().w, 32), 2)
        lbl = current_app.font.render(self._title, True, self.border_color)
        self.surface.blit(lbl, (11, 12))

    def close(self):
        self.enabled = False 
        current_scene.gui_layer -= 1
        current_scene.em.delete(self)

    def show(self):
        self.enabled = True
        current_scene.gui_layer += 1
        self.set_gui_level(current_scene.gui_layer)

    def draw(self, elapsed, surface):
        surface.blit(self.mask, (0,0))
        super().draw(elapsed, surface)
        self.em.draw(elapsed, surface, EntityType.GUI)

    def tick(self, elapsed):
        super().tick(self)
        self.em.tick(elapsed, EntityType.GUI)

    @property
    def rect(self):
        """
        Cached copy of Surface Rect with Position Set to parent pos and sprite_offset
        """
        if not self._rect:
            self._rect = self.get_rect()
            self._rect.topleft = self.pos + self.sprite_offset
        return self._rect


class ChooseListPanel(Panel):
    def __init__(self, title, items, current_value=None):
        panel_rows = 12
        panel_cols = ((len(items) // 12) + 1) * self.default_widget_size.x
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, title)

        self.title = title
        self.items = items
        self.current_value = current_value
        self.on_choice = []

        sy = self.pos.y + 40
        sx = self.pos.x + 10
        y_step = 29
        x_step = 245
        
        for i, key in enumerate(items.keys()):
            value = items[key]
            r = (i % panel_rows) 
            c = (i // panel_cols) * self.default_widget_size.x
            btn = Button(key, self.grid_pos(c, r), self.grid_size())
            self.em.add(btn)
            if value == current_value:
                btn.toggled = True
            btn.on_button_1.append(lambda btn, key=key: self.on_btn_click(key))

    def on_btn_click(self, key):
        value = self.items[key]
        self.close()
        for cb in self.on_choice:
            cb(key, value)


class ConfirmPanel(Panel):
    def __init__(self, title, on_confirm=None, on_cancel=None):
        panel_rows = 1
        panel_cols = 12
        size = self.get_panel_size_by_grid(panel_cols, panel_rows)
        pos = Vector2(EDITOR_SCREEN_RECT.w / 2 - size.x/2, EDITOR_SCREEN_RECT.h / 2 - size.y / 2)
        super().__init__(pos, size, title)
        self.on_confirm = on_confirm
        if on_cancel:
            self.on_cancel.append(on_cancel)
        self.title = title 

        self.btn_confirm = Button("Confirm", self.grid_pos(0,0), self.grid_size())
        self.btn_confirm.on_button_1.append(self.on_btn_confirm)
        self.em.add(self.btn_confirm)

        self.btn_cancel = Button("Cancel", self.grid_pos(6,0), self.grid_size())
        self.btn_cancel.on_button_1.append(self.on_btn_cancel)
        self.em.add(self.btn_cancel)

    def on_btn_confirm(self, btn):
        if self.on_confirm:
            self.close()
            self.on_confirm(btn)

    def on_btn_cancel(self, btn):
        self._cancel_button(btn)
        

class GuiEntity(Entity):
    def __init__(self, pos, size):
        super().__init__()
        self.type = EntityType.GUI
        self.frames = [
            pygame.Surface(size, pygame.SRCALPHA),
        ]
        self.pos = Vector2(pos)
        self._disabled = False
        self._hovered = False
        self._rect = None
        self.gui_layer = 0

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = value
        self.render()

    @property
    def rect(self):
        rect = self.get_rect()
        rect.topleft = self.pos + self.sprite_offset
        return rect 

    def render(self):
        """
        Default Pink Cube
        """
        self.surface.fill((255, 0, 255))


    def bjust_in_rect(self, rect, offset=0):
        surface_rect = self.get_rect()
        self.y = rect.h - surface_rect.h - self.sprite_offset.y - offset

    def tjust_in_rect(self, rect, offset=0):
        surface_rect = self.get_rect()
        self.y = rect.y + offset  - self.sprite_offset.y

    def rjust_in_rect(self, rect, offset=0):
        surface_rect = self.get_rect()
        self.x = rect.x + rect.w - offset - surface_rect.w + self.sprite_offset.x

    def ljust_in_rect(self, rect, offset=0):
        surface_rect = self.get_rect()
        self.x = rect.x + offset - self.sprite_offset.x

    def centerx_in_rect(self, rect):
        surface_rect = self.get_rect()
        self.pos.x = rect.centerx - (surface_rect.w/2) - self.sprite_offset.x

    def centery_in_rect(self, rect):
        surface_rect = self.get_rect()
        self.pos.y = rect.centery - (surface_rect.h/2) - self.sprite_offset.y

    def center_in_rect(self, rect):
        surface_rect = self.get_rect()
        self.pos.x = rect.centerx - (surface_rect.w/2) - self.sprite_offset.x
        self.pos.y = rect.centery - (surface_rect.h/2) - self.sprite_offset.y


class RubberBand(GuiEntity):
    def __init__(self, pos, size, label=None):
        super().__init__(pos, size)
        # self.min_value = min_value
        # self.max_value = max_value
        self._value = 0.5
        self._label = label

        self.font_color = (255, 255, 255)
        self.font_disabled_color = (80, 80, 80)
        self.label_color = (8, 134, 189)  # (127, 127, 127)
        self.label_hover_color = (7, 170, 170)
        self.label_disabled_color = (7, 77, 100)  # (60,60,60)
        self.background_color = (6, 86, 120)
        self.background_disabled_color = (2, 36, 51)
        self.background_hover_color = (5, 114, 161)
        self.border_color = (8, 134, 189)
        self.border_disabled_color = (7, 77, 110)

        self.dragging = False
        self.dragging_start_x = 0
        self.dragging_start_value = 0
        self.on_value_changed = []
        self.on_value_changing = []
        self.on_value_start = []

        self.render()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.render()

    def input_finished(self):
        # call backs
        for cb in self.on_value_changed:
            cb(self)

    def render(self):
        br = 5
        self.surface.fill((0, 0, 0))
        if self.disabled:
            c_txt = self.font_disabled_color
            c_bg = self.background_disabled_color
            c_brd = self.border_disabled_color
            c_lbl = self.label_disabled_color
        elif self.dragging == True:
            c_txt = self.font_color
            c_bg = self.background_hover_color
            c_lbl = self.label_hover_color
            c_brd = self.border_color
        else:
            c_txt = self.font_color
            if self._hovered:
                c_bg = self.background_hover_color
                c_lbl = self.label_hover_color
            else:
                c_lbl = self.label_color
                c_bg = self.background_color
            c_brd = self.border_color

        # Render Background and Border
        fill = pygame.Surface(self.get_rect().size, pygame.SRCALPHA)
        fill.fill((0, 0, 0, 0))
        pygame.draw.rect(fill, c_bg, self.get_rect(), 0, br)

        # self._value = 0.25
        r = self.get_rect()
        half = r.w / 2
        s = r.w * self._value
        if self._value < 0.5:
            w = half - s + 1
            area = pygame.Rect(0, 0, w, r.h)
            area.right = half
            self.surface.blit(fill, (s, 0), area)
        else:
            w = s - half 
            area = pygame.Rect(half, 0, w, r.h)
            self.surface.blit(fill, (half, 0), area)
                

        pygame.draw.rect(self.surface, c_brd, self.get_rect(), 1, br)


        #center line
        y1 = r.top
        y2 = r.bottom
        pygame.draw.line(self.surface, c_bg, (half, y1), (half, y2))

        # Render an uneditable Label
        x = 5
        y = 0
        if self._label:
            lbl = current_app.font.render(self._label, True, c_lbl)
            y = (self.get_rect().h / 2) - (lbl.get_rect().h / 2)
            self.surface.blit(lbl, (x, y))
            x += lbl.get_rect().w

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.dragging:
            speed_modifier = 1
            mpos_x = pygame.mouse.get_pos()[0]
            delta = self.dragging_start_x - mpos_x
            key_mods = pygame.key.get_mods()
            if key_mods & pygame.KMOD_SHIFT:
                speed_modifier = 4
            vd = delta / self.rect.w
            self._value = self.dragging_start_value - vd
            if self._value > 1.0:
                self._value = 1.0
            if self._value < 0.0:
                self._value = 0.0
            self.render()
            for cb in self.on_value_changing:
                v = self._value - 0.5
                cb(elapsed * speed_modifier, v * 2)

    def on_event(self, event, elapsed):
        if not self.disabled and current_scene.gui_layer <= self.gui_layer:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if not self.disabled:
                        self._hovered = True
                        self.render()
                elif self._hovered:
                    self._hovered = False
                    self.render()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos)
            ):
                if self.dragging == False:
                    self.dragging = True
                    self.dragging_start_x = event.pos[0]
                    self.dragging_start_value = self._value
                    for cb in self.on_value_start:
                        cb(self)
        
            if (
                event.type == pygame.MOUSEBUTTONUP
                and event.button == 1
                and self.dragging
            ):
                self.dragging = False
                self._value = 0.5
                self.input_finished()
                self.render()


class SlideValue(GuiEntity):
    def __init__(self, min_value, max_value, pos, size, label=None):
        super().__init__(pos, size)
        self.min_value = min_value
        self.max_value = max_value
        self._value = 0.0
        self._label = label

        self.font_color = (255, 255, 255)
        self.font_disabled_color = (80, 80, 80)
        self.label_color = (8, 134, 189)  # (127, 127, 127)
        self.label_hover_color = (7, 170, 170)
        self.label_disabled_color = (7, 77, 100)  # (60,60,60)
        self.background_color = (6, 86, 120)
        self.background_disabled_color = (2, 36, 51)
        self.background_hover_color = (5, 114, 161)
        self.border_color = (8, 134, 189)
        self.border_disabled_color = (7, 77, 110)

        self.dragging = False
        self.dragging_start_x = 0
        self.dragging_start_value = 0
        
        self.on_value_changed = []
        self.on_value_changing = []

        self.render()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.render()

    def input_finished(self):
        # call backs
        for cb in self.on_value_changed:
            cb(self)

    def render(self):
        br = 5
        self.surface.fill((0, 0, 0))
        if self.disabled:
            c_txt = self.font_disabled_color
            c_bg = self.background_disabled_color
            c_brd = self.border_disabled_color
            c_lbl = self.label_disabled_color
        elif self.dragging == True:
            c_txt = self.font_color
            c_bg = self.background_hover_color
            c_lbl = self.label_hover_color
            c_brd = self.border_color
        else:
            c_txt = self.font_color
            if self._hovered:
                c_bg = self.background_hover_color
                c_lbl = self.label_hover_color
            else:
                c_lbl = self.label_color
                c_bg = self.background_color
            c_brd = self.border_color

        # Render Background and Border
        fill = pygame.Surface(self.get_rect().size, pygame.SRCALPHA)
        fill.fill((0, 0, 0, 0))
        pygame.draw.rect(fill, c_bg, self.get_rect(), 0, br)
        w = self.get_rect().w * self._value
        area = pygame.Rect(0, 0, w, self.get_rect().h)
        self.surface.blit(fill, (0, 0), area)
        pygame.draw.rect(self.surface, c_brd, self.get_rect(), 1, br)

        # Render an uneditable Label
        x = 5
        y = 0
        if self._label:
            lbl = current_app.font.render(self._label, True, c_lbl)
            y = (self.get_rect().h / 2) - (lbl.get_rect().h / 2)
            self.surface.blit(lbl, (x, y))
            x += lbl.get_rect().w

        # Render the Actual Text, and handle Overage
        max_width = self.get_rect().w - x - 5
        txt = current_app.font.render(self.get_format_value(), True, c_txt)
        y = (self.get_rect().h / 2) - (txt.get_rect().h / 2)
        txt_rect = txt.get_rect()
        txt_rect.topleft = (x, y)
        if txt_rect.w > max_width:
            d = txt_rect.w - max_width
            area = pygame.Rect(d, 0, max_width, txt_rect.h)
        else:
            area = pygame.Rect(0, 0, txt_rect.w, txt_rect.h)
        self.surface.blit(txt, txt_rect, area)

    def get_format_value(self):
        return "{:.2f}".format(self.value)

    @property
    def value(self):
        d = self.max_value - self.min_value
        return (d * self._value) + self.min_value

    @value.setter
    def value(self, value):
        d = self.max_value - self.min_value
        v = value - self.min_value
        self._value = v / d
        self.render()

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.dragging:
            mpos_x = pygame.mouse.get_pos()[0]
            delta = self.dragging_start_x - mpos_x
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                delta = delta / 4
            vd = delta / self.rect.w
            self._value = self.dragging_start_value - vd
            if self._value > 1.0:
                self._value = 1.0
            if self._value < 0.0:
                self._value = 0.0
            self.render()
            for cb in self.on_value_changing:
                cb(self)

    def on_event(self, event, elapsed):
        if not self.disabled and current_scene.gui_layer <= self.gui_layer:
            pass
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if not self.disabled:
                        self._hovered = True
                        self.render()
                elif self._hovered:
                    self._hovered = False
                    self.render()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos)
            ):
                if self.dragging == False:
                    self.dragging = True
                    self.dragging_start_x = event.pos[0]
                    self.dragging_start_value = self._value
            if (
                event.type == pygame.MOUSEBUTTONUP
                and event.button == 1
                and self.dragging
            ):
                self.dragging = False
                self.input_finished()



class SlideValueInt(SlideValue):
    @property
    def value(self):
        d = self.max_value - self.min_value
        return int(round((d * self._value) + self.min_value, 0))

    @value.setter
    def value(self, value):
        d = self.max_value - self.min_value
        v = value - self.min_value
        self._value = v / d
        self.render()

    def get_format_value(self):
        return "{:0d}".format(self.value)



class TextBox(GuiEntity):
    def __init__(self, text, pos, size, label=None):
        super().__init__(pos, size)
        self.value = text

        self.font_color = (255, 255, 255)
        self.font_disabled_color = (80, 80, 80)
        self.label_color = (7, 131, 131)  # (127, 127, 127)
        self.label_hover_color = (7, 170, 170)
        self.label_disabled_color = (7, 70, 70)  # (60,60,60)
        self.background_color = (6, 55, 55)
        self.background_disabled_color = (2, 32, 32)
        self.background_hover_color = (8, 100, 100)
        self.border_color = (7, 131, 131)
        self.border_disabled_color = (7, 70, 70)

        self.user_input = False
        self.cursor_show = False
        self.cursor_elapsed = 0
        self.cursor_index = -1
        self._label = label
        self.on_value_changed = []
        self._old_value = ""
        self._edit_text = ""
        self.max_length = 42
        self.editable = True
        self.render()

    def tick(self, elapsed):
        if self.user_input:
            self.cursor_elapsed += elapsed
            if self.cursor_elapsed >= 400:
                self.cursor_elapsed = 0
                self.cursor_show = not self.cursor_show

    def deactivate(self):
        self.input_cancelled()

    @property
    def text(self):
        return self.value

    @text.setter
    def text(self, value):
        self.value = value
        self.render()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.render()

    def validate_text(self, text):
        return True

    def input_finished(self):
        self.user_input = False
        if not self.validate_text(self._edit_text):
            print("Invalid TextBox Value '{}'".format(self.value))
            self.value = self._old_value
        else:
            self.value = self.format_from_text(self._edit_text)
        self.gui_layer -= 1
        current_scene.gui_layer -= 1
        self.render()
        self.cursor_show = False
        # call backs
        for cb in self.on_value_changed:
            cb(self)

    def input_cancelled(self):
        if self.user_input:
            self.cursor_show = False
            self.user_input = False
            self.value = self._old_value
            self.gui_layer -= 1
            current_scene.gui_layer -= 1
            self.render()
            # call backs

    def render(self):
        br = 5
        self.surface.fill((0, 0, 0))
        if self.disabled:
            c_txt = self.font_disabled_color
            c_bg = self.background_disabled_color
            c_brd = self.border_disabled_color
            c_lbl = self.label_disabled_color
        elif self.user_input == True:
            c_txt = self.font_color
            c_bg = self.background_hover_color
            c_brd = self.border_color
            c_lbl = self.label_hover_color
        else:

            c_txt = self.font_color
            if self._hovered:
                c_bg = self.background_hover_color
                c_lbl = self.label_hover_color
            else:
                c_lbl = self.label_color
                c_bg = self.background_color
            c_brd = self.border_color

        # Render Baclground and Border
        pygame.draw.rect(self.surface, c_bg, self.get_rect(), 0, br)
        pygame.draw.rect(self.surface, c_brd, self.get_rect(), 1, br)

        # Render an uneditable Label
        x = 5
        y = 0
        if self._label:
            lbl = current_app.font.render(self._label, True, c_lbl)
            y = (self.get_rect().h / 2) - (lbl.get_rect().h / 2)
            self.surface.blit(lbl, (x, y))
            x += lbl.get_rect().w

        # Render the Actual Text, and handle Overage
        max_width = self.get_rect().w - x - 5
        txt = current_app.font.render(self._get_text(), True, c_txt)
        y = (self.get_rect().h / 2) - (txt.get_rect().h / 2)
        txt_rect = txt.get_rect()
        txt_rect.topleft = (x, y)
        # if txt_rect.w > max_width:

        cursor_back = (len(self._edit_text) - self.cursor_index) * 7
        d = txt_rect.w - max_width
        if cursor_back > max_width / 2:
            d -= (cursor_back - (max_width / 2))
        if d < 0:
            d = 0
        txt_rect.left -= d
        area = pygame.Rect(d, 0, max_width, txt_rect.h)
        # else:
        #     area = pygame.Rect(0, 0, txt_rect.w, txt_rect.h)
        self.surface.blit(txt, (x, y), area)
        self.cursor_pos = Vector2(txt_rect.right, 0) + Vector2(0, 4) + self.pos

    def _get_text(self):
        if self.user_input:
            return self._edit_text
        else:
            return self.format_to_text(self.value)

    def format_to_text(self, value):
        return value

    def format_from_text(self, text):
        return text

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        if self.cursor_show:
            pos = self.cursor_pos.copy()
            pos.x -= (len(self._edit_text) - self.cursor_index) * 7
            r = pygame.Rect(pos[0], pos[1], 2, 16)
            pygame.draw.rect(surface, (255, 255, 255), r, 0)

    def on_event(self, event, elapsed):
        if not self.disabled and current_scene.gui_layer <= self.gui_layer and self.editable == True:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if not self.disabled:
                        self._hovered = True
                        self.render()
                elif self._hovered:
                    self._hovered = False
                    self.render()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.user_input == False:
                    if self.rect.collidepoint(event.pos):
                        self.user_input = True
                        self._old_value = self.text
                        if self.value == None:
                            self._edit_text = ""
                        else:
                            self._edit_text = str(self.value)
                        self.cursor_index = len(self._edit_text)
                        self.gui_layer += 1
                        current_scene.gui_layer += 1
                        self.render()
                else:
                    if not self.rect.collidepoint(event.pos):
                        self.input_finished()
                        
                # else:
                    # self.user_input = False
                    # self.cursor_show = False
                self.render()
            if self.user_input == True and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Stop Editing
                    self.input_cancelled()
                    pass
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # Stop Editing
                    self.input_finished()
                    pass
                elif event.key == pygame.K_LEFT:
                    self.cursor_index -= 1
                    if self.cursor_index < 0:
                        self.cursor_index = 0
                    self.render()
                elif event.key == pygame.K_RIGHT:
                    self.cursor_index += 1
                    if self.cursor_index > len(self._edit_text):
                        self.cursor_index = len(self._edit_text)
                    self.render()
                # Check for backspace
                elif event.key == pygame.K_BACKSPACE:
                    if self.cursor_index > 0:
                        self._edit_text = self._edit_text[:self.cursor_index - 1] + self._edit_text[self.cursor_index:]
                        self.cursor_index -= 1
                        self.render()
                # Check for delete
                elif event.key == pygame.K_DELETE:
                    if self.cursor_index < len(self._edit_text):
                        self._edit_text = self._edit_text[:self.cursor_index] + self._edit_text[self.cursor_index + 1:]
                        self.render()
                else:
                    if len(str(self.value)) < self.max_length:
                        if self.cursor_index == len(self._edit_text):
                            self._edit_text += event.unicode
                        else:
                            self._edit_text = self._edit_text[:self.cursor_index] + event.unicode + self._edit_text[self.cursor_index:]
                        if event.unicode:
                            self.cursor_index += 1
                        self.render()

class TextBoxInt(TextBox):
    def __init__(self, value, pos, size, label=None):
        # if type(value) not in [int, ]:
            # raise AttributeError("value not int")
        super().__init__(value, pos, size, label)

    def format_to_text(self, value):
        if self.user_input:
            return str(value)
        if type(value) == int:
            return "{:,d}".format(value)
        if value == None:
            return None
        raise AttributeError

    def format_from_text(self, text):
        return int(text)

    def validate_text(self, text):
        try:
            v = int(text)
        except:
            return False
        return True

class TextBoxFloat(TextBox):
    def __init__(self, value, pos, size, label=None):
        if type(value) not in [float, int]:
            raise AttributeError("value not float")
        super().__init__(value, pos, size, label)

    def format_to_text(self, value):
        if self.user_input:
            return str(value)
        if type(value) == float:
            return "{:,.02f}".format(value)
        if type(value) == int:
            return "{:,d}".format(value)
        return ""
        raise AttributeError

    def format_from_text(self, text):
        if text == None:
            return None
        return float(text)

    def validate_text(self, text):
        try:
            v = float(text)
        except:
            return False
        return True
        

class Label(GuiEntity):
    def __init__(self, text, pos, size, align="left", background_color=None):
        super().__init__(pos, size)
        self._text = text

        self.font_color = (255, 255, 255)
        self.font_disabled_color = (80, 80, 80)
        self.background_color = background_color
        self._align = align
        self.valign = "middle"
        self.render()

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, value):
        self._align = value
        self.render()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render()

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = value
        self.render()

    def render(self):
        br = 5
        self.surface.fill((0, 0, 0,0))
        if self.disabled:
            c_lbl = self.font_disabled_color
        else:
            c_lbl = self.font_color
        c_bg = self.background_color
        # lbl = current_app.font.render(self._text, True, c_lbl)
        lbl = multi_line_text_render(self._text, current_app.font, c_lbl)
        if self.valign == "top":
            y = 0
        else:
            y = (self.get_rect().h / 2) - (lbl.get_rect().h / 2)
        if self._align == "right":
            x = self.get_rect().w - 5 - lbl.get_rect().w
        elif self._align == "center":
            x = (self.get_rect().w / 2) - 5 - (lbl.get_rect().w / 2)
        else:
            x = 5
        lpos = (x, y)
        if c_bg:
            pygame.draw.rect(self.surface, c_bg, self.get_rect(), 0, br)
        self.surface.blit(lbl, lpos)


class Button(GuiEntity):
    def __init__(self, text, pos, size, align="left"):
        super().__init__(pos, size)
        self.lbl = None
        self._text = None

        self._toggled = False

        self.font_color = (255, 255, 255)
        self.font_disabled_color = (80, 80, 80)
        self.font_toggled_color = (0, 0, 0)
        self.border_color = (180, 180, 180)
        self.border_disabled_color = (80, 80, 80)
        self.border_toggled_color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.background_hover_color = (40, 40, 40)
        self.background_toggled_color = (235, 235, 235)
        self.background_toggled_disabled_color = (127, 127, 127)
        self.background_toggled_hovered_color = (255, 255, 255)

        self._border_width = 1

        self._disabled = False
        self._hovered = False
        self._text = text
        self._align = align

        self.render()

        self.on_button_1 = []

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, value):
        self._align = value
        self.render()

    def render(self):
        br = 5
        self.surface.fill((0, 0, 0, 0))
        if self.disabled:
            if self._toggled:
                c_bg = self.background_toggled_disabled_color
            else:
                c_bg = self.background_color
            c_lbl = self.font_disabled_color
            c_brd = self.border_disabled_color
        else:
            if self._toggled:
                if self._hovered:
                    c_bg = self.background_toggled_hovered_color
                else:
                    c_bg = self.background_toggled_color
                c_lbl = self.font_toggled_color
                c_brd = self.border_toggled_color
            else:
                if self._hovered:
                    c_bg = self.background_hover_color
                else:
                    c_bg = self.background_color
                c_lbl = self.font_color
                c_brd = self.border_color

        # lbl = current_app.font.render(self._text, True, c_lbl)
        lbl = multi_line_text_render(self._text, current_app.font, c_lbl)
        if self._align == "right":
            x = self.get_rect().w - 5 - lbl.get_rect().w
        elif self._align == "center":
            x = (self.get_rect().w / 2) - (lbl.get_rect().w / 2)
        else:
            x = 5

        lpos = (x, (self.get_rect().h / 2) - (lbl.get_rect().h / 2))
        if c_bg:
            pygame.draw.rect(self.surface, c_bg, self.get_rect(), 0, br)
        pygame.draw.rect(self.surface, c_brd, self.get_rect(), self._border_width, br)
        self.surface.blit(lbl, lpos)

    @property
    def toggled(self):
        return self._toggled

    @toggled.setter
    def toggled(self, value):
        self._toggled = value
        self.render()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render()

    def on_event(self, event, elapsed):
        if not self.disabled and current_scene.gui_layer <= self.gui_layer:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self._hovered = True
                    self.render()
                elif self._hovered:
                    self._hovered = False
                    self.render()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos)
            ):
                if not self.disabled:
                    for cb in self.on_button_1:
                        cb(self)

class ButtonGraphic(Button):
    def __init__(self, image, text, pos, size, align="left"):
        self._image = image 
        super().__init__(text, pos, size, align=align)



    def render(self):
        br = 5
        self.surface.fill((0, 0, 0, 0))
        if self.disabled:
            if self._toggled:
                c_bg = self.background_toggled_disabled_color
            else:
                c_bg = self.background_color
            c_lbl = self.font_disabled_color
            c_brd = self.border_disabled_color
        else:
            if self._toggled:
                if self._hovered:
                    c_bg = self.background_toggled_hovered_color
                else:
                    c_bg = self.background_toggled_color
                c_lbl = self.font_toggled_color
                c_brd = self.border_toggled_color
            else:
                if self._hovered:
                    c_bg = self.background_hover_color
                else:
                    c_bg = self.background_color
                c_lbl = self.font_color
                c_brd = self.border_color

        if c_bg:
            pygame.draw.rect(self.surface, c_bg, self.get_rect(), 0, br)

        if self._image:
            image_rect = self._image.get_rect()
            image_rect.y = (self.get_rect().h / 2 - image_rect.h / 2)
        else:
            image_rect = pygame.Rect(0,0,0,0)

        lbl = current_app.font.render(self._text, True, c_lbl)
        lbl_y = (self.get_rect().h / 2) - (lbl.get_rect().h / 2)
        if self._align == "right":
            combined_width = image_rect.w + 5 + lbl.get_rect().w
            image_rect.x = self.get_rect().w - 5 - combined_width
            # lbl_x = self.get_rect().w - 5 - lbl.get_rect().w
        elif self._align == "center":
            if lbl.get_rect().w > 0:
                combined_width = image_rect.w + 5 + lbl.get_rect().w
            else:
                combined_width = image_rect.w
            start_x = (self.get_rect().w / 2) - (combined_width / 2)
            image_rect.x = start_x 
        else:
            image_rect.x = 5 
        
        lbl_x = image_rect.right + 5

        if self._image:
            self.surface.blit(self._image, image_rect)
        pygame.draw.rect(self.surface, c_brd, self.get_rect(), 1, br)
        self.surface.blit(lbl, (lbl_x, lbl_y))

    @property
    def image(self):
        return self._image 
    
    @image.setter
    def image(self, value):
        self._image = value 
        self.render()

class ButtonTimeCursor(Button):
    def __init__(self, text, pos, size, align="left"):
        super().__init__(text, pos, size, align)
        self.border_color = (80,80,80)
        self.background_color = None 
        self.render()

class ButtonEntityBadge(Button):
    def __init__(self, text, pos, size, align="left"):
        self._active = False
        self._selected = False
    
        # self.background_active_color = (180, 127, 127)
        # self.border_active_color = (80, 40, 40)
        # self.background_active_hover_color = (220, 127, 127)
        
    
        # self.background_selected_color = (90, 90, 197)
        # self.border_selected_color = (40, 40, 80)
        # self.background_selected_hover_color = (120, 120, 227)
        # self.border_selected_hover_color = (70, 70, 225)

        self.background_active_color = (90, 90, 197)
        self.border_active_color = (40, 40, 80)
        self.background_active_hover_color = (120, 120, 227)
        
    
        self.background_selected_color = (255, 127, 127)
        self.border_selected_color = (80, 40, 40)
        self.background_selected_hover_color = (225, 80, 80)
        self.border_selected_hover_color = (225, 0, 0)

        super().__init__(text, pos, size, align)
        self.font_color = (0, 0, 0)
        # self.font_toggled_color = (0, 0, 0)
        # self.border_toggled_color = (255, 255, 255)
        self.border_color = (40, 40, 40)
        self.border_hover_color = (255, 0, 0)
        
        self.background_color = (90, 90, 90)
        self.background_hover_color = (127, 127, 127)
        
        # self.background_toggled_color = (235, 235, 235)
        # self.background_toggled_hovered_color = (255, 255, 255)
        
        self.render()

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value):
        if self._selected != value:
            self._selected = value 
            self.render()


    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value):
        if self._active != value:
            self._active = value 
            self.render()

    def render(self):
        br = 5
        self.surface.fill((0, 0, 0, 0))
        if self._selected:
            if self._hovered:
                c_bg = self.background_selected_hover_color
                c_brd = self.border_selected_hover_color
            else:
                c_bg = self.background_selected_color
                c_brd = self.border_selected_color
            c_lbl = self.font_color
        else:
            if self._active:
                if self._hovered:
                    c_bg = self.background_active_hover_color
                    c_brd = self.border_hover_color
                else:
                    c_bg = self.background_active_color
                    c_brd = self.border_active_color
                c_lbl = self.font_color
            else:
                if self._hovered:
                    c_bg = self.background_hover_color
                    c_brd = self.border_hover_color
                else:
                    c_bg = self.background_color
                    c_brd = self.border_color
                c_lbl = self.font_color

        lbl = current_app.font.render(self._text, True, c_lbl)
        if self._align == "right":
            x = self.get_rect().w - 5 - lbl.get_rect().w
        elif self._align == "center":
            x = (self.get_rect().w / 2) - (lbl.get_rect().w / 2)
        else:
            x = 5

        lpos = (x, (self.get_rect().h / 2) - (lbl.get_rect().h / 2))
        if c_bg:
            pygame.draw.rect(self.surface, c_bg, self.get_rect(), 0, br)
        pygame.draw.rect(self.surface, c_brd, self.get_rect(), 1, br)
        self.surface.blit(lbl, lpos)


class TimelineSlider(GuiEntity):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        handle_width = 20

        self.render_handle(handle_width, size)
        self.render()

        self.handle_rect = self.handle.get_rect()
        self.slide_rect = pygame.Rect(
            self.pos.x + 2, self.pos.y + 2, size.x - 4 - handle_width, size.y - 4
        )
        self._value = 0
        self.update_handle_pos()

        self.dragging = False
        self.dragging_offset = 0
        self.on_value_change = []

    def render_handle(self, w, slide_size):
        self.handle = pygame.Surface((w, slide_size.y - 4))
        self.handle.fill((80, 80, 180))
        r = self.handle.get_rect()
        c1, c2 = (151, 151, 225), (5, 5, 155)
        s = self.handle
        pygame.draw.line(s, c1, (0, 0), (0, r.h))
        pygame.draw.line(s, c1, (0, 0), (r.w, 0))
        pygame.draw.line(s, c2, (0, r.h - 1), (r.w - 1, r.h - 1))
        pygame.draw.line(s, c2, (r.w - 1, 0), (r.w - 1, r.h - 1))

    def update_handle_pos(self):
        s = Vector2(self.slide_rect.topright)
        e = Vector2(self.slide_rect.topleft)
        self.handle_rect.topleft = Vector2.lerp(e, s, self._value)

    def render(self):
        self.surface.fill((110, 110, 110))
        r = self.get_rect()
        pygame.draw.line(self.surface, (80, 80, 80), (0, 0), (0, r.h))
        pygame.draw.line(self.surface, (80, 80, 80), (0, 0), (r.w, 0))
        pygame.draw.line(
            self.surface, (220, 220, 220), (0, r.h - 1), (r.w - 1, r.h - 1)
        )
        pygame.draw.line(
            self.surface, (220, 220, 220), (r.w - 1, 0), (r.w - 1, r.h - 1)
        )
        # pygame.draw.rect(self.surface, (255,255,255), self.get_rect(), 1)

    def on_event(self, event, elapsed):
        if not self.disabled and current_scene.gui_layer <= self.gui_layer:
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.handle_rect.collidepoint(event.pos)
            ):
                self.dragging = True
                self.dragging_offset = self.handle_rect.x - event.pos[0]
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos)
            ):
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.value = self.get_value_from_mouse(event.pos)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
                self.dragging = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value  < 0:
            value = 0
        elif value > 1.0:
            value = 1.0
        self._value = value
        self.update_handle_pos()
        # Do Call Backs
        for cb in self.on_value_change:
            cb(self)

    def set_value(self, value):
        """
        Set Value without triggering callbacks, and update handle positions
        """

        if value  < 0:
            value = 0
        elif value > 1.0:
            value = 1.0
        # if value < 0 or value > 1.0:
            # raise AttributeError
        self._value = value
        self.update_handle_pos()

    def get_value_from_mouse(self, mpos):
        v = (mpos[0] + self.dragging_offset - self.slide_rect.x) / (self.slide_rect.w)
        if v > 1:
            v = 1
        if v < 0:
            v = 0
        return v

    def tick(self, elapsed):
        super().tick(elapsed)
        if self.dragging:
            mpos = pygame.mouse.get_pos()
            self.value = self.get_value_from_mouse(mpos)
            

    def draw(self, elapsed, surface):
        super().draw(elapsed, surface)
        surface.blit(self.handle, self.handle_rect)

class ShowButton(ButtonGraphic):
    def __init__(self, pos, size, align="left"):
        text = ""
        image = editor_assets.sprites["icon show white"]
        super().__init__(image, text, pos, size, align)

    @property
    def toggled(self):
        return self._toggled

    @toggled.setter
    def toggled(self, value):
        if self._toggled != value:
            self._toggled = value 
            if self._toggled:
                self._image = editor_assets.sprites["icon show black"]
            else:
                self._image = editor_assets.sprites["icon show white"]
            self.render()
