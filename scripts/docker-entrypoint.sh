#!/bin/bash
CONTROLLER_PID=0
TACHO_PID=0
if [ ! -f startup_done ]; then
  #python3 /root/read_fan_speed.py &
  #TACHO_PID=$!
  python3 /root/fan_control.py ${PWM_OUT_PIN} ${PWM_FREQUENCY} ${PWM_REFRESH_TIME} ${FAN_OFF_TEMP} ${FAN_MIN_TEMP} ${FAN_MAX_TEMP} 0 &
  CONTROLLER_PID=$!

  touch startup_done
fi

python3 /root/read_fan_speed.py ${FAN_TACH_IN_PIN} ${FAN_TACH_PULSE_PER_REV} ${FAN_TACH_REFRESH_TIME} 0
