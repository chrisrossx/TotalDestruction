from TD.scenes.levels.level import Level
from TD.enemies.PlaneT8 import EnemyPlaneT8
from .level_state import LevelState
from TD.pickups import PickupHeart, PickupCoin
    

class Level_001(Level):

    def __init__(self):
        super().__init__()


        t = 1000
        chain_1 = self.create_chain(EnemyPlaneT8, 0, t, 7, 500, {"velocity": 0.25})
        chain_1[2].drops = [PickupHeart]

        t += 1000
        chain_2 = self.create_chain(EnemyPlaneT8, 1, t, 7, 500, {"velocity": 0.25})

        t += 5000
        chain_2 = self.create_chain(EnemyPlaneT8, 2, t, 7, 500, {"velocity": 0.25})



    def create_chain(self, cls, path, start_time, count, spacing, attr):
        entities = []
        for i in range(count):
            entity = cls(path)
            # entity.delayed_start = i * spacing
            entities.append(entity)
            for key, value in attr.items():
                setattr(entity, key, value)
            t = start_time + (i * spacing)
            self.add_level_entity(t, entity)
        return entities
    

    def add_level_entity(self, time, entity):
        self.state_machines[LevelState.PLAYING].timed_add.append((time, entity))

