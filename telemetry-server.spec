# telemetry-server.spec
from PyInstaller.utils.hooks import collect_submodules
import sys
import os

block_cipher = None

a = Analysis(
    ['server/__main__.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    hiddenimports=[
        'encodings',
        'codecs',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='telemetry-server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='telemetry-server'
)