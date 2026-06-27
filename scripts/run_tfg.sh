#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV="$PROJECT_DIR/.venv"

if [ -f "$VENV/bin/python" ]; then
    PYTHON="$VENV/bin/python"
elif [ -f "$VENV/Scripts/python.exe" ]; then
    PYTHON="$VENV/Scripts/python.exe"
else
    echo "[ERROR] No se encontró el virtualenv en $VENV"
    echo "Crealo con: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

"$PYTHON" "$PROJECT_DIR/src/run_tfg.py" > /dev/null 2>&1
