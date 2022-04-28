# PID-Controller for a 4-pin PWM-Fan on a RaspberryPi

The Docker Image is based on [Pythons slim Image](https://hub.docker.com/_/python).

## Dependencies:
[![Generic badge](https://img.shields.io/badge/python-3.10--slim-brightgreen)](https://hub.docker.com/_/python)
[![Generic badge](https://img.shields.io/badge/rpi.gpio-0.7.1-brightgreen)](https://pypi.org/project/RPi.GPIO/)

## Configuration:
The container needs access to the device: `/dev/gpiomem` This can either be accomplished by adding it as a device, or by adding it as a Volume, if you are running this image in a swarm.

## Variables:

The following Docker Environment Variables can be set:


| Variable               | Default | Description                                                  |
|------------------------|---------|--------------------------------------------------------------|
| FAN_START_PERCENTAGE   | 50      | value at which the Fan should start                          |
| FAN_OFF_PERCENTAGE     | 0.0     | Percentage at which the fan is stopped                       |
| FAN_MIN_PERCENTAGE     | 1.0     | Percentage minimum controllable value.                       |
| FAN_MAX_PERCENTAGE     | 100.0   | Percentage up to which the fan should be controlled          |
| FAN_TACH_IN_PIN        | 24      | GPIO Pin that is connected to the fans TACH-output           |
| FAN_TACH_PULSE_PER_REV | 2       | How many TACH-pulses are provided per revolustion of the fan |
| FAN_TACH_REFRESH_TIME  | 1       | Time between fan-speed measurements                          |
| FAN_TEMP_OFF           | 35.0    | Temperature lower of which the fan should be turned off      |
| FAN_TEMP_TARGET        | 40.0    | Temperature that should be reached                           |
| PWM_FREQUENCY          | 25      | PWM-frequency in kHz                                         |
| PWM_OUT_PIN            | 18      | GPIO-Pin that the Fan is connected to                        |
| PWM_REFRESH_TIME       | 1.0     | Time between temp-measurements & fan-speed calculations      |
| PID_P_VALUE            | 5.0     | P constant for the PID-controller algorithm                  |
| PID_I_VALUE            | 5.0     | I constant for the PID-controller algorithm                  |
| PID_D_VALUE            | 5.0     | D constant for the PID-controller algorithm                  |

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
