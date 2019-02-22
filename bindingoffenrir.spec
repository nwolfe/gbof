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
CODE = ['bindingoffenrir/main.py']

DEBUG = False
CONSOLE = DEBUG


# Write runtime options into executable.
# NOTE this is reverted at end of this file.
fullscreenfile = None
if os.getenv('FULLSCREEN') == 'true':
    fullscreenfile = os.path.join(NAME, 'fullscreen.py')
    with open(fullscreenfile, 'w') as f:
        f.write('ENABLED = True\n')


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

# Revert runtime options.
if fullscreenfile:
    with open(fullscreenfile, 'w') as f:
        f.write('ENABLED = False\n')
