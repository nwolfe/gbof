import pygame as pg


class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.rect.Rect(x, y, width, height)
        self.rect.centerx = x
        self.rect.centery = y
