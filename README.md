# Pygame Template

Starting point for creating a Python game using Pygame.

Add code, images, and sounds, then build into a single
executable using PyInstaller.

### How To Use

1. Clone repository
2. Delete `.git/` directory (so you can `git init`)
3. Replace `pgtemplate` with game name everywhere
4. Put images in a new `resources/img/` directory
5. Put sounds in a new `resources/snd/` directory
6. Install build dependencies: `pip install -r build-requirements.txt`
7. Install game dependencies: `pip install -r requirements.txt`
8. Build standalone executable: `make.sh build`
9. Clean build artifacts: `make.sh clean`
