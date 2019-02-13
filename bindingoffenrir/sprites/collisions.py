import pygame as pg


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
            # Collision with bottom of object
            # (e.g. player jumping up and hitting their
            # head on the bottom of a platform)
            elif sprite.vel.y < 0:
                if sprite.rect.top < hit.rect.bottom:
                    sprite.rect.top = hit.rect.bottom
                    sprite.vel.y = 0
                    sprite.pos.y = sprite.rect.centery
