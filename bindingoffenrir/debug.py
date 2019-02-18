import pygame as pg
import bindingoffenrir.settings as settings
import bindingoffenrir.version as version


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
