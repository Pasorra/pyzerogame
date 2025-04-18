from entity import Entity


class Coin(Entity):

    def __init__(
        self,
        pos: tuple,
    ):
        super().__init__("coin", "coin/", {"idle": 12}, pos, 0.1, False)

        self.collected = False
