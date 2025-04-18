from entity import Entity
from constants import *


class Player(Entity):
    def __init__(self, pos: tuple[float, float]):
        animations = {
            "idle": 4,
            "run": 16,
        }
        super().__init__("knight", "knight/", animations, pos, 0.1, True)

        self.movement_speed = PLAYER_MOVEMENT_SPEED
        self.jump_speed = PLAYER_JUMP_SPEED

    def update(self, delta: float):
        if self.top > HEIGHT:  # oyuncu haritadan düşerse
            self.player_restart()
        super().update(delta)

    def handle_input(self, keys):
        if keys["left"]:
            self.velocity_x = -self.movement_speed
        elif keys["right"]:
            self.velocity_x = self.movement_speed
        else:
            self.velocity_x = 0

        if keys["jump"] and self.grounded:
            self.velocity_y = self.jump_speed
            self.grounded = False

    def player_restart(self):
        self.pos = PLAYER_INITIAL_POSITION
