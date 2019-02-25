import pygame as pg
import bindingoffenrir.sprites as sprites
import bindingoffenrir.resources as resources
import bindingoffenrir.settings as settings


class Images:
    def __init__(self):
        self.spritesheet = None
        self.player_move_images_r = None
        self.player_move_images_l = None
        self.player_idle_images_r = None
        self.player_idle_images_l = None
        self.enemy_image_r = None
        self.enemy_image_l = None

    def load(self):
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
        self.enemy_image_r = _load_image(settings.ENEMY_IMAGE,
                                         scale=settings.SCALE_FACTOR)
        self.enemy_image_l = pg.transform.flip(self.enemy_image_r, True, False)


def _scale_image(image, scale):
    if type(scale) is tuple:
        return pg.transform.scale(image, scale)
    elif type(scale) is int:
        r = image.get_rect()
        s = (r.width * scale, r.height * scale)
        return pg.transform.scale(image, s)
    else:
        return image


def _load_image(filename, scale=None):
    i = pg.image.load(resources.image(filename)).convert_alpha()
    if scale:
        return _scale_image(i, scale)
    else:
        return i


ALL = Images()
