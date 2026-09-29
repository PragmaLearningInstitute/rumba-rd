@echo off
setlocal

set ROOT_DIR=%~dp0..
cd /d %ROOT_DIR%

py -3 -m venv .venv-build
call .venv-build\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install pyinstaller pillow python-docx reportlab

pyinstaller ^
  --name "Rumba Reader" ^
  --windowed ^
  --noconfirm ^
  --clean ^
  --icon assets\logo_1024.png ^
  --add-data "assets;assets" ^
  --collect-all reportlab ^
  --collect-all docx ^
  app.py

echo Build Windows termine: %ROOT_DIR%\dist\Rumba Reader\Rumba Reader.exe
endlocal
