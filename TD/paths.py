import json
import math

import blinker
import pygame

from TD.config import PATHS_FILENAME
from TD.utils import fast_round 


class PathItem:
    def __init__(self, name=None, data=None):
        self.points = []

        self.start = []
        self.end = []
        self.length = []
        self.total_length = 0.0

        self.name = name if name else "" 
        self.hidden = False 
        if data:
            self.set_data(data)

    def clear(self):
        self.points = []
        self.calculate()

    def calculate(self):
        self.start = []
        self.end = []
        self.length = []

        start = 0.0
        end = 0.0
        for i in range(len(self.points)-1):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            d = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            start = end 
            end = end + d
            self.start.append(start)
            self.end.append(end)
            self.length.append(d)      
        self.total_length = end   

    def duplicate(self):
        """return a copied item of path item"""
        item = PathItem()
        item.name = self.name
        item.hidden = self.hidden
        item.points = [[x[0], x[1]] for x in self.points]
        item.calculate()
        return item
    
    def set_data(self, data):
        self.name = data["name"]
        self.points = data["path"]
        self.hidden = data["hidden"]
        self.calculate()

    def get_data(self):
        return {
            "name": self.name,
            "path": self.points,
            "hidden": self.hidden,
        }

class PathData:
# JSON DATA STRUCTURE:
# [
#     {"name": "name 01",
#       "hidden": False,
#      "path": [(x0,y0), (x1, y1),],
#     },
#     {"name": "name 02",
#       "hidden": False,
#      "path": [(x0,y0), (x1, y1),],
#     },
# ]

    def __init__(self):
        self._file = PATHS_FILENAME
        self._items = []
        for i in range(256):
            self._items.append(PathItem())

    def __getitem__(self, index):
        # if type(index) == int:
            # return self._items[index]
        if type(index) == str:
            for i, path in enumerate(self._items):
                if path.name == index:
                    return self._items[i]

        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def save(self):
        #compile to json data
        data = []
        for i, item in enumerate(self._items):
            item_data = item.get_data()
            data.append(item_data)
        with open(self._file, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not self._file.exists():
            for i in range(256):
                self._items[i].name="PATHITEM {}".format(i)
        else:
            self._items = []
            with open(self._file, "r") as f:
                data = json.load(f)
            for i, item_data in enumerate(data):
                item = PathItem(data=item_data)
                self._items.append(item)

class PathFollower:
    def __init__(self, index):
        """
        @param index can by int or str: list index or path.name
        """
        # self.x = 0.0
        # self.y = 0.0
        self.pos = pygame.Vector2(0.0, 0.0)
        self.set_new_path(index)


        self.velocity = 0.1
        self.distance = 0
        self.on_path = False
        self.on_end_of_path = []

        #Update self.x and self.y to starting position
        self.tick(0)

    # @property
    # def pos(self):
        # return self.x, self.y
    
    def set_new_path(self, index):
        if type(index) == int:
            self.data = path_data[index]
        if type(index) == str:
            for path in path_data:
                if path.name == index:
                    self.data = path
                    break

    def draw(self, elapsed, surface):
        pygame.draw.lines(surface,(255,0,0), False, self.data.points)
        if self.on_path:
            pygame.draw.circle(surface, (255, 0, 255), self.pos, 5)

    def loop(self):
        
        step = self.data.total_length
        # if self.velocity >= 0:
            # step *= -1
        while True:
            if self.velocity >= 0:
                if self.distance < step:
                    break
                self.distance -= step
            else:
                if self.distance > 0:
                    break
                self.distance += step

            

    def tick(self, elapsed):
        self.distance += elapsed * self.velocity
        self.on_path = False
        for i in range(len(self.data.points)-1):
            start = self.data.start[i]
            end = self.data.end[i]
            if self.distance >= start and self.distance < end:
                d = self.data.length[i]
                p1 = self.data.points[i]
                p2 = self.data.points[i+1]
                t = (self.distance - start) / d
                self.pos.x = ((1-t) * p1[0])  + (t * p2[0])
                self.pos.y = ((1-t) * p1[1])  + (t * p2[1])
                self.on_path = True
                break
        
        if self.on_path == False:
            for cb in self.on_end_of_path:
                cb()
            # self.on_end_of_path.send()
        
        return self.pos


# Singleton Pattern - Stinky, but practical for a game environment
path_data = PathData()
path_data.load()
