import pygame as pg
import bindingoffenrir.settings as settings
import bindingoffenrir.version as version


def draw_physics(game, group):
    size = 12
    font = pg.font.SysFont('Arial', size, bold=False)
    color = settings.GREEN
    for s in group:
        rect = game.camera.apply_rect(s.rect)
        pos = s.pos
        # pos = rect.center
        acc = s.acc
        vel = s.vel

        surf = font.render("Pos: [%s, %s]" % (pos[0], pos[1]), True, color)
        r = surf.get_rect()
        r.bottomleft = rect.topleft
        game.screen.blit(surf, r)

        surf = font.render("Vel: %s" % vel, True, color)
        r = surf.get_rect()
        r.bottomleft = rect.topleft
        r = r.move(0, size * -1)
        game.screen.blit(surf, r)

        surf = font.render("Acc: %s" % acc, True, color)
        r = surf.get_rect()
        r.bottomleft = rect.topleft
        r = r.move(0, size * -2)
        game.screen.blit(surf, r)

        surf = font.render("On Stairs: %s" % s.on_stairs, True, color)
        r = surf.get_rect()
        r.bottomleft = rect.topleft
        r = r.move(0, size * -3)
        game.screen.blit(surf, r)


def draw_version(game):
    builddate = "Built: %s" % version.BUILD_DATE
    font = pg.font.SysFont('Arial', 16, bold=True)
    surface = font.render(builddate, True, settings.GREEN)
    rect = surface.get_rect()
    rect.topleft = (0, 0)
    game.screen.blit(surface, rect)


def draw_grid(game):
    for x in range(0, settings.WIDTH, settings.TILESIZE):
        pg.draw.line(game.screen, settings.LIGHTGREY,
                     (x, 0), (x, settings.HEIGHT))
    for y in range(0, settings.HEIGHT, settings.TILESIZE):
        pg.draw.line(game.screen, settings.LIGHTGREY,
                     (0, y), (settings.WIDTH, y))


def draw_rects(game, group):
    for s in group:
        rect = game.camera.apply_rect(s.rect)
        pg.draw.rect(game.screen, settings.CYAN, rect, 1)
        pg.draw.circle(game.screen, settings.RED, rect.center, 3)
        pg.draw.circle(game.screen, settings.GREEN, rect.topleft, 3)
        pg.draw.circle(game.screen, settings.GREEN, rect.topright, 3)
        pg.draw.circle(game.screen, settings.GREEN, rect.bottomleft, 3)
        pg.draw.circle(game.screen, settings.GREEN, rect.bottomright, 3)


def draw_stairs(game):
    for s in game.stairs:
        rect = game.camera.apply_rect(s.rect)
        if s.is_right:
            pg.draw.line(game.screen, settings.CYAN,
                         rect.bottomleft, rect.topright)
        elif s.is_left:
            pg.draw.line(game.screen, settings.CYAN,
                         rect.topleft, rect.bottomright)
