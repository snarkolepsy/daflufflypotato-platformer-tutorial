import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # nine neighbor tiles
# List of things we want to apply physics upon
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = [] # will be relevant in the level editor portion of the class later

        # EXAMPLE: a tilemap containing a row of horizontal grass tiles and the column of vertical stone tiles
        for i in range(10):
            # grass/1.png from grid position (x;y) 3;10 to 12;10
            self.tilemap[str(i + 3) + ';10'] = {'type' : 'grass', 'variant' : 1, 'pos' : (i + 3, 10)}
            # stone/1.png from grid position (x;y) 10;5 to 10;14
            self.tilemap['10;' + str(i + 5)] = {'type' : 'stone', 'variant' : 1, 'pos' : (10, i + 5)}

    def tiles_around(self, pos):
        """List the details of the surrounding tiles

        :param pos -- the tuple contain the pixel position of current central cell
        :return: a list of tiles and their properties
        """
        tiles = []

        # convert the pixel position into a GRID position
        tile_loc =(int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1]) # outputs X;Y
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surface):
        # Render the off-grid "decorative elements" first
        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        # Drawing the objects that will be used for collision and physics and logic
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
