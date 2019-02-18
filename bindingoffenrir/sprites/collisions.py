import pygame as pg
import bindingoffenrir.geometry as geometry


# if xp > 0: above if right, below if left
# if xp < 0: below if right, above if left
# if xp = 0: on line
def cross_product(line_a, line_b, point):
    x1, y1 = line_a[0], line_a[1]
    x2, y2 = line_b[0], line_b[1]
    xA, yA = point[0], point[1]
    v1 = pg.Vector2(x2 - x1, y2 - y1)
    v2 = pg.Vector2(x2 - xA, y2 - yA)
    xp = v1.x * v2.y - v1.y * v2.x
    return xp


def get_position_relative_to(point, stairs):
    """Tests where the point lies in relation to the diagonal
    line of the stairs. Returns 'above', 'below', or 'on'."""
    if stairs.is_right:
        line_a, line_b = stairs.rect.bottomleft, stairs.rect.topright
        xp = cross_product(line_a, line_b, point)
        if xp > 0:
            return 'above'
        elif xp < 0:
            return 'below'
        else:
            return 'on'
    elif stairs.is_left:
        line_a, line_b = stairs.rect.bottomright, stairs.rect.topleft
        xp = cross_product(line_a, line_b, point)
        if xp > 0:
            return 'below'
        elif xp < 0:
            return 'above'
        else:
            return 'on'
    else:
        return None


def collide_with_objects(sprite, group, dir):
    if 'x' == dir:
        hit = pg.sprite.spritecollideany(sprite, group)
        if hit:
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


def collide_with_stairs(sprite, stairsgroup):
    stairs = pg.sprite.spritecollideany(sprite, stairsgroup)
    if not stairs:
        sprite.on_stairs = False
        sprite.stairs = None
        return

    # Let the sprite jump up through the stairs; don't snap to stairs
    if sprite.vel.y < 0 and sprite.jump_point:
        pos = get_position_relative_to(sprite.jump_point, stairs)
        if 'below' == pos:
            sprite.on_stairs = False
            sprite.stairs = None
            return

    # Snap bottom-right of sprite to diagonal stair line
    if stairs.is_right:
        # Check if corner is on the line
        corner_on = False
        pos = get_position_relative_to(sprite.rect.bottomright, stairs)
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
                sprite.pos = sprite.rect.center
            sprite.vel.y = 0
            sprite.jump_point = None
            sprite.on_stairs = True
            sprite.stairs = stairs
            return
    # Snap bottom-left of sprite to diagonal stair line
    elif stairs.is_left:
        # Check if corner is on the line
        corner_on = False
        pos = get_position_relative_to(sprite.rect.bottomleft, stairs)
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
                sprite.pos = sprite.rect.center
            sprite.vel.y = 0
            sprite.jump_point = None
            sprite.on_stairs = True
            sprite.stairs = stairs
            return

    sprite.on_stairs = False
    sprite.stairs = None
