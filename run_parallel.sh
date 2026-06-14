#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Uso: $0 <modo> <instancias>"
    echo "Ejemplo: $0 modified 3"
    exit 1
fi

MODE=$1
INSTANCES=$2
PIDS=()

echo "Lanzando $INSTANCES instancias con MODE='$MODE'..."

for i in $(seq 1 $INSTANCES); do
    ./run_tfg.sh $MODE &
    PID=$!
    PIDS+=($PID)
    echo "Instancia $i lanzada [PID=$PID]"

    if [ $i -lt $INSTANCES ]; then
        echo "Esperando 30s antes de la siguiente instancia..."
        sleep 30
    fi
done

echo ""
echo "Monitoreando procesos (Ctrl+C para salir del monitor, los procesos siguen corriendo)..."

while true; do
    RUNNING=0
    STATUS=""

    for PID in "${PIDS[@]}"; do
        if kill -0 $PID 2>/dev/null; then
            CPU=$(ps -p $PID -o %cpu= 2>/dev/null | tr -d ' ')
            MEM=$(ps -p $PID -o %mem= 2>/dev/null | tr -d ' ')
            STATUS+="  [PID=$PID] corriendo — CPU: ${CPU}% MEM: ${MEM}%\n"
            RUNNING=$((RUNNING + 1))
        else
            STATUS+="  [PID=$PID] finalizado\n"
        fi
    done

    clear
    echo "=== Instancias MODE='$MODE' === $(date '+%H:%M:%S')"
    echo -e "$STATUS"
    echo "Activas: $RUNNING / ${#PIDS[@]}"

    if [ $RUNNING -eq 0 ]; then
        echo ""
        echo "Todas las instancias finalizaron."
        break
    fi

    sleep 3
done
