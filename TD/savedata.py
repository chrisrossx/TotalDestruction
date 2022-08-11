

class SaveSlot:
    def __init__(self):
        self.name = None
        self.percent = 0.0


class SaveData:
    def __init__(self) -> None:
        self.slots = []
        self.index = None
        for i in range(8):
            item = SaveSlot()
            self.slots.append(item)

    @property
    def name(self):
        return self.slots[self.index].name

    @property
    def percent(self):
        return self.slots[self.index].percent

save_data = SaveData()
