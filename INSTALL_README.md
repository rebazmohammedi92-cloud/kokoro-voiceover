> **Before you start:** put these 5 files in the same folder as your
> original `kokoro-v1.0.onnx` and `voices-v1.0.bin` (not included here —
> they're 300MB+, and you already have them from the original zip).

# Turning this into an installable app (Windows)

Everything here has to be built **on a Windows PC** (PyInstaller and Inno
Setup both produce Windows binaries only — they can't be cross-built from
another OS). Two steps, both one-click:

## Step 1 — Build the .exe

Double-click **`build_exe.bat`**. It installs PyInstaller, then bundles
`kokoro_youtube_tts.py`, the model files, and `icon.ico` into a single
file: `dist\KokoroVoiceover.exe`. It already has the mic icon baked in
(taskbar, title bar, and file icon).

You could stop here and just share that one `.exe` — it runs standalone,
no installer needed. But it won't show up in "Installed Apps" or the
Start Menu, and there's no uninstaller.

## Step 2 — Make it a real installer

For a proper install experience (Start Menu entry, optional desktop
shortcut, uninstaller, shows up in Windows' "Installed Apps" list):

1. Install **Inno Setup** (free): https://jrsoftware.org/isinfo.php
2. Open **`installer.iss`** in Inno Setup and click **Compile** (or
   right-click the file → Compile).
3. You'll get `installer_output\KokoroVoiceover-Setup.exe` — hand this
   single file to anyone, and double-clicking it installs the app like
   any normal Windows program, icon and all.

## What was added to the original files

- `icon.ico` — new mic-themed app icon (multi-resolution, for taskbar/
  Start Menu/exe).
- `build_exe.bat` — added `--icon "icon.ico"` and bundled the icon file
  so it's baked into the .exe.
- `kokoro_youtube_tts.py` — one added line so the browser tab also shows
  the icon as its favicon. No other logic touched.
- `installer.iss` — new Inno Setup script that wraps the built .exe into
  a proper Setup.exe installer.
