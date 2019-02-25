import pygame as pg
import bindingoffenrir.geometry as geometry
import bindingoffenrir.settings as settings
import bindingoffenrir.images as images


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = settings.LAYER_PLAYER
        pg.sprite.Sprite.__init__(self)
        self._game = game

        # Change velocity to change acceleration to change position.
        # The position changes based on the velocity and acceleration,
        # and the velocity changes based on the acceleration.
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0, 0)
        self.acc = pg.Vector2(0, 0)

        self.image = images.ALL.player_idle_images_r[0]
        self._current_frame = 0
        self._last_update = 0
        self._facing = 'right'

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.on_stairs = False
        self.stairs = None
        self.go_up_stairs = False

        self.jump_point = None
        self._last_jump = 0

    def set_position(self, x, y):
        self.pos.x = x
        self.pos.y = y
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self._animate()

        # Update logic moves the player by setting
        # the acceleration in the x,y directions
        self.acc = pg.Vector2(0, settings.PLAYER_GRAVITY)

        # Disable gravity when on the stairs to prevent sliding down
        if self.on_stairs:
            self.acc.y = 0

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
        if self.pos.x + (self.rect.width / 2) >= self._game.level.map.width:
            self.pos.x = self._game.level.map.width - (self.rect.width / 2)
        if self.pos.x - (self.rect.width / 2) < 0:
            self.pos.x = self.rect.width / 2

        # Check for collisions and move if necessary
        # Get the stairs that we're on / near so we can
        # ignore other tiles that overlap with the stairs,
        # giving us the ability to walk through tiles when
        # traversing stairs.
        if not self.stairs:
            stairs = pg.sprite.spritecollideany(self, self._game.level.stairs)
        else:
            stairs = self.stairs

        self.rect.centery = self.pos.y
        _collide_with_objects(self, self._game.level.ground, 'y', stairs)
        self.rect.centerx = self.pos.x
        _collide_with_objects(self, self._game.level.ground, 'x', stairs)

        _collide_with_stairs(self, stairs)

    def _handle_keys(self):
        keys = pg.key.get_pressed()
        left = keys[pg.K_LEFT] or keys[pg.K_a]
        right = keys[pg.K_RIGHT] or keys[pg.K_d]
        up = keys[pg.K_UP] or keys[pg.K_w]
        down = keys[pg.K_DOWN] or keys[pg.K_s]
        if left:
            # move left/back
            self.acc.x = -settings.PLAYER_ACC
            self._facing = 'left'
            # move up stairs by walking into them
            if self.on_stairs:
                self.vel.y = -settings.PLAYER_STAIR_SPEED
        if right:
            # move right/forward
            self.acc.x = settings.PLAYER_ACC
            self._facing = 'right'
            # move up stairs by walking into them
            if self.on_stairs:
                self.vel.y = -settings.PLAYER_STAIR_SPEED
        # if up: flag the player and let stair collision do the rest
        self.go_up_stairs = up
        if down:
            # move down stairs
            if self.on_stairs:
                if self.stairs.is_right:
                    self.vel.y = settings.PLAYER_STAIR_SPEED
                    self.acc.x = settings.PLAYER_ACC
                    self._facing = 'left'
                elif self.stairs.is_left:
                    self.vel.y = settings.PLAYER_STAIR_SPEED
                    self.acc.x = -settings.PLAYER_ACC
                    self._facing = 'right'
            # fall through ground if we're above stairs
            else:
                self.rect.y += 1
                stairs = pg.sprite.spritecollideany(self, self._game.level.stairs)
                self.rect.y -= 1
                if stairs:
                    # and completely within the right half of the stairs
                    if stairs.is_right:
                        s = stairs.rect
                        p = self.rect
                        if (s.centerx < p.left) and (p.right < s.right):
                            self.on_stairs = True
                            self.stairs = stairs
                    # or complete within the left half of the stairs
                    elif stairs.is_left:
                        s = stairs.rect
                        p = self.rect
                        if (s.left < p.left) and (p.right < s.centerx):
                            self.on_stairs = True
                            self.stairs = stairs

        if keys[pg.K_SPACE]:
            # jump up
            self._jump()

    def _jump(self):
        now = pg.time.get_ticks()
        if self.on_stairs:
            if now - self._last_jump > settings.PLAYER_JUMP_COOLDOWN:
                self._last_jump = now
                self.vel.y = -settings.PLAYER_JUMP_HEIGHT
                self.jump_point = self.rect.midbottom
                self._last_jump = pg.time.get_ticks()
        else:
            if now - self._last_jump > settings.PLAYER_JUMP_COOLDOWN:
                self.rect.y += 1
                hit = pg.sprite.spritecollideany(self, self._game.level.ground)
                self.rect.y -= 1
                if hit:
                    self._last_jump = now
                    self.vel.y = -settings.PLAYER_JUMP_HEIGHT
                    self.jump_point = self.rect.midbottom
                    self._last_jump = pg.time.get_ticks()

    def _animate(self):
        now = pg.time.get_ticks()
        # Walk animation
        if self.vel.x != 0:
            if now - self._last_update > 180:
                self._last_update = now
                if self._facing == 'right':
                    self._use_frame_from(images.ALL.player_move_images_r)
                else:
                    self._use_frame_from(images.ALL.player_move_images_l)
        # Idle animation
        else:
            if now - self._last_update > 350:
                self._last_update = now
                if self._facing == 'right':
                    self._use_frame_from(images.ALL.player_idle_images_r)
                else:
                    self._use_frame_from(images.ALL.player_idle_images_l)

    def _use_frame_from(self, image_frames):
        center = self.rect.center
        self._current_frame = (self._current_frame + 1) % len(image_frames)
        self.image = image_frames[self._current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = center


def _collide_with_objects(sprite, group, dir, stairs=None):
    if 'x' == dir:
        hit = pg.sprite.spritecollideany(sprite, group)
        if hit:
            # Special-case: ignore collisions when on stairs
            if stairs and hit.rect.colliderect(stairs.rect):
                return

            # Collision with left side of object
            # (e.g. player running to the right, into a platform)
            if sprite.vel.x > 0:
                if sprite.rect.right > hit.rect.left:
                    sprite.rect.right = hit.rect.left
                    sprite.vel.x = 0
                    sprite.pos.x = sprite.rect.centerx
            # Collision with right side of object
            # (e.g. player running to the left, into a platform)
            if sprite.vel.x < 0:
                if sprite.rect.left < hit.rect.right:
                    sprite.rect.left = hit.rect.right
                    sprite.vel.x = 0
                    sprite.pos.x = sprite.rect.centerx
    elif 'y' == dir:
        hit = pg.sprite.spritecollideany(sprite, group)
        if hit:
            # Special-case: ignore collisions when on stairs
            if stairs and hit.rect.colliderect(stairs.rect):
                return

            # Collision with top of object
            # (e.g. player falling down, onto a platform)
            if sprite.vel.y > 0:
                if sprite.rect.bottom > hit.rect.top:
                    sprite.rect.bottom = hit.rect.top
                    sprite.vel.y = 0
                    sprite.pos.y = sprite.rect.centery
                    sprite.jump_point = None
            # Collision with bottom of object
            # (e.g. player jumping up and hitting their
            # head on the bottom of a platform)
            elif sprite.vel.y < 0:
                if sprite.rect.top < hit.rect.bottom:
                    sprite.rect.top = hit.rect.bottom
                    sprite.vel.y = 0
                    sprite.pos.y = sprite.rect.centery


def _collide_with_stairs(sprite, stairs):
    """Test collision with a single stair sprite (not a spritegroup)."""
    if not stairs:
        sprite.on_stairs = False
        sprite.stairs = None
        return

    # If the sprite is *trying* to collide with the stairs to go up them,
    # then just see if their feet are close enough to the base of the stairs.
    if sprite.go_up_stairs and sprite.stairs is None:
        if stairs.is_right:
            distance = pg.Vector2(stairs.rect.bottomleft) - \
                       pg.Vector2(sprite.rect.bottomright)
        else:  # stairs.is_left
            distance = pg.Vector2(stairs.rect.bottomright) - \
                       pg.Vector2(sprite.rect.bottomleft)
        if distance.length() < 10:
            sprite.on_stairs = True
            sprite.stairs = stairs
            return

    # Let the sprite jump up through the stairs; don't snap to stairs
    if sprite.vel.y < 0 and sprite.jump_point:
        pos = _get_position_relative_to(sprite.jump_point, stairs)
        if 'below' == pos:
            sprite.on_stairs = False
            sprite.stairs = None
            return

    # Snap bottom-right of sprite to diagonal stair line
    if stairs.is_right:
        # Check if corner is on the line
        corner_on = False
        pos = _get_position_relative_to(sprite.rect.bottomright, stairs)
        if 'on' == pos:
            corner_on = True

        # Calculate intersection, if any
        intersect_point = None
        if not corner_on:
            p1 = sprite.rect.midbottom
            p2 = sprite.rect.bottomright
            p3 = stairs.rect.topright
            p4 = stairs.rect.bottomleft
            intersect_point = geometry.calculateIntersectPoint(p1, p2, p3, p4)

        if corner_on or intersect_point:
            if intersect_point:
                sprite.rect.bottomright = intersect_point
                sprite.pos.x = sprite.rect.centerx
                sprite.pos.y = sprite.rect.centery
            sprite.vel.y = 0
            sprite.jump_point = None
            sprite.on_stairs = True
            sprite.stairs = stairs
            return
    # Snap bottom-left of sprite to diagonal stair line
    elif stairs.is_left:
        # Check if corner is on the line
        corner_on = False
        pos = _get_position_relative_to(sprite.rect.bottomleft, stairs)
        if 'on' == pos:
            corner_on = True

        # Calculate intersection, if any
        intersect_point = None
        if not corner_on:
            p1 = sprite.rect.bottomleft
            p2 = sprite.rect.midbottom
            p3 = stairs.rect.bottomright
            p4 = stairs.rect.topleft
            intersect_point = geometry.calculateIntersectPoint(p1, p2, p3, p4)

        if corner_on or intersect_point:
            if intersect_point:
                sprite.rect.bottomleft = intersect_point
                sprite.pos.x = sprite.rect.centerx
                sprite.pos.y = sprite.rect.centery
            sprite.vel.y = 0
            sprite.jump_point = None
            sprite.on_stairs = True
            sprite.stairs = stairs
            return

    sprite.on_stairs = False
    sprite.stairs = None


def _get_position_relative_to(point, stairs):
    """Tests where the point lies in relation to the diagonal
    line of the stairs. Returns 'above', 'below', or 'on'."""
    if stairs.is_right:
        line_a, line_b = stairs.rect.bottomleft, stairs.rect.topright
        xp = _cross_product(line_a, line_b, point)
        if xp > 0:
            return 'above'
        elif xp < 0:
            return 'below'
        else:
            return 'on'
    elif stairs.is_left:
        line_a, line_b = stairs.rect.bottomright, stairs.rect.topleft
        xp = _cross_product(line_a, line_b, point)
        if xp > 0:
            return 'below'
        elif xp < 0:
            return 'above'
        else:
            return 'on'
    else:
        return None


# if xp > 0: above if right, below if left
# if xp < 0: below if right, above if left
# if xp = 0: on line
def _cross_product(line_a, line_b, point):
    x1, y1 = line_a[0], line_a[1]
    x2, y2 = line_b[0], line_b[1]
    xa, ya = point[0], point[1]
    v1 = pg.Vector2(x2 - x1, y2 - y1)
    v2 = pg.Vector2(x2 - xa, y2 - ya)
    xp = v1.x * v2.y - v1.y * v2.x
    return xp
