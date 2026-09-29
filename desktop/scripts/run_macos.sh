#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv-local" ]; then
  python3 -m venv .venv-local
fi

source .venv-local/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
