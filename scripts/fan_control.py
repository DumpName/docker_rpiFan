#! /usr/bin/env python3
import os
import time
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO

PWM_OUT_PIN = int( os.getenv( 'PWM_OUT_PIN', 18 ) )          # pin used to drive PWM fan
PWM_FREQUENCY = int( os.getenv( 'PWM_FREQUENCY', 25 ) )      # [kHz] PWM frequency
PWM_REFRESH_TIME = int( os.getenv( 'PWM_REFRESH_TIME', 1 ) ) # [s] Time to wait between each refresh

FAN_TEMP_TARGET = float( os.getenv( 'TEMP_TARGET', 40.0 ) )
FAN_TEMP_OFF = float( os.getenv( 'TEMP_OFF', 35.0 ) )
FAN_OFF_PERCENTAGE = float( os.getenv( 'FAN_OFF_PERCENTAGE', 0.0 ) )
FAN_MIN_PERCENTAGE = float( os.getenv( 'FAN_MIN_PERCENTAGE', 1.0 ) )
FAN_MAX_PERCENTAGE = float( os.getenv( 'FAN_MAX_PERCENTAGE', 100.0 ) )
FAN_START_PERCENTAGE = float( os.getenv( 'FAN_START_PERCENTAGE', 50.0 ) )

PID_P_VALUE = float( os.getenv( 'PID_P_VALUE', 5.0 ) )
PID_I_VALUE = float( os.getenv( 'PID_I_VALUE', 5.0 ) )
PID_D_VALUE = float( os.getenv( 'PID_D_VALUE', 5.0 ) )

fanSpeed = FAN_START_PERCENTAGE
tempSum = 0

def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read()) / 1000

tempOld = getCpuTemperature()

def fanOFF():
    pwmPin.ChangeDutyCycle(0)
    return()

def handleFanSpeed( ):
    global fanSpeed, tempSum, tempOld
    tempAct = getCpuTemperature( )

    tempDiff = tempAct - FAN_TEMP_TARGET
    tempSum = tempSum + tempDiff
    pDiff = PID_P_VALUE * tempDiff
    iDiff = PID_I_VALUE * PWM_REFRESH_TIME * tempSum
    dDiff = PID_D_VALUE * ( tempDiff - tempOld ) / PWM_REFRESH_TIME
    fanSpeed = pDiff + iDiff + dDiff
    tempOld = tempAct

    if fanSpeed > FAN_MAX_PERCENTAGE:
        fanSpeed = FAN_MAX_PERCENTAGE
    if fanSpeed < FAN_MIN_PERCENTAGE:
        fanSpeed = FAN_OFF_PERCENTAGE
    if tempSum > 100:
        tempSum = 100
    if tempSum < -100:
        tempSum = -100
    print("actualTemp %4.2f TempDiff %4.2f pDiff %4.2f iDiff %4.2f dDiff %4.2f fanSpeed %5d" % (
         tempAct, tempDiff, pDiff, iDiff, dDiff, fanSpeed))
    pwmPin.ChangeDutyCycle(fanSpeed)
    return()

try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM_OUT_PIN, GPIO.OUT)
    pwmPin = GPIO.PWM(PWM_OUT_PIN, PWM_FREQUENCY)
    pwmPin.start(FAN_START_PERCENTAGE)
    GPIO.setwarnings(False)
    fanOFF()
    while True:
        handleFanSpeed()
        sleep(PWM_REFRESH_TIME)
except KeyboardInterrupt:
    fanOFF()
finally:
    GPIO.cleanup()
