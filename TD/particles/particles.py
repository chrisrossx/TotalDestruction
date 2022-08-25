from TD.entity import EntityType, Entity, EntityVectorMovement
from TD.assetmanager import asset_manager


class ParticleVectorMovement(EntityVectorMovement):
    def __init__(self, pos):
        super().__init__()
        self.type = EntityType.PARTICLE
        self.pos = pos.copy()


class ParticleEntityFollower(Entity):
    def __init__(self, follow_entity, follow_offset):
        super().__init__()
        self.follow_entity = follow_entity
        self.follow_offset = follow_offset
        self.type = EntityType.PARTICLE

    def tick(self, elapsed):
        super().tick(elapsed)
        if not self.follow_entity.deleted:
            self.pos = self.follow_entity.pos + self.follow_offset
        else:
            self.delete()
