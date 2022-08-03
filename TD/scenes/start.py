from enum import Enum

import pygame
from blinker import signal

from TD.player import PlayerShip
from TD.enemies.PlaneT8 import EnemyPlaneT8
from TD.backgrounds import Sky
from TD.debuging import game_debugger

from TD.states import State


class StartScene:

    def __init__(self, size):

        self.font_96 = pygame.font.SysFont(None, 96)
        self.font_28 = pygame.font.SysFont(None, 28)
        self.surface = pygame.Surface(size)

        self.sky = Sky(size)

        self.state = State.NOT_STARTED

    def tick(self, elapsed):
        self.sky.tick(elapsed)

    def pressed(self, pressed, elapsed):
        pass

    def on_event(self, event, elapsed):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                signal("game.change_scene").send({
                    "sky_offset":self.sky.offset,
                    "scene": "play",
                    })

    def draw(self, elapsed):
        self.surface.fill((0,0,0))

        #fill background with Sky Texture
        self.sky.draw(elapsed, self.surface)

        line_b = self.font_96.render("[T]otal [D]estruction", True, (0,0,0))
        line_w = self.font_96.render("[T]otal [D]estruction", True, (255,255,255))

        
        rect = line_b.get_rect()
        x = (1024/2) - (rect.width/2)
        y = (600/2) - (rect.height/2)
        self.surface.blit(line_b, (x+5, y+5))
        self.surface.blit(line_w, (x, y))

        line = self.font_28.render("Press [space] to start", True, (55,55,155))
        rect = line.get_rect()
        x = (1024/2) - (rect.width/2)
        y = (600/2) - (rect.height/2) + 80
        self.surface.blit(line, (x, y))



