import os
import json
import pygame as pg
import bindingoffenrir.settings as settings


class MetadataStrategy:
    def get_coords(self, spritename):
        pass


# import xml.etree.ElementTree as xml
# class XmlMetadata(MetadataStrategy):
#     def __init__(self, filename):
#         self._xml = xml.parse(filename.replace('png', 'xml')).getroot()
#
#     def get_coords(self, spritename):
#         query = ".//SubTexture[@name='%s']" % spritename
#         props = self._xml.find(query).attrib
#         x = int(props['x'])
#         y = int(props['y'])
#         w = int(props['width'])
#         h = int(props['height'])
#         return (x, y, w, h)


class JsonMetadata(MetadataStrategy):
    def __init__(self, filename):
        self._name = os.path.basename(filename).replace('.png', '')
        with open(filename.replace('png', 'json')) as f:
            self._json = json.load(f)

    def get_coords(self, spritename):
        tag = self._get_frametag(spritename)
        metadata = self._json['frames'][tag]['frame']
        x = metadata['x']
        y = metadata['y']
        w = metadata['w']
        h = metadata['h']
        return (x, y, w, h)

    def _get_frametag(self, name):
        frame = None
        for t in self._json['meta']['frameTags']:
            if t['name'] == name:
                # Assume 'from' and 'to' are the same for now
                frame = t['from']
        return "%s %s.aseprite" % (self._name, frame)
        # return "spritesheet_frames %s.aseprite" % frame


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        try:
            self._metadata = JsonMetadata(filename)
        except Exception:
            self._metadata = None

    def get_image_at(self, x, y, width, height, scale=1):
        i = pg.Surface((width, height))
        i.blit(self.spritesheet, (0, 0), (x, y, width, height))
        i.set_colorkey(settings.TRANSPARENT)
        if scale > 1:
            r = i.get_rect()
            i = pg.transform.scale(i,  (r.width * scale, r.height * scale))
        return i

    def get_image(self, name, scale=1):
        coords = self._metadata.get_coords(name)
        return self.get_image_at(*coords, scale)

    def get_images(self, names, scale=1):
        return list(map(lambda i: self.get_image(i, scale), names))


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.pos = pg.Vector2(x, y)
        self.image = game.player_images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._on_stairs = False

    def update(self):
        self._handle_keys()

    def _handle_keys(self):
        # Restrict movement while going up/down stairs
        if self._on_stairs:
            hit = pg.sprite.spritecollideany(self, self.game.stairs)
            if not hit:
                self._on_stairs = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # move left/back
            if not self._on_stairs:
                self.pos.x -= settings.PLAYER_SPEED
                self.rect.x = self.pos.x
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            # move right/forward
            if not self._on_stairs:
                self.pos.x += settings.PLAYER_SPEED
                self.rect.x = self.pos.x
        if keys[pg.K_UP] or keys[pg.K_w]:
            # go up stairs/ladder
            self._go_up_stairs()
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            # go down stairs/ladder; through platform
            if not self._on_stairs:
                pass
        if keys[pg.K_SPACE]:
            # jump up
            if not self._on_stairs:
                pass

    def _go_up_stairs(self):
        stairs = pg.sprite.spritecollideany(self, self.game.stairs)
        if stairs:
            # Only go up stairs if you're near the base of them
            if not self._on_stairs:
                if stairs.direction == 'right':
                    if self.pos.x >= stairs.pos.x:
                        return
                elif stairs.direction == 'left':
                    x = stairs.pos.x + stairs.rect.width - self.rect.width
                    if self.pos.x <= x:
                        return
            self._on_stairs = True
            self.pos.y -= settings.PLAYER_STAIR_SPEED
            if stairs.direction == 'right':
                self.pos.x += settings.PLAYER_STAIR_SPEED
            elif stairs.direction == 'left':
                self.pos.x -= settings.PLAYER_STAIR_SPEED
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y


class Baddie(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites, game.baddies)
        self.game = game
        self.pos = pg.Vector2(x, y)
        self.image = game.enemy_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Stairs(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, direction):
        pg.sprite.Sprite.__init__(self, game.stairs)
        self.pos = pg.Vector2(x, y)
        self.rect = pg.rect.Rect(x, y, width, height)
        self.rect.topleft = (x, y)
        self.direction = direction
