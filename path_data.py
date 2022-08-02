from pathlib import Path
import json
import math

from config import PATHS_FILENAME

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
        item.points = [x for x in self.points]
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
        self._file = Path(PATHS_FILENAME)
        self._items = []
        for i in range(256):
            self._items.append(PathItem())

    def __getitem__(self, index):
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
