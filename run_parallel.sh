#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Uso: $0 <modo> <instancias>"
    echo "Ejemplo: $0 modified 3"
    exit 1
fi

MODE=$1
INSTANCES=$2
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PIDS_FILE="$SCRIPT_DIR/.pids"

# Limpiar pids anteriores
rm -f "$PIDS_FILE"
touch "$PIDS_FILE"

cleanup() {
    echo ""
    echo "Interrumpido — matando procesos activos..."
    pkill -f RUN_TFG.py
    rm -f "$PIDS_FILE"
    kill $MONITOR_PID 2>/dev/null
    exit 1
}

trap cleanup SIGINT SIGTERM

monitor() {
    sleep 2
    while true; do
        RUNNING=0
        STATUS=""
        LAUNCHED=0

        while IFS= read -r PID; do
            LAUNCHED=$((LAUNCHED + 1))
            if kill -0 $PID 2>/dev/null; then
                CPU=$(ps -p $PID -o %cpu= 2>/dev/null | tr -d ' ')
                MEM=$(ps -p $PID -o %mem= 2>/dev/null | tr -d ' ')
                STATUS+="  [PID=$PID] corriendo — CPU: ${CPU}% MEM: ${MEM}%\n"
                RUNNING=$((RUNNING + 1))
            else
                STATUS+="  [PID=$PID] finalizado\n"
            fi
        done < "$PIDS_FILE"

        clear
        echo "=== Instancias MODE='$MODE' === $(date '+%H:%M:%S') | Ctrl+C para terminar todo"
        echo "Lanzadas: $LAUNCHED / $INSTANCES — Activas: $RUNNING"
        echo ""
        echo -e "$STATUS"

        if [ $RUNNING -eq 0 ] && [ $LAUNCHED -eq $INSTANCES ]; then
            echo "Todas las instancias finalizaron."
            rm -f "$PIDS_FILE"
            break
        fi

        sleep 3
    done
}

echo "Lanzando $INSTANCES instancias con MODE='$MODE'..."

monitor &
MONITOR_PID=$!

for i in $(seq 1 $INSTANCES); do
    ./run_tfg.sh $MODE &

    if [ $i -lt $INSTANCES ]; then
        echo "Instancia $i lanzada — esperando 30s..."
        sleep 30
    else
        echo "Instancia $i lanzada"
    fi
done

wait $MONITOR_PID