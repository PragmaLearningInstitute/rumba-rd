@echo off
setlocal

set ROOT_DIR=%~dp0..
cd /d %ROOT_DIR%

if not exist .venv-local (
  py -3 -m venv .venv-local
)

call .venv-local\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py

endlocal
