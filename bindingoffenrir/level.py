import bindingoffenrir.settings as settings
import bindingoffenrir.resources as resources
import bindingoffenrir.tilemap as tilemap


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

    def load(self, scale):
        self.map = tilemap.TiledMap(self._filename, scale)

    def new(self, game):
        self.map_image = self.map.make_map(game)
        self.map_rect = self.map_image.get_rect()
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        # for exit in self.map.tm.get_layer_by_name('exit'):

    def draw(self, screen):
        screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))


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
