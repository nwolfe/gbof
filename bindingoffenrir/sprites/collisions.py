import pygame as pg
import bindingoffenrir.geometry as geometry


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
        return

    # Let the sprite jump up through the stairs; don't snap to stairs
    if sprite.vel.y < 0 and sprite.jump_point:
        pos = stairs.get_above_below_on(sprite.jump_point)
        if pos == 'below':
            sprite.on_stairs = False
            return

    # Snap bottom-right of sprite to diagonal stair line
    if stairs.is_right:
        p1 = sprite.rect.midbottom
        p2 = sprite.rect.bottomright
        p3 = stairs.rect.topright
        p4 = stairs.rect.bottomleft
        ip = geometry.calculateIntersectPoint(p1, p2, p3, p4)
        if ip:
            sprite.rect.bottomright = ip
            sprite.pos = sprite.rect.center
            sprite.vel.y = 0
            sprite.jump_point = None
            sprite.on_stairs = True
            return
    # Snap bottom-left of sprite to diagonal stair line
    elif stairs.is_left:
        p1 = sprite.rect.bottomleft
        p2 = sprite.rect.midbottom
        p3 = stairs.rect.topleft
        p4 = stairs.rect.bottomright
        ip = geometry.calculateIntersectPoint(p1, p2, p3, p4)
        if ip:
            sprite.rect.bottomleft = ip
            sprite.pos = sprite.rect.center
            sprite.vel.y = 0
            sprite.jump_point = None
            sprite.on_stairs = True
            return

    sprite.on_stairs = False
