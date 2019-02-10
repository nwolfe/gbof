import pygame as pg
import bindingoffenrir.settings as settings


class Baddie(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self._layer = settings.LAYER_BADDIE
        pg.sprite.Sprite.__init__(self, game.all_sprites, game.baddies)
        self.game = game
        self.pos = pg.Vector2(x, y)
        if direction == 'right':
            self.image = game.enemy_image_r.copy()
        elif direction == 'left':
            self.image = game.enemy_image_l.copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.direction = direction
