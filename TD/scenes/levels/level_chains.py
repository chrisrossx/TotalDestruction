from TD.scenes.levels.enemy_chain import EnemyChain
# from TD.enemies.D2 import EnemyD2
# from TD.enemies.CX5B import EnemyCX5B
# from TD.enemies.T8 import EnemyT8
# from TD.enemies.BT1 import EnemyBT1
from TD.enemies import * 


class T8Chain(EnemyChain):
    spacing = 600
    count = 5 
    enemy_class = EnemyT8
    def factory(self, path_index, gun=None):
        t8 = self.enemy_class(path_index)
        if gun:
            t8.set_gun(gun())
        return t8       


class CX5BChain(T8Chain):
    enemy_class = EnemyCX5B


class D2Chain(T8Chain):
    enemy_class = EnemyD2


class BT1Chain(T8Chain):
    count = 1
    enemy_class = EnemyBT1
