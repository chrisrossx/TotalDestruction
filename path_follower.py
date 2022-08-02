import math
import json

import pygame 
import blinker

FILENAME = "line_editor.json"

class Lines:
    def __init__(self):
        self.waypoints = []
        for i in range(255):
            self.waypoints.append([])

        try:        
            with open(FILENAME, "r") as f:
                data = json.load(f)
            for i in range(255):
                try:
                    key = "waypoint_{}".format(i)
                    data[key].pop(0)
                    self.waypoints[i] = data[key]

                except KeyError:
                    pass
        except FileNotFoundError:
            pass

lines = Lines()

class PathFollower:
    def __init__(self, index, offset=(0,0)):
        self.x = 0
        self.y = 0
        self.offset = offset

        self._waypoints = lines.waypoints[index]
        self._start = []
        self._end = []
        self._length = []

        self.velocity = 0.1
        self.distance = 0

        self._calculated = False 
        self.calculate()
        self.on_path = False
        self.on_end_of_path = blinker.Signal()

    def calculate(self):
        self._start = []
        self._end = []
        self._length = []
        self._calculated = True 

        start = 0
        end = 0
        for i in range(len(self._waypoints)-1):
            p1 = self._waypoints[i]
            p2 = self._waypoints[i + 1]
            d = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            start = end 
            end = end + d
            self._start.append(start)
            self._end.append(end)
            self._length.append(d) 

    def add_waypoint(self, waypoint):
        self._waypoints.append(waypoint)
        self._calculated = False

    @property
    def pos(self):
        return self.x, self.y

    def draw(self, elapsed, surface):
        pygame.draw.lines(surface,(255,0,0),False, self._waypoints)
        if self.on_path:
            pygame.draw.circle(surface, (255, 0, 255), (self.x - self.offset[0], self.y - self.offset[1]), 5)

    def tick(self, elapsed):

        self.distance += elapsed * self.velocity
        self.on_path = False
        for i in range(len(self._waypoints)-1):
            start = self._start[i]
            end = self._end[i]
            if self.distance >= start and self.distance < end:
                d = self._length[i]
                p1 = self._waypoints[i]
                p2 = self._waypoints[i+1]
                t = (self.distance - start) / d
                self.x = ((1-t) * p1[0])  + (t * p2[0])
                self.y = ((1-t) * p1[1])  + (t * p2[1])
                self.x += self.offset[0]
                self.y += self.offset[1]
                self.on_path = True
                break
        
        if self.on_path == False:
            self.on_end_of_path.send()
