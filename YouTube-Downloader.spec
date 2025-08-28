# -*- mode: python ; coding: utf-8 -*-

import os
import platform

block_cipher = None

# FFmpeg binary paths (you need to download FFmpeg first)
if platform.system() == "Windows":
    ffmpeg_path = "ffmpeg/bin/ffmpeg.exe"
    ffprobe_path = "ffmpeg/bin/ffprobe.exe"
else:
    ffmpeg_path = "ffmpeg/ffmpeg"
    ffprobe_path = "ffmpeg/ffprobe"

# Data files to include
datas = []
if os.path.exists(ffmpeg_path):
    datas.append((ffmpeg_path, 'ffmpeg'))
if os.path.exists(ffprobe_path):
    datas.append((ffprobe_path, 'ffmpeg'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtWidgets', 
        'PySide6.QtGui',
        'yt_dlp',
        'yt_dlp.extractor',
        'yt_dlp.downloader',
        'yt_dlp.postprocessor'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTube-Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon/download_medium_48x48.ico',
)
