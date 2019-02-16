# -*- mode: python -*-
#
# To build executable: $ pyinstaller bindingoffenrir.spec


# Write build / version information into executable.
import os
import datetime
builddatefile = os.path.join('resources', 'builddate')
with open(builddatefile, 'w') as f:
    f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


NAME = 'bindingoffenrir'
ASSETS = [('resources', 'resources')]
CODE = [
    'bindingoffenrir/sprites/__init__.py',
    'bindingoffenrir/sprites/baddie.py',
    'bindingoffenrir/sprites/collisions.py',
    'bindingoffenrir/sprites/ground.py',
    'bindingoffenrir/sprites/player.py',
    'bindingoffenrir/sprites/spritesheet.py',
    'bindingoffenrir/sprites/stairs.py',
    'bindingoffenrir/game.py',
    'bindingoffenrir/geometry.py',
    'bindingoffenrir/main.py',
    'bindingoffenrir/resources.py',
    'bindingoffenrir/settings.py',
    'bindingoffenrir/tilemap.py'
]

DEBUG = False
CONSOLE = DEBUG

# PyInstaller configuration below

block_cipher = None
a = Analysis(CODE,
             pathex=['.'],
             binaries=[],
             datas=ASSETS,
             hiddenimports=['pygame'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=NAME,
          debug=DEBUG,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=CONSOLE)