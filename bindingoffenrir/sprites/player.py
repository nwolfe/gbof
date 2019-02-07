import pygame as pg
import bindingoffenrir.settings as settings


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game

        # Change velocity to change acceleration to change position.
        # The position changes based on the velocity and acceleration,
        # and the velocity changes based on the acceleration.
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        self.acc = pg.Vector2(0, 0)

        self.image = game.player_idle_images_r[0]
        self._current_frame = 0
        self._last_update = 0
        self._facing = 'right'

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self._on_stairs = False

    def update(self):
        self._animate()

        # Update logic moves the player by setting
        # the acceleration in the x,y directions
        self.acc = pg.Vector2(0, settings.PLAYER_GRAVITY)

        # Update player based on input
        self._handle_keys()

        # Apply friction, but only for left/right movement
        self.acc.x += self.vel.x * -settings.PLAYER_FRICTION

        # Equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + (0.5 * self.acc)

        # Don't walk off edge of screen
        if self.pos.x + self.rect.width >= self.game.map.width:
            self.pos.x = self.game.map.width - self.rect.width
        if self.pos.x < 0:
            self.pos.x = 0

        # Update our rectangle with our new position
        self.rect.topleft = self.pos

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
                self.acc.x = -settings.PLAYER_ACC
                self._facing = 'left'
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            # move right/forward
            if not self._on_stairs:
                self.acc.x = settings.PLAYER_ACC
                self._facing = 'right'
        if keys[pg.K_UP] or keys[pg.K_w]:
            # go up stairs/ladder
            self._go_up_stairs()
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            # go down stairs/ladder; through platform
            self._go_down_stairs()
        if keys[pg.K_SPACE]:
            # jump up
            if not self._on_stairs:
                self._jump()

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
            self.vel.y = -settings.PLAYER_STAIR_SPEED
            if stairs.direction == 'right':
                self.vel.x = settings.PLAYER_STAIR_SPEED
                self._facing = 'right'
            elif stairs.direction == 'left':
                self.vel.x = -settings.PLAYER_STAIR_SPEED
                self._facing = 'left'

    def _go_down_stairs(self):
        self.rect.y += 15
        stairs = pg.sprite.spritecollideany(self, self.game.stairs)
        self.rect.y -= 15
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
            self.vel.y = settings.PLAYER_STAIR_SPEED
            if stairs.direction == 'right':
                self.vel.x = -settings.PLAYER_STAIR_SPEED
                self._facing = 'right'
            elif stairs.direction == 'left':
                self.vel.x = settings.PLAYER_STAIR_SPEED
                self._facing = 'left'

    def _jump(self):
        self.rect.x += 1
        hit = pg.sprite.spritecollideany(self, self.game.ground)
        self.rect.x -= 1
        if hit:
            self.vel.y = -settings.PLAYER_JUMP

    def _animate(self):
        now = pg.time.get_ticks()
        # Walk animation
        if self.vel.x != 0:
            if now - self._last_update > 180:
                self._last_update = now
                if self.vel.x > 0:
                    self._use_frame_from(self.game.player_move_images_r)
                else:
                    self._use_frame_from(self.game.player_move_images_l)
        # Idle animation
        else:
            if now - self._last_update > 350:
                self._last_update = now
                if self._facing == 'right':
                    self._use_frame_from(self.game.player_idle_images_r)
                else:
                    self._use_frame_from(self.game.player_idle_images_l)

    def _use_frame_from(self, images):
        topleft = self.rect.topleft
        self._current_frame = (self._current_frame + 1) % len(images)
        self.image = images[self._current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
