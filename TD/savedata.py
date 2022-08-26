import json 

from TD.config import SAVE_FILENAME, NUMBER_OF_LEVELS
from TD.globals import current_app


class SaveSlot:
    def __init__(self, file_data=None):
        self.name = None
        self.coins = 0
        self.level_state = {}

        if file_data != None:
            self.set_data(file_data)

    def get_level(self, level):
        if type(level) == int:
            level = str(level)
        if level not in self.level_state.keys():
            # if level == 10:
            #     self.level_state[level] = {
            #         "finished": True,
            #         "medalHeart": True,
            #         "enemies": 1.0,
            #         "coins": 0.99,
            #     }
            # elif level == 1:
            #     self.level_state[level] = {
            #         "finished": False,
            #         "medalHeart": False,
            #         "enemies": 0.0,
            #         "coins": 1.0,
            #     }
            # else:
            self.level_state[level] = {
                "finished": False,
                "medalHeart": False,
                "enemies": 0.0,
                "coins": 0.0,
            }

        return self.level_state[level]

    def set_level(self, level, data):
        if type(level) == int:
            level = str(level)
        self.level_state[level] = {
            "finished": data["finished"],
            "medalHeart": data["medalHeart"],
            "enemies": data["enemies"],
            "coins": data["coins"],
        }

    @property
    def percent(self):
        score = 0
        for i in range(NUMBER_OF_LEVELS):
            data = self.get_level(i)
            pfinished = 1 if data["finished"] else 0
            p70 = 1 if data["enemies"] >= 0.7 else 0
            p100 = 1 if data["enemies"] >= 1.0 else 0
            pHealth = 1 if data["medalHeart"] else 0
            score += pfinished + p70 + p100 + pHealth

        return score / (4 * NUMBER_OF_LEVELS)


    def clear(self):
        self.name = None 
        self.coins = 0 
        self.level_state = {}        

    def set_data(self, data):
        self.name = data["name"]
        self.coins = data["coins"]
        self.level_state = data["level_state"]

    def get_data(self):
        return {
            "name": self.name,
            "coins": self.coins,
            "level_state": self.level_state
        }


class SaveData:
    def __init__(self) -> None:
        self._file = SAVE_FILENAME
        self.slots = []
        self._index = None
        self.sounds_muted = None
        self.music_muted = None
        for i in range(8):
            item = SaveSlot()
            self.slots.append(item)

        self.load()


    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, value):
        # print("Player Save Data Index Set", value)
        self._index = value

    def load_failed(self):
        self.slots = []
        self._index = None
        self.sounds_muted = False
        self.music_muted = False
        for i in range(8):
            item = SaveSlot()
            self.slots.append(item)

    def load(self):
        if not self._file.exists():
            self.load_failed()
            return 
        else:
            self.slots = []
            with open(self._file, "r") as f:
                data = json.load(f)
            self.sounds_muted = data["sounds_mute"]
            self.music_muted = data["music_mute"]

        try:
            for i in range(8):
                slot = data["slots"][i]
                self.slots.append(SaveSlot(file_data = slot))
        except KeyError:
            self.load_failed()
                
    def save(self, *args, **kwargs):
        data = {
            "sounds_mute": current_app.mixer.is_sounds_muted(),
            "music_mute": current_app.mixer.is_music_muted(),
            "slots": [s.get_data() for s in self.slots],
        }
        with open(self._file, "w") as f:
            json.dump(data, f, indent=2)

    def get_level_data(self, level_index):
        return self.slots[self._index].get_level(level_index)

    def set_level_data(self, level_index, data):
        return self.slots[self._index].set_level(level_index, data)

    @property
    def name(self):
        return self.slots[self._index].name

    @property
    def percent(self):
        return self.slots[self._index].percent
