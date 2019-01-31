import pygame as pg
import pytmx


class TiledMap:
    def __init__(self, filename):
        self._tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self._tm.width * self._tm.tilewidth
        self.height = self._tm.height * self._tm.tileheight

    def make_map(self, game):
        s = pg.Surface((self.width, self.height))
        self._render(s)
        return s

    def _render(self, surface):
        for layer in self._tm.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self._tm.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self._tm.tilewidth,
                                            y * self._tm.tileheight))
