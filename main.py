### oyun başladığında otomatik olarak ekranın ortasına gelsin
import os

os.environ["SDL_VIDEO_CENTERED"] = "1"
###

import pgzrun
from pygame import Rect
from player import Player
from enemy import Enemy
import map
from constants import *
from coin import Coin

player = Player(PLAYER_INITIAL_POSITION)
enemies = [
    Enemy("green_slime", "enemies/", {"run": 4}, (TILE_SIZE * 12, TILE_SIZE * 13), 300),
    Enemy("purple_slime", "enemies/", {"run": 4}, (TILE_SIZE * 28, TILE_SIZE * 14), 50),
    Enemy("green_slime", "enemies/", {"run": 4}, (TILE_SIZE * 12, TILE_SIZE * 6), 300),
]

coins = [
    Coin(((TILE_SIZE * 11) + 16, (TILE_SIZE * 14) + 20)),
    Coin(((TILE_SIZE * 28) + 16, (TILE_SIZE * 14) + 20)),
    Coin(((TILE_SIZE * 11) + 16, (TILE_SIZE * 7) + 20)),
    Coin(((TILE_SIZE * 3) + 16, (TILE_SIZE * 4) + 20)),
]

menu_active = True
muted = False
game_won = False

buttons = {
    "oyna": Rect((WIDTH // 2 - 75, 240), (150, 40)),
    "çık": Rect((WIDTH // 2 - 75, 360), (150, 40)),
}
mute_button = Rect((WIDTH - 130, 10), (120, 40))
restart_button = Rect((WIDTH // 2 - 75, 380), (150, 40))


def draw():
    screen.clear()

    if menu_active:  # menüdeyken objektifi ve butonları göster
        screen.draw.text("Kazanmak için tüm altınları topla!", center=(WIDTH // 2, 100))
        for name, rect in buttons.items():
            screen.draw.filled_rect(rect, (167, 167, 167))
            screen.draw.text(name.capitalize(), center=rect.center)
    elif game_won:  # oyun sonunda tebrikler mesajıyla yeniden deneme butonunu göster
        screen.draw.text(
            "Tebrikler, kazandınız!",
            center=(WIDTH / 2, HEIGHT / 2 - 20),
            anchor=("center", "center"),
        )
        screen.draw.filled_rect(restart_button, (167, 167, 167))
        screen.draw.text("Yeniden Oyna", center=restart_button.center)
    else:  # oyun devam ederken öğeleri göster
        map.draw_map()
        for enemy in enemies:
            enemy.draw()
        for coin in coins:
            if not coin.collected:
                coin.draw()
        player.draw()

    # ses kontrolü düğmesini her zaman sağ üst köşede göster
    screen.draw.filled_rect(mute_button, (167, 167, 167))
    screen.draw.text("Sesi Kapa" if not muted else "Sesi Aç", center=mute_button.center)


def update(delta):
    global game_won, muted
    # Müzik durumu
    if not muted and not music.is_playing("bgm"):
        music.play("bgm")

    if menu_active or game_won:
        return

    # oyuncu hareketi
    keys = {
        "left": keyboard.left or keyboard.a,
        "right": keyboard.right or keyboard.d,
        "jump": keyboard.space or keyboard.up or keyboard.w,
    }
    player.handle_input(keys)
    player.update(delta)

    # düşman lojiği
    for enemy in enemies:
        enemy.update(delta)
        if enemy.colliderect(player):
            player.player_restart()
            if not muted:
                sounds.hurt.play()
            for coin in coins:
                coin.collected = False

    # coin lojiği
    for coin in coins:
        if not coin.collected and coin.colliderect(player):
            coin.collected = True
            if not muted:
                sounds.coin.play()

    # oyun kazanıldı mı kontrolü
    game_won = all(coin.collected for coin in coins)


# butonlara tıklama olayları
def on_mouse_down(pos):
    global menu_active, muted, game_won
    if mute_button.collidepoint(pos):
        muted = not muted
        if muted:
            music.stop()
        return

    if menu_active:
        if buttons["oyna"].collidepoint(pos):
            menu_active = False
        elif buttons["çık"].collidepoint(pos):
            exit()
    elif game_won and restart_button.collidepoint(pos):
        game_won = False
        player.player_restart()
        for coin in coins:
            coin.collected = False


pgzrun.go()
