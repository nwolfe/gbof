import pygame as pg
import bindingoffenrir.settings as settings
from bindingoffenrir.sprites.collisions import collide_with_objects
from bindingoffenrir.sprites.collisions import collide_with_stairs


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = settings.LAYER_PLAYER
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
        self.rect.center = self.pos
        self.on_stairs = False

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
        if self.pos.x + (self.rect.width / 2) >= self.game.map.width:
            self.pos.x = self.game.map.width - (self.rect.width / 2)
        if self.pos.x - (self.rect.width / 2) < 0:
            self.pos.x = self.rect.width / 2

        # Check for collisions and move if necessary
        self.rect.centerx = self.pos.x
        collide_with_objects(self, self.game.ground, 'x')
        self.rect.centery = self.pos.y
        collide_with_objects(self, self.game.ground, 'y')

        collide_with_stairs(self, self.game.stairs)

    def _handle_keys(self):
        keys = pg.key.get_pressed()
        left = keys[pg.K_LEFT] or keys[pg.K_a]
        right = keys[pg.K_RIGHT] or keys[pg.K_d]
        # up = keys[pg.K_UP] or keys[pg.K_w]
        # down = keys[pg.K_DOWN] or keys[pg.K_s]
        if left:
            # move left/back
            self.acc.x = -settings.PLAYER_ACC
            self._facing = 'left'
            if self.on_stairs:
                self.vel.y = -settings.PLAYER_STAIR_SPEED
        if right:
            # move right/forward
            self.acc.x = settings.PLAYER_ACC
            self._facing = 'right'
            if self.on_stairs:
                self.vel.y = -settings.PLAYER_STAIR_SPEED

        if keys[pg.K_SPACE]:
            # jump up
            self._jump()

    def _jump(self):
        if self.on_stairs:
            self.vel.y = -settings.PLAYER_JUMP
        else:
            self.rect.y += 1
            hit = pg.sprite.spritecollideany(self, self.game.ground)
            self.rect.y -= 1
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
        center = self.rect.center
        self._current_frame = (self._current_frame + 1) % len(images)
        self.image = images[self._current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
