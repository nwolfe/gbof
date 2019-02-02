import pygame as pg
import bindingoffenrir.settings as settings


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.pos = pg.Vector2(x, y)
        self.image = game.player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._on_stairs = False

    def update(self):
        self._handle_keys()

    def _handle_keys(self):
        # Restrict movement while going up/down stairs
        if self._on_stairs:
            hit = pg.sprite.spritecollideany(self, self.game.stairs)
            if not hit:
                self._on_stairs = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # move left/back
            if not self._on_stairs:
                self.pos.x -= settings.PLAYER_SPEED
                self.rect.x = self.pos.x
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            # move right/forward
            if not self._on_stairs:
                self.pos.x += settings.PLAYER_SPEED
                self.rect.x = self.pos.x
        if keys[pg.K_UP] or keys[pg.K_w]:
            # go up stairs/ladder
            self._go_up_stairs()
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            # go down stairs/ladder; through platform
            if not self._on_stairs:
                pass
            pass
        if keys[pg.K_SPACE]:
            # jump up
            if not self._on_stairs:
                pass
            pass

    def _go_up_stairs(self):
        stairs = pg.sprite.spritecollideany(self, self.game.stairs)
        if stairs:
            # Only go up stairs if you're near the base of them
            if not self._on_stairs:
                if stairs.direction == 'right':
                    if self.pos.x < stairs.pos.x:
                        # print('less than')
                        pass
                    else:
                        # print('nope')
                        return
                elif stairs.direction == 'left':
                    pass
            # print(stairs.__dict__)
            # print('stairs: %s' % stairs.pos.x)
            # print(self.__dict__)
            # print('player: %s' % self.pos.x)
            self._on_stairs = True
            self.pos.y -= settings.PLAYER_STAIR_SPEED
            if stairs.direction == 'right':
                self.pos.x += settings.PLAYER_STAIR_SPEED
            elif stairs.direction == 'left':
                self.pos.x -= settings.PLAYER_STAIR_SPEED
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y


class Baddie(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites, game.baddies)
        self.game = game
        self.pos = pg.Vector2(x, y)
        self.image = game.enemy_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Stairs(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, direction):
        pg.sprite.Sprite.__init__(self, game.stairs)
        self.pos = pg.Vector2(x, y)
        self.rect = pg.rect.Rect(x, y, width, height)
        self.direction = direction
