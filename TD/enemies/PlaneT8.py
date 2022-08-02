from blinker import signal

from TD.assetmanager import asset_manager
from TD.paths import PathFollower


class EnemyPlaneT8:
    def __init__(self, pos):
        self.frames = [
            asset_manager.sprites["T8 001"],
            asset_manager.sprites["T8 002"],
            asset_manager.sprites["T8 003"],
            asset_manager.sprites["T8 004"],
        ]
        self.frame_index = 0
        self.frame_elapsed = 0

        self.velocity = -0.4


        self.path = PathFollower(0, (-32, -32))
        self.path.on_end_of_path.connect(self.on_end_of_path)
        self.path.velocity = 0.25
        self.deleted = False

    def draw(self, elapsed, surface):
        self.frame_elapsed += elapsed
        if self.frame_elapsed >= 25:
            self.frame_elapsed = 0
            self.frame_index += 1
            if self.frame_index == 4:
                self.frame_index = 0
        self.path.draw(elapsed, surface)
        surface.blit(self.frames[self.frame_index], (self.path.x, self.path.y))

    def tick(self, elapsed):
        self.path.tick(elapsed)

    def delete(self):
        self.deleted = True 
        signal("scene.delete_enemy").send(self)

    def on_end_of_path(self, sender):
        self.delete()

