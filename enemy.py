from entity import Entity
from constants import *


class Enemy(Entity):
    def __init__(
        self,
        name: str,
        animation_dir: str,
        animations: dict[str, int],
        pos: tuple[float, float],
        movement_speed: float,
    ):
        super().__init__(name, animation_dir, animations, pos, 0.1, True, "r", "run")

        self.initial_position = pos
        self.movement_speed = movement_speed

    # düşmanlar bir şeyle karşılasıya kadar hareketlerini koruyup sonra ters yönde giderler
    def update(self, delta: float):
        if self.velocity_x == 0:
            if self.look_direction == "r":
                self.velocity_x = -self.movement_speed
                self.look_direction = "l"
            else:
                self.velocity_x = self.movement_speed
                self.look_direction = "r"
        super().update(delta)
