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
