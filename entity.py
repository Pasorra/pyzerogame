from pgzero.actor import Actor
from map import ground_tiles
from constants import *


class Entity(Actor):
    def __init__(
        self,
        name: str,
        animation_dir: str,
        animations: dict[str, int],  # her animasyonun kaç kare olduğunu tutuyor
        pos: tuple,
        frame_speed: float,  # her kare kaç ms tutulacak
        has_gravity: bool,
        look_direction: str = "r",  # seçenekler sadece "r" ve "l"
        starting_state: str = "idle",
    ):
        self.name = name

        self.animation_dir = animation_dir
        self.animations = animations
        self.current_state = starting_state
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = frame_speed
        self.look_direction = look_direction
        self.frames = self._load_frames(self.current_state)

        self.velocity_x = 0
        self.velocity_y = 0
        self.has_gravity = has_gravity
        self.grounded = False
        super().__init__(self.frames[0], pos)

    def _load_frames(self, state: str) -> list[str]:
        return [
            f"{self.animation_dir}{self.name}_{state}_{i}_{self.look_direction}"
            for i in range(self.animations[state])
        ]

    def set_state(self, new_state: str):
        if new_state not in self.animations:
            return
        if new_state != self.current_state:
            self.current_state = new_state
            self.frame_index = 0
            self.frame_timer = 0

        # her durumda frameleri yeniden yükle
        self.frames = self._load_frames(new_state)

    def draw(self):
        self.image = self.frames[self.frame_index]
        super().draw()

    def update(self, delta: float):
        self.update_position(delta)
        self.update_sprites(delta)

    def update_sprites(self, delta: float) -> None:
        # hareket varsa state ve yön belirle
        if self.velocity_x > 0:
            self.look_direction = "r"
            self.set_state("run")
        elif self.velocity_x < 0:
            self.look_direction = "l"
            self.set_state("run")
        else:
            self.set_state("idle")

        self.frame_timer += delta
        # eğer zamanı geldiyse sonraki kareye geç
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def update_position(self, delta) -> None:
        # yer çekimi uygula
        if self.has_gravity:
            self.velocity_y += GRAVITY * delta

        self.y += self.velocity_y * delta

        for tile in ground_tiles:
            if self.colliderect(tile):
                if self.velocity_y > 0:  # ayağın yerle temasında
                    self.bottom = tile.top
                    self.grounded = True
                elif self.velocity_y < 0:  # kafanın tavasla temasında
                    self.top = tile.bottom
                self.velocity_y = 0

        self.x += self.velocity_x * delta
        for tile in ground_tiles:
            if self.colliderect(tile):
                if self.velocity_x > 0:  # sağda bir tile varsa
                    self.right = tile.left
                elif self.velocity_x < 0:  # solda bir tile varsa
                    self.left = tile.right
                self.velocity_x = 0

        # haritadan sağdan ve soldan çıkamasın
        if self.left < 0:
            self.left = 0
            self.velocity_x = 0
        elif self.right > WIDTH:
            self.right = WIDTH
            self.velocity_x = 0
