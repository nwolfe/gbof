import pygame as pg


class Stairs(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, direction):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.rect.Rect(0, 0, width, height)
        self.rect.centerx = x
        self.rect.centery = y
        self.direction = direction
        self.is_right = direction == 'right'
        self.is_left = direction == 'left'
