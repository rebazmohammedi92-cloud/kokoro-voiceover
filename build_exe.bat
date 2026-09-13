@echo off
REM ============================================================
REM  Builds kokoro_youtube_tts.py into a standalone Windows .exe
REM  Run this ONCE, on a machine where the script already runs
REM  correctly with "python kokoro_youtube_tts.py".
REM
REM  Afterward, the file in dist\KokoroVoiceover.exe can be
REM  copied to ANY Windows PC and double-clicked to run —
REM  no Python installation needed on that PC.
REM ============================================================

echo Installing required packages...
python -m pip install -U pyinstaller kokoro-onnx soundfile gradio numpy onnxruntime

echo.
echo Building KokoroVoiceover.exe (this can take several minutes)...
python -m PyInstaller ^
  --name KokoroVoiceover ^
  --onefile ^
  --console ^
  --icon "icon.ico" ^
  --collect-all gradio ^
  --collect-all gradio_client ^
  --collect-all kokoro_onnx ^
  --collect-all onnxruntime ^
  --collect-all numpy ^
  --collect-all soundfile ^
  --add-data "kokoro-v1.0.onnx;." ^
  --add-data "voices-v1.0.bin;." ^
  --add-data "icon.ico;." ^
  kokoro_youtube_tts.py

echo.
echo ============================================================
echo Done! Your standalone app is at: dist\KokoroVoiceover.exe
echo Copy that single file anywhere — it will run without Python.
echo.
echo Want a real installer (Start Menu + Desktop shortcut, uninstaller)?
echo Install Inno Setup, then compile installer.iss - see INSTALL_README.md.
echo ============================================================
pause
