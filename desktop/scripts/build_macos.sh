#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

python3 -m venv .venv-build
source .venv-build/bin/activate
python -m pip install --upgrade pip
python -m pip install pyinstaller pillow python-docx reportlab

pyinstaller \
  --name "Rumba Reader" \
  --windowed \
  --noconfirm \
  --clean \
  --icon "assets/logo_1024.png" \
  --add-data "assets:assets" \
  --collect-all reportlab \
  --collect-all docx \
  app.py

echo "Build macOS terminé: $ROOT_DIR/dist/Rumba Reader.app"
