import pygame as pg
import bindingoffenrir.settings as settings
import bindingoffenrir.images as images


class Baddie(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        self._layer = settings.LAYER_BADDIE
        pg.sprite.Sprite.__init__(self)
        self.pos = pg.Vector2(x, y)
        if direction == 'right':
            self.image = images.ALL.enemy_image_r.copy()
        elif direction == 'left':
            self.image = images.ALL.enemy_image_l.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.direction = direction
