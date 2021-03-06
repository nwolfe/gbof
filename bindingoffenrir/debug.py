import pygame as pg
import bindingoffenrir.settings as settings
import bindingoffenrir.version as version


class _Flags:
    def __init__(self):
        self.grid = False
        self.hitboxes = False
        self.physics = False
        self.points = False
        self.version = False


draw = _Flags()


def draw_all(game):
    if draw.grid:
        _draw_grid(game)
    if draw.hitboxes:
        _draw_rects(game, game.level.all_sprites)
        _draw_rects(game, game.level.stairs)
        _draw_rects(game, game.level.ground)
        _draw_rects(game, game.level.platforms)
        _draw_rects(game, game.level.exits, settings.GREEN)
        _draw_rects(game, game.level.spikes, settings.RED)
        _draw_stairs(game)
    if draw.version:
        _draw_version(game)
    if draw.physics:
        _draw_physics(game, [game.player])
    if draw.points:
        _draw_points(game, [game.player])


def _draw_points(game, group):
    size = 12
    font = pg.font.SysFont('Arial', size, bold=False)
    color = settings.GREEN
    for s in group:
        rect = game.level.camera.apply_rect(s.rect)

        # Center
        pos = rect.center
        surf = font.render("[%s, %s]" % (pos[0], pos[1]), True, color)
        r = surf.get_rect()
        r.midtop = rect.center
        game.screen.blit(surf, r)

        # Topleft
        pos = rect.topleft
        surf = font.render("[%s, %s]" % (pos[0], pos[1]), True, color)
        r = surf.get_rect()
        r.topright = rect.topleft
        game.screen.blit(surf, r)

        # Topright
        pos = rect.topright
        surf = font.render("[%s, %s]" % (pos[0], pos[1]), True, color)
        r = surf.get_rect()
        r.topleft = rect.topright
        game.screen.blit(surf, r)

        # Bottomleft
        pos = rect.bottomleft
        surf = font.render("[%s, %s]" % (pos[0], pos[1]), True, color)
        r = surf.get_rect()
        r.bottomright = rect.bottomleft
        game.screen.blit(surf, r)

        # Bottomright
        pos = rect.bottomright
        surf = font.render("[%s, %s]" % (pos[0], pos[1]), True, color)
        r = surf.get_rect()
        r.bottomleft = rect.bottomright
        game.screen.blit(surf, r)


def _draw_physics(game, group):
    size = 12
    font = pg.font.SysFont('Arial', size, bold=False)
    color = settings.GREEN
    for s in group:
        rect = game.level.camera.apply_rect(s.rect)

        # Position
        pos = s.pos
        surf = font.render("Pos: [{:.2f}, {:.2f}]".format(pos[0], pos[1]),
                           True, color)
        r = surf.get_rect()
        r.bottomleft = rect.topleft
        game.screen.blit(surf, r)

        # Velocity
        surf = font.render("Vel: %s" % s.vel, True, color)
        r = surf.get_rect()
        r.bottomleft = rect.topleft
        r.move_ip(0, size * -1)
        game.screen.blit(surf, r)

        # Acceleration
        surf = font.render("Acc: %s" % s.acc, True, color)
        r = surf.get_rect()
        r.bottomleft = rect.topleft
        r.move_ip(0, size * -2)
        game.screen.blit(surf, r)

        # On Stairs?
        surf = font.render("On Stairs: %s (%s)" % (s.on_stairs, s.stairs),
                           True, color)
        r = surf.get_rect()
        r.bottomleft = rect.topleft
        r.move_ip(0, size * -3)
        game.screen.blit(surf, r)

        # Jump Point
        if s.jump_point:
            m = "Jump Point: [%s, %s]" % (s.jump_point[0], s.jump_point[1])
        else:
            m = "Jump Point: None"
        surf = font.render(m, True, color)
        r = surf.get_rect()
        r.bottomleft = rect.topleft
        r.move_ip(0, size * -4)
        game.screen.blit(surf, r)


def _draw_version(game):
    build_date = "Built: %s" % version.BUILD_DATE
    font = pg.font.SysFont('Arial', 16, bold=True)
    surface = font.render(build_date, True, settings.GREEN)
    rect = surface.get_rect()
    rect.topleft = (0, 0)
    game.screen.blit(surface, rect)


def _draw_grid(game):
    for x in range(0, settings.WIDTH, settings.TILESIZE):
        pg.draw.line(game.screen, settings.LIGHTGREY,
                     (x, 0), (x, settings.HEIGHT))
    for y in range(0, settings.HEIGHT, settings.TILESIZE):
        pg.draw.line(game.screen, settings.LIGHTGREY,
                     (0, y), (settings.WIDTH, y))


def _draw_rects(game, group, color=settings.CYAN):
    for s in group:
        rect = game.level.camera.apply_rect(s.rect)
        pg.draw.rect(game.screen, color, rect, 1)
        pg.draw.circle(game.screen, settings.RED, rect.center, 3)
        pg.draw.circle(game.screen, settings.GREEN, rect.topleft, 3)
        pg.draw.circle(game.screen, settings.GREEN, rect.topright, 3)
        pg.draw.circle(game.screen, settings.GREEN, rect.bottomleft, 3)
        pg.draw.circle(game.screen, settings.GREEN, rect.bottomright, 3)


def _draw_stairs(game):
    for s in game.level.stairs:
        rect = game.level.camera.apply_rect(s.rect)
        if s.is_right:
            pg.draw.line(game.screen, settings.CYAN,
                         rect.bottomleft, rect.topright)
        elif s.is_left:
            pg.draw.line(game.screen, settings.CYAN,
                         rect.topleft, rect.bottomright)
