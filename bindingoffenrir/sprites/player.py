import pygame as pg
import bindingoffenrir.settings as settings


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.pos = pg.Vector2(x, y)
        self.image = game.player_images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
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
            self._go_down_stairs()
        if keys[pg.K_SPACE]:
            # jump up
            if not self._on_stairs:
                pass

    def _go_up_stairs(self):
        stairs = pg.sprite.spritecollideany(self, self.game.stairs)
        if stairs:
            # Only go up stairs if you're near the base of them
            if not self._on_stairs:
                if stairs.direction == 'right':
                    if self.pos.x >= stairs.pos.x:
                        return
                elif stairs.direction == 'left':
                    x = stairs.pos.x + stairs.rect.width - self.rect.width
                    if self.pos.x <= x:
                        return
            self._on_stairs = True
            self.pos.y -= settings.PLAYER_STAIR_SPEED
            if stairs.direction == 'right':
                self.pos.x += settings.PLAYER_STAIR_SPEED
            elif stairs.direction == 'left':
                self.pos.x -= settings.PLAYER_STAIR_SPEED
            self.rect.topleft = self.pos

    def _go_down_stairs(self):
        self.rect.y += 5
        stairs = pg.sprite.spritecollideany(self, self.game.stairs)
        self.rect.y -= 5
        if stairs:
            # Only go down stairs if you're near the top of them
            if not self._on_stairs:
                if stairs.direction == 'right':
                    x = stairs.pos.x + stairs.rect.width - self.rect.width
                    if self.pos.x <= x:
                        return
                elif stairs.direction == 'left':
                    if self.pos.x >= stairs.pos.x:
                        return
            self._on_stairs = True
            self.pos.y += settings.PLAYER_STAIR_SPEED
            if stairs.direction == 'right':
                self.pos.x -= settings.PLAYER_STAIR_SPEED
            elif stairs.direction == 'left':
                self.pos.x += settings.PLAYER_STAIR_SPEED
            self.rect.topleft = self.pos
