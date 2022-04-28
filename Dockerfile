FROM python:3.10-slim as builder
ARG BUILD_DATE
ARG VCS_REF

ENV PWM_OUT_PIN=18 \
    PWM_FREQUENCY=25 \
    PWM_REFRESH_TIME=1 \
    FAN_TEMP_TARGET=40.0 \
    FAN_TEMP_OFF=35.0 \
    FAN_OFF_PERCENTAGE=0.0 \
    FAN_MIN_PERCENTAGE=1.0 \
    FAN_MAX_PERCENTAGE=100.0 \
    FAN_START_PERCENTAGE=50 \
    FAN_TACH_IN_PIN=24 \
    FAN_TACH_PULSE_PER_REV=2 \
    FAN_TACH_REFRESH_TIME=1 \
    PID_P_VALUE=5.0 \
    PID_I_VALUE=3.0 \
    PID_D_VALUE=3.0 \
    GID_GPIO=997

#ARG PYTHON3_VERSION="3.9.7-r4"
#ARG PYTHON3_DEV_VERSION="3.9.7-r4"
#ARG PYTHON3_PIP_VERSION="20.3.4-r1"
#ARG MUSL_DEV_VERSION="1.2.2-r7"
#ARG GCC_VERSION="10.3.1_git20211027-r0"
#ARG WIRINGPI_VERSION="2.50-r0"
ARG RPI_GPIO_VERSION="0.7.1"

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential && \
    apt-get clean && \
    python3 -m pip install --no-cache-dir rpi.gpio==$RPI_GPIO_VERSION

RUN groupadd -g $GID_GPIO gpio && \
    usermod -aG gpio root

COPY scripts/* /root/
RUN chmod +x /root/docker-entrypoint.sh
WORKDIR /root

CMD ["python", "-u", "/root/fan_control.py"]
