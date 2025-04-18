from map_data import bg_tilemap, ground_tilemap
from pgzero.actor import Actor
from constants import *

background_tiles = []
ground_tiles = []


for y in range(ROW_AMOUNT):
    for x in range(COL_AMOUNT):
        i = x + y * COL_AMOUNT
        tile_index = bg_tilemap[i]
        if tile_index != -1:
            tile = Actor(f"tiles/{tile_index}")
            tile.topleft = (x * TILE_SIZE, y * TILE_SIZE)
            background_tiles.append(tile)

        tile_index = ground_tilemap[i]
        if tile_index != -1:
            tile = Actor(f"tiles/{tile_index}")
            tile.topleft = (x * TILE_SIZE, y * TILE_SIZE)
            ground_tiles.append(tile)


def draw_map():
    for tile in background_tiles:
        tile.draw()

    for tile in ground_tiles:
        tile.draw()
