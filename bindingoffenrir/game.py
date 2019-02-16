import sys
import pygame as pg
import bindingoffenrir.settings as settings
import bindingoffenrir.resources as resources
import bindingoffenrir.sprites as sprites
import bindingoffenrir.version as version
from bindingoffenrir.tilemap import TiledMap, Camera


def scale_image(image, scale):
    if type(scale) is tuple:
        return pg.transform.scale(image, scale)
    elif type(scale) is int:
        r = image.get_rect()
        s = (r.width * scale, r.height * scale)
        return pg.transform.scale(image, s)
    else:
        return image


def load_image(filename, scale=None):
    i = pg.image.load(resources.image(filename)).convert_alpha()
    if scale:
        return scale_image(i, scale)
    else:
        return i


class Game:
    def __init__(self):
        # pg.mixer.pre_init(44100, -16, 1 2048)
        pg.init()
        pg.display.set_caption(settings.TITLE)
        self.screen = pg.display.set_mode(
            # (settings.WIDTH, settings.HEIGHT), pg.FULLSCREEN)
            (settings.WIDTH, settings.HEIGHT))
        self.playing = False

        # Debugging
        self.draw_debug = False

        # Pausing
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # Clock / timing
        self.clock = pg.time.Clock()
        self.dt = None

        # Object groups [declarations only; see #new()]
        self.player = None
        self.all_sprites = None
        self.baddies = None
        self.stairs = None
        self.ground = None

        # Game state [declarations only; see #new()]
        self.paused = None

        # Tilemap [declarations only; see #new()]
        self.map_image = None
        self.map_rect = None
        self.camera = None

        # Resources from disk [see #_load_data()]
        self.map = None
        self.spritesheet = None
        self.player_move_images_r = None
        self.player_move_images_l = None
        self.player_idle_images_r = None
        self.player_idle_images_l = None
        self.enemy_image_r = None
        self.enemy_image_l = None
        self._load_data()

    def _load_data(self):
        self.map = TiledMap(resources.map(settings.SAMPLE_LEVEL),
                            scale=settings.SCALE_FACTOR)
        self.spritesheet = sprites.Spritesheet(
            resources.image(settings.PLAYER_SPRITESHEET))
        self.player_move_images_r = self.spritesheet.get_images(
            settings.PLAYER_MOVE_IMAGES, scale=settings.SCALE_FACTOR)
        self.player_move_images_l = [
            pg.transform.flip(right_image, True, False)
            for right_image in self.player_move_images_r]
        self.player_idle_images_r = self.spritesheet.get_images(
            settings.PLAYER_IDLE_IMAGES, scale=settings.SCALE_FACTOR)
        self.player_idle_images_l = [
            pg.transform.flip(right_image, True, False)
            for right_image in self.player_idle_images_r]
        self.enemy_image_r = load_image(settings.ENEMY_IMAGE,
                                        scale=settings.SCALE_FACTOR)
        self.enemy_image_l = pg.transform.flip(self.enemy_image_r, True, False)

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.baddies = pg.sprite.Group()
        self.stairs = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.paused = False
        self.map_image = self.map.make_map(self)
        self.map_rect = self.map_image.get_rect()
        self.camera = Camera(self.map.width, self.map.height)
        self._create_tilemap_objects()

    def _create_tilemap_objects(self):
        for obj in self.map.tm.objects:
            # Scale the object up
            obj.x *= settings.SCALE_FACTOR
            obj.y *= settings.SCALE_FACTOR
            obj.width *= settings.SCALE_FACTOR
            obj.height *= settings.SCALE_FACTOR
            # Assume (x,y) is topleft and convert to center
            obj.x += obj.width / 2
            obj.y += obj.height / 2
            # Construct all the entities
            if obj.name == 'ground':
                sprites.Ground(self, obj.x, obj.y, obj.width, obj.height)
            elif obj.name == 'player':
                self.player = sprites.Player(self, obj.x, obj.y)
            elif obj.name == 'baddie_r':
                sprites.Baddie(self, obj.x, obj.y, 'right')
            elif obj.name == 'baddie_l':
                sprites.Baddie(self, obj.x, obj.y, 'left')
            elif obj.name == 'stairs_r':
                sprites.Stairs(self, obj.x, obj.y,
                               obj.width, obj.height, 'right')
            elif obj.name == 'stairs_l':
                sprites.Stairs(self, obj.x, obj.y,
                               obj.width, obj.height, 'left')

    def run(self):
        # pg.mixer_music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(settings.FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        pg.display.set_caption("{} (FPS {:.2f})".format(
            settings.TITLE, self.clock.get_fps()))

        self.screen.fill(settings.BGCOLOR)
        # self.screen.blit(self.bgimg, (0, 0))
        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        if self.draw_debug:
            # Draw outlines around all the collidable things, etc
            self._debug_draw_grid()
            self._debug_draw_rects(self.all_sprites)
            self._debug_draw_rects(self.stairs)
            self._debug_draw_rects(self.ground)
            self._debug_draw_stairs()
            self._debug_draw_version()

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))

        pg.display.flip()

    def _debug_draw_version(self):
        builddate = "Built: %s" % version.BUILD_DATE
        font = pg.font.SysFont('Arial', 16, bold=True)
        surface = font.render(builddate, True, settings.GREEN)
        rect = surface.get_rect()
        rect.topleft = (0, 0)
        self.screen.blit(surface, rect)

    def _debug_draw_grid(self):
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, settings.LIGHTGREY,
                         (x, 0), (x, settings.HEIGHT))
        for y in range(0, settings.HEIGHT, settings.TILESIZE):
            pg.draw.line(self.screen, settings.LIGHTGREY,
                         (0, y), (settings.WIDTH, y))

    def _debug_draw_rects(self, group):
        for s in group:
            rect = self.camera.apply_rect(s.rect)
            pg.draw.rect(self.screen, settings.CYAN, rect, 1)
            pg.draw.circle(self.screen, settings.RED, rect.center, 3)
            pg.draw.circle(self.screen, settings.GREEN, rect.topleft, 3)
            pg.draw.circle(self.screen, settings.GREEN, rect.topright, 3)
            pg.draw.circle(self.screen, settings.GREEN, rect.bottomleft, 3)
            pg.draw.circle(self.screen, settings.GREEN, rect.bottomright, 3)

    def _debug_draw_stairs(self):
        for s in self.stairs:
            rect = self.camera.apply_rect(s.rect)
            if s.is_right:
                pg.draw.line(self.screen, settings.CYAN,
                             rect.bottomleft, rect.topright)
            elif s.is_left:
                pg.draw.line(self.screen, settings.CYAN,
                             rect.topleft, rect.bottomright)

    def quit(self):
        pg.quit()
        sys.exit()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass
