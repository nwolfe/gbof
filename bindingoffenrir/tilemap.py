import pygame as pg
import pytmx
import bindingoffenrir.settings as settings


class TiledMap:
    def __init__(self, filename, scale=1):
        self.tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tm.width * self.tm.tilewidth
        self.height = self.tm.height * self.tm.tileheight
        self.scale = scale
        if scale > 1:
            self.width *= scale
            self.height *= scale

    def make_map(self, game):
        s = pg.Surface((self.width / self.scale, self.height / self.scale))
        self._render(s)
        s.set_colorkey(settings.TRANSPARENT)
        if self.scale > 1:
            r = s.get_rect()
            s = pg.transform.scale(s, (r.width * self.scale,
                                       r.height * self.scale))
        return s

    def _render(self, surface):
        for layer in self.tm.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tm.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tm.tilewidth,
                                            y * self.tm.tileheight))


class Camera:
    def __init__(self, mapwidth, mapheight):
        self._camera = pg.Rect(0, 0, mapwidth, mapheight)
        self._mapwidth = mapwidth
        self._mapheight = mapheight

    def apply(self, entity):
        return entity.rect.move(self._camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self._camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(settings.WIDTH / 2)
        y = -target.rect.centery + int(settings.HEIGHT / 2)
        # limit scrolling to map size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self._mapwidth - settings.WIDTH), x)
        y = max(-(self._mapheight - settings.HEIGHT), y)
        self._camera = pg.Rect(x, y, self._mapwidth, self._mapheight)
