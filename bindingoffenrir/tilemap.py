import pygame as pg
import pytmx
import bindingoffenrir.settings as settings


class TiledMap:
    def __init__(self, filename):
        self.tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tm.width * self.tm.tilewidth
        self.height = self.tm.height * self.tm.tileheight

    def make_map(self, game):
        s = pg.Surface((self.width, self.height))
        self._render(s)
        s.set_colorkey(settings.BLACK)
        return s

    def _render(self, surface):
        for layer in self.tm.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tm.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tm.tilewidth,
                                            y * self.tm.tileheight))
