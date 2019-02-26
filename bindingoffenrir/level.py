import pygame as pg
import bindingoffenrir.settings as settings
import bindingoffenrir.resources as resources
import bindingoffenrir.tilemap as tilemap
import bindingoffenrir.sprites as sprites


def get_sample():
    d, f = settings.SAMPLE_LEVEL
    return Level(f, resources.map(d, f))


def get_all():
    levels = []
    for d, fs in settings.LEVELS:
        for f in fs:
            name = f.strip('.tmx')
            path = resources.map(d, f)
            levels.append(Level(name, path))
    return Levels(levels)


class Level:
    def __init__(self, name, filename):
        self.name = name
        self._filename = filename
        self.map = None
        self.map_image = None
        self.map_rect = None
        self.camera = None

        self.all_sprites = None
        self.baddies = None
        self.stairs = None
        self.ground = None
        self.exits = None

    def load(self):
        self.map = tilemap.TiledMap(self._filename, settings.SCALE_FACTOR)

    def new(self, game):
        self.map_image = self.map.make_map(game)
        self.map_rect = self.map_image.get_rect()
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.baddies = pg.sprite.Group()
        self.stairs = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.exits = pg.sprite.Group()
        self._create_objects(game)

    def place_at_exit(self, player, exit_name):
        for e in self.exits:
            if e.name == exit_name:
                player.set_position(e.rect.x, e.rect.y)

    def _create_objects(self, game):
        player_spawn = None
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
                g = sprites.Ground.from_tiled_object(obj)
                g.add(self.ground)
            elif obj.name == 'player':
                player_spawn = (obj.x, obj.y)
            elif obj.name and obj.name.startswith('baddie'):
                b = sprites.Baddie.from_tiled_object(obj)
                b.add(self.all_sprites, self.baddies)
            elif obj.name and obj.name.startswith('stairs'):
                s = sprites.Stairs.from_tiled_object(obj)
                s.add(self.stairs)
            elif obj.name and obj.name.startswith('exit'):
                e = sprites.Exit.from_tiled_object(obj)
                e.add(self.exits)

        # Start player at the first exit by default
        if player_spawn is None:
            for e in self.exits:
                if e.name == 'exit1':
                    player_spawn = e.rect.center

        # Place the player at the entry to the level
        game.player.set_position(player_spawn[0], player_spawn[1])
        game.player.kill()  # Remove it from all previous groups
        game.player.add(self.all_sprites)

    def draw(self, screen):
        screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))

    def update(self, game):
        self.all_sprites.update()
        self.camera.update(game.player)


class Levels:
    def __init__(self, levels):
        self._levels = levels
        self.current = None

    def get(self, name):
        for level in self._levels:
            if level.name == name:
                return level
        return None

    def load(self, scale):
        for level in self._levels:
            level.load(scale)

    def first(self):
        return self._levels[0]
