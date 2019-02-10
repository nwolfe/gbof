import pygame as pg


class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        pg.sprite.Sprite.__init__(self, game.ground)
        self.rect = pg.rect.Rect(x, y, width, height)
        self.rect.center = pg.Vector2(x, y)
