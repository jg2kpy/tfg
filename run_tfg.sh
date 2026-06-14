#!/bin/bash

MODE=${1:-original}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$SCRIPT_DIR/.venv"

# Buscar python del venv (WSL/Linux o Windows nativo)
if [ -f "$VENV/bin/python" ]; then
    PYTHON="$VENV/bin/python"
elif [ -f "$VENV/Scripts/python.exe" ]; then
    PYTHON="$VENV/Scripts/python.exe"
else
    echo "[ERROR] No se encontró el virtualenv en $VENV"
    echo "Crealo con: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

echo "Iniciando MODE='$MODE'..."
"$PYTHON" "$SCRIPT_DIR/src/RUN_TFG.py" $MODE > /dev/null 2>&1
echo "Finalizado con código de salida: $?"
