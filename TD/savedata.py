import json 

from blinker import signal 

from TD.config import SAVE_FILENAME


class SaveSlot:
    def __init__(self, file_data=None):
        self.name = None
        self.coins = 0
        self.level_state = {}

        if file_data != None:
            self.set_data(file_data)

    def get_level_(self, level):
        if level not in self.level_state.keys():
            self.level_state[level] = {
                "finished": False,
                "medalHeart": False,
                "medal70": False, 
                "medal100": False,
            }
        return self.level_state[level]

    @property
    def percent(self):
        return 0.42

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
        self.index = None
        self.muted = None
        for i in range(8):
            item = SaveSlot()
            self.slots.append(item)

        self.load()
        signal("savedata.save").connect(self.save)

    def load_failed(self):
        self.slots = []
        self.index = None
        self.muted = False
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
            self.muted = data["mute"]

        try:
            for i in range(8):
                slot = data["slots"][i]
                self.slots.append(SaveSlot(file_data = slot))
        except KeyError:
            self.load_failed()
                
    def save(self, *args, **kwargs):
        data = {
            "mute": signal("mixer.is_muted").send()[0][1],
            "slots": [s.get_data() for s in self.slots],
        }
        with open(self._file, "w") as f:
            json.dump(data, f, indent=2)

    @property
    def name(self):
        return self.slots[self.index].name

    @property
    def percent(self):
        return self.slots[self.index].percent

save_data = SaveData()
