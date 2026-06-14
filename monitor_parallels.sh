#!/bin/bash

watch -n 3 "echo 'PID      %CPU %MEM     ELAPSED COMMAND'; pgrep -f RUN_TFG.py --runstates S,R | xargs ps --no-headers -o pid,pcpu,pmem,etime,args -p 2>/dev/null | grep python || echo 'Sin procesos activos'"
