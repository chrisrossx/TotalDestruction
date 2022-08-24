
# class current_level():
#     pass 



class Level1:
    def __init__(self) -> None:
        self.name = "Level 1"

class Level2:
    """Whats Up Doc"""
    def __init__(self) -> None:
        self.name = "Level 2"


if __name__ == "__main__":
    from TD.globals import current_level
    # current_level = Proxy(Level1())
    # current_player = Proxy(Level2())
    print(current_level.__wrapped__)

    current_level.__wrapped__ = Level1()

    print(current_level.__wrapped__)


    # print(current_level.name, current_level.__class__, current_level.__doc__)
    # print(current_player.name, current_player.__class__, current_player.__doc__)
