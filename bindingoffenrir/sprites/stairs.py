import pygame as pg


class Stairs(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, direction):
        pg.sprite.Sprite.__init__(self, game.stairs)
        self.pos = pg.Vector2(x, y)
        self.rect = pg.rect.Rect(x, y, width, height)
        self.rect.topleft = self.pos
        self.direction = direction
