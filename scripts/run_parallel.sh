#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Uso: $0 <instancias>"
    echo "Ejemplo: $0 3"
    exit 1
fi

INSTANCES=$1
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PIDS=()
MONITOR_PID=""

cleanup() {
    echo ""
    echo "Interrumpido — matando procesos activos..."
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null
    done
    pkill -f run_tfg.py
    [ -n "$MONITOR_PID" ] && kill "$MONITOR_PID" 2>/dev/null
    exit 1
}

trap cleanup SIGINT SIGTERM

is_running() {
    kill -0 "$1" 2>/dev/null
}

monitor() {
    sleep 2
    while true; do
        RUNNING=0
        STATUS=""

        for pid in "${PIDS[@]}"; do
            if is_running "$pid"; then
                ELAPSED=$(ps -o etime= -p "$pid" 2>/dev/null | tr -d ' ')
                CPU=$(ps -o %cpu= -p "$pid" 2>/dev/null | tr -d ' ')
                MEM=$(ps -o %mem= -p "$pid" 2>/dev/null | tr -d ' ')
                STATUS+="  [PID=$pid] corriendo — CPU: ${CPU}% MEM: ${MEM}% ELAPSED: ${ELAPSED}\n"
                RUNNING=$((RUNNING + 1))
            else
                STATUS+="  [PID=$pid] finalizado\n"
            fi
        done

        clear
        echo "=== Instancias === $(date '+%H:%M:%S') | Ctrl+C para terminar todo"
        echo "Activas: $RUNNING / $INSTANCES"
        echo ""
        echo -e "$STATUS"

        if [ "$RUNNING" -eq 0 ]; then
            echo "Todas las instancias finalizaron."
            break
        fi

        sleep 3
    done
}

echo "Lanzando $INSTANCES instancias..."

for i in $(seq 1 "$INSTANCES"); do
    "$SCRIPT_DIR/run_tfg.sh" &
    PIDS+=($!)
    echo "  Instancia $i lanzada [PID=${PIDS[-1]}]"

    if [ "$i" -lt "$INSTANCES" ]; then
        sleep 10
    fi
done

echo "Todas las instancias lanzadas. Iniciando monitor..."

monitor &
MONITOR_PID=$!

wait "$MONITOR_PID"
