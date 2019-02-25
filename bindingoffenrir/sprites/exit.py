import pygame as pg


class Exit(pg.sprite.Sprite):
    @staticmethod
    def from_tiled_object(obj):
        return Exit(obj.x, obj.y, obj.width, obj.height,
                    obj.name, obj.properties)

    def __init__(self, x, y, width, height, name, properties):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.rect = pg.Rect(x, y, width, height)
        self.rect.centerx = x
        self.rect.centery = y
        self.next_map = properties.get('next_map', None)
        self.next_exit = properties.get('next_exit', None)
