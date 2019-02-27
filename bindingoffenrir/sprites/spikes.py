import pygame as pg


class Spikes(pg.sprite.Sprite):
    @staticmethod
    def from_tiled_object(obj):
        return Spikes(obj.x, obj.y, obj.width, obj.height)

    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(x, y, width, height)
        self.rect.centerx = x
        self.rect.centery = y
