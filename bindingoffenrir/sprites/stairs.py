import pygame as pg


class Stairs(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, direction):
        pg.sprite.Sprite.__init__(self, game.stairs)
        self.rect = pg.rect.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.direction = direction
        self.is_right = direction == 'right'
        self.is_left = direction == 'left'

    def get_above_below_on(self, point):
        """Tests where the point lies in relation to the diagonal
        line of the stairs. Returns 'above', 'below', or 'on'."""
        if self.is_right:
            line_a, line_b = self.rect.bottomleft, self.rect.topright
            xp = _cross_product(line_a, line_b, point)
            if xp > 0:
                return 'above'
            elif xp < 0:
                return 'below'
            else:
                return 'on'
        elif self.is_left:
            line_a, line_b = self.rect.bottomright, self.rect.topleft
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
    xA, yA = point[0], point[1]
    v1 = pg.Vector2(x2 - x1, y2 - y1)
    v2 = pg.Vector2(x2 - xA, y2 - yA)
    xp = v1.x * v2.y - v1.y * v2.x
    return xp
