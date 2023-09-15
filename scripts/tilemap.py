import pygame

# dictionary = {} list = []

# in this instance the {} are being used in a "set" not a dictionary
PHYSICS_TILES = {"grass", "stone"}
NEIGHBOR_OFFSETS = [
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (0, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            # syntax for creating a horizontal line
            self.tilemap[str(3 + i) + ";10"] = {
                "type": "grass",
                "variant": 1,
                "pos": (3 + i, 10),
            }
            # syntax for creating a vertical line
            self.tilemap[";10" + str(5 + i)] = {
                "type": "stone",
                "variant": 1,
                "pos": (10, 5 + i),
            }

    def tiles_around(self, pos):
        tiles = []
        # convert pixel position to grid position // = int division chop off remainder
        # done for both the x and y axis remember 0 = x 1 = y
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            # here we are adding all the numbers in N_OF to base location so we get
            # 9 tiles surrounding to check for collision
            check_loc = (
                str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
            )
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    # function to filter near by tiles that have physics enabled
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            # itterating over all near by tiles
            if tile["type"] in PHYSICS_TILES:
                rects.append(
                    pygame.Rect(
                        tile["pos"][0] * self.tile_size,
                        tile["pos"][1] * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                )
        return rects

    # renderer for both tilemap dict and offgrid tiles list
    def render(self, surf):
        # if something is put first it renders first which means it will be on the
        # bottom of the layers. So e.g. we load the player last in the game.py
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile["type"]][tile["variant"]], tile["pos"])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size),
            )
