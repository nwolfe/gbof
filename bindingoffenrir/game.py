import sys
import pygame as pg
import bindingoffenrir.settings as settings
import bindingoffenrir.resources as resources
from bindingoffenrir.tilemap import TiledMap
from bindingoffenrir.sprites import Player, Baddie


def load_image(filename, scale=None):
    i = pg.image.load(resources.image(filename)).convert_alpha()
    if scale:
        return pg.transform.scale(i, scale)
    else:
        return i


class Game:
    def __init__(self):
        # pg.mixer.pre_init(44100, -16, 1 2048)
        pg.init()
        pg.display.set_caption(settings.TITLE)
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.playing = False

        # Debugging
        self.draw_debug = False

        # Pausing
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # Clock / timing
        self.clock = pg.time.Clock()
        self.dt = None

        # Declarations only; see #new()
        self.player = None
        self.all_sprites = None
        self.baddies = None
        self.paused = None
        self.map_image = None
        self.map_rect = None

        # Resources from disk
        self.map = None
        self.player_image = None
        self.enemy_image = None
        self._load_data()

    def _load_data(self):
        self.map = TiledMap(resources.map(settings.SAMPLE_LEVEL))
        self.player_image = load_image(settings.PLAYER_IMAGE,
                                       scale=settings.SPRITE_SCALE)
        self.enemy_image = load_image(settings.ENEMY_IMAGE,
                                      scale=settings.SPRITE_SCALE)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.baddies = pg.sprite.Group()
        self.paused = False
        self.map_image = self.map.make_map(self)
        self.map_image = pg.transform.scale(self.map_image, settings.MAX_SCALE)
        self.map_rect = self.map_image.get_rect()
        self._create_tilemap_objects()

    def _create_tilemap_objects(self):
        for obj in self.map.tm.objects:
            obj.x *= settings.SCALE_FACTOR
            obj.y *= settings.SCALE_FACTOR
            if obj.name == 'player':
                self.player = Player(self, obj.x, obj.y)
            elif obj.name == 'baddie':
                Baddie(self, obj.x, obj.y)

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

    def draw(self):
        pg.display.set_caption("{} (FPS {:.2f})".format(
            settings.TITLE, self.clock.get_fps()))

        self.screen.fill(settings.BGCOLOR)
        # self.screen.blit(self.bgimg, (0, 0))
        self.screen.blit(self.map_image, self.map_rect)
        self.all_sprites.draw(self.screen)

        if self.draw_debug:
            # Draw outlines around all the collidable things, etc
            self._draw_grid()
            for s in self.all_sprites:
                if hasattr(s, 'rect'):
                    pg.draw.rect(self.screen, settings.CYAN, s.rect, 1)

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))

        pg.display.flip()

    def _draw_grid(self):
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, settings.LIGHTGREY,
                         (x, 0), (x, settings.HEIGHT))
        for y in range(0, settings.HEIGHT, settings.TILESIZE):
            pg.draw.line(self.screen, settings.LIGHTGREY,
                         (0, y), (settings.WIDTH, y))

    def quit(self):
        pg.quit()
        sys.exit()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass
