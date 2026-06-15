#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Uso: $0 <modo> <instancias>"
    echo "Ejemplo: $0 modified 3"
    exit 1
fi

MODE=$1
INSTANCES=$2
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PIDS=()

cleanup() {
    echo ""
    echo "Interrumpido — matando procesos activos..."
    kill "${PIDS[@]}" 2>/dev/null
    pkill -f run_tfg.py
    kill $MONITOR_PID 2>/dev/null
    exit 1
}

trap cleanup SIGINT SIGTERM

monitor() {
    sleep 2
    while true; do
        RUNNING=0
        STATUS=""

        while IFS= read -r line; do
            PID=$(echo "$line" | awk '{print $1}')
            CPU=$(echo "$line" | awk '{print $2}')
            MEM=$(echo "$line" | awk '{print $3}')
            ELAPSED=$(echo "$line" | awk '{print $4}')
            STATUS+="  [PID=$PID] corriendo — CPU: ${CPU}% MEM: ${MEM}% ELAPSED: ${ELAPSED}\n"
            RUNNING=$((RUNNING + 1))
        done < <(ps -eo pid,%cpu,%mem,etime,args | grep "run_tfg.py $MODE" | grep -v grep)

        clear
        echo "=== Instancias MODE='$MODE' === $(date '+%H:%M:%S') | Ctrl+C para terminar todo"
        echo "Activas: $RUNNING / $INSTANCES"
        echo ""
        echo -e "$STATUS"

        if [ $RUNNING -eq 0 ]; then
            echo "Todas las instancias finalizaron."
            break
        fi

        sleep 3
    done
}

echo "Lanzando $INSTANCES instancias con MODE='$MODE'..."

monitor &
MONITOR_PID=$!

for i in $(seq 1 $INSTANCES); do
    "$SCRIPT_DIR/run_tfg.sh" $MODE &

    if [ $i -lt $INSTANCES ]; then
        sleep 30
    fi
done

wait $MONITOR_PID