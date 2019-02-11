import pygame as pg


class Stairs(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, direction):
        pg.sprite.Sprite.__init__(self, game.stairs)
        self.rect = pg.rect.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.direction = direction
