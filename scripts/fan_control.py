#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
import signal
import sys

PWM_OUT_PIN = int( sys.argv[1] )       # pin used to drive PWM fan
PWM_FREQUENCY = int( sys.argv[2] )     # [kHz] PWM frequency
PWM_REFRESH_TIME = int( sys.argv[3] )  # [s] Time to wait between each refresh

FAN_OFF_TEMP = int( sys.argv[4] )    # [°C] temperature below which to stop the fan
FAN_MIN_TEMP = int( sys.argv[5] )      # [°C] temperature above which to start the fan
FAN_MAX_TEMP = 70               # [°C] temperature at which to operate at max fan speed
FAN_LOW = 1
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100
FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(FAN_MAX_TEMP - FAN_MIN_TEMP)


def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read()) / 1000


def handleFanSpeed(fan, temperature):
    if temperature > FAN_MIN_TEMP:
        delta = min(temperature, FAN_MAX_TEMP) - FAN_MIN_TEMP
        fan.start(FAN_LOW + delta * FAN_GAIN)

    elif temperature < FAN_OFF_TEMP:
        fan.start(FAN_OFF)


try:
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM_OUT_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(PWM_OUT_PIN, PWM_FREQUENCY)
    while True:
        handleFanSpeed(fan, getCpuTemperature())
        time.sleep(PWM_REFRESH_TIME)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
