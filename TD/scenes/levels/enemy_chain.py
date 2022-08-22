

def ChainGunFactory(gun_cls, *args, **kwargs):
    def factory():
        return gun_cls(*args, **kwargs)
    return factory


class EnemyChain:
    def __init__(self, level, start_time, *args, **kwargs):
        self.level = level
        self.args = args 
        self.kwargs = kwargs
        self.entities = []
        self.chain_lost = False
        self.start_time = start_time

        for i in range(self.count):
            entity = self.factory(*self.args, **self.kwargs)
            entity.chain = self
            self.entities.append(entity)

        for i, entity in enumerate(self.entities):
            time = self.start_time + (i * self.spacing)
            self.level.add_level_entity(time, entity)

    def __getitem__(self, index):
        return self.entities[index]

    def set_guns(self, gun_factory, which=None):
        
        for i, entity in enumerate(self.entities):
            gun = gun_factory()
            if which != None:
                if i in which:
                    entity.set_gun(gun)
            else:
                entity.set_gun(gun)


    def add_drops(self, drops, which=None):
        for i, entity in enumerate(self.entities):
            if which != None:
                if i in which:
                    entity.drops = drops
            else:
                entity.drops = drops
