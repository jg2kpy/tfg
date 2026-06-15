#!/bin/bash

while true; do
    clear
    echo "=== run_tfg Monitor === $(date '+%H:%M:%S') | Ctrl+C para salir"
    echo ""
    echo "PID      %CPU %MEM     ELAPSED COMMAND"
    pgrep -f run_tfg.py --runstates S,R | grep -v $$ | xargs ps --no-headers -o pid,pcpu,pmem,etime,args -p 2>/dev/null | grep python || echo "Sin procesos activos"
    sleep 3
done