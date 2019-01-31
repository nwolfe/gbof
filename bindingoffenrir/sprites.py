import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        print(x, y)
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.pos = pg.Vector2(x, y)
        self.image = game.player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    # def update(self):
    #     pass
