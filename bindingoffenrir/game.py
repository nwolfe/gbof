import sys
import pygame as pg
import bindingoffenrir.settings as settings
import bindingoffenrir.debug as debug
import bindingoffenrir.fullscreen as fullscreen
import bindingoffenrir.level as level
import bindingoffenrir.images as images
import bindingoffenrir.sprites as sprites


class Game:
    def __init__(self):
        # pg.mixer.pre_init(44100, -16, 1 2048)
        pg.init()
        pg.display.set_caption(settings.TITLE)
        if fullscreen.ENABLED:
            self.screen = pg.display.set_mode(
                (settings.WIDTH, settings.HEIGHT), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(
                (settings.WIDTH, settings.HEIGHT))
        self.playing = False

        # Pausing
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # Clock / timing
        self.clock = pg.time.Clock()
        self.dt = None

        # Game state
        self.player = None
        self.paused = None

        # Resources from disk [see #_load_data()]
        self._levels = None
        self.level = None
        self._load_data()

    def _load_data(self):
        self._levels = level.get_all()
        self.level = self._levels.first()
        # self.level = level.get_sample()
        self.level.load()
        images.ALL.load()

    def new(self):
        self.paused = False
        self.player = sprites.Player(self)
        # self.level = self._levels.first()
        self.level.new(self)

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
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_F1:
                    debug.draw.grid = not debug.draw.grid
                if event.key == pg.K_F2:
                    debug.draw.hitboxes = not debug.draw.hitboxes
                if event.key == pg.K_F3:
                    debug.draw.physics = not debug.draw.physics
                if event.key == pg.K_F4:
                    debug.draw.version = not debug.draw.version
                if event.key == pg.K_F5:
                    debug.draw.points = not debug.draw.points

    def update(self):
        # Update all the objects in the current level
        self.level.update(self)

        # Player exiting the level? Go to the next level
        exit_ = pg.sprite.spritecollideany(self.player, self.level.exits)
        if exit_:
            if exit_.next_map and exit_.next_exit:
                self._next_level(exit_.next_map, exit_.next_exit)

        # Player fall off the bottom of the level? End the game
        if self.player.rect.top > settings.HEIGHT:
            self.player.kill()
            self.playing = False

    def _next_level(self, next_map, next_exit):
        next_level = self._levels.get(next_map)
        if next_level:
            next_level.load()
            next_level.new(self)
            next_level.place_at_exit(self.player, next_exit)
            self.level = next_level

    def draw(self):
        pg.display.set_caption("{} (FPS {:.2f})".format(
            settings.TITLE, self.clock.get_fps()))

        self.screen.fill(settings.BGCOLOR)
        self.level.draw(self.screen)
        debug.draw_all(self)

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))

        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass
