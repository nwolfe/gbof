import os
import sys


# Support running from single .exe (via PyInstaller)
if getattr(sys, 'frozen', False):
    _rootdir = sys._MEIPASS
else:
    _rootdir = os.getcwd()

RESOURCE_DIR = os.path.join(_rootdir, 'resources')
IMAGE_DIR = os.path.join(RESOURCE_DIR, 'img')
MAP_DIR = os.path.join(RESOURCE_DIR, 'map')


def image(file):
    return os.path.join(IMAGE_DIR, file)


def map(directory, file):
    return os.path.join(MAP_DIR, directory, file)
