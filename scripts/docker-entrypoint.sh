#!/bin/bash
CONTROLLER_PID=0
TACHO_PID=0
if [ ! -f startup_done ]; then
  #python3 /root/read_fan_speed.py &
  #TACHO_PID=$!
  python3 /root/fan_control.py &
  CONTROLLER_PID=$!

  touch startup_done
fi

python3 /root/read_fan_speed.py
