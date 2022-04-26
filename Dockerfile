FROM alpine:3.15
ARG BUILD_DATE
ARG VCS_REF

ENV PWM_OUT_PIN=18 \
    PWM_FREQUENCY=25 \
    PWM_REFRESH_TIME=1 \
    FAN_TACH_IN_PIN=24 \
    FAN_TACH_PULSE_PER_REV=2 \
    FAN_TACH_REFRESH_TIME=1 \
    FAN_OFF_TEMP=40 \
    FAN_MIN_TEMP=45 \
    FAN_MAX_TEMP=70

ARG PYTHON3_VERSION="3.9.7-r4"
ARG PYTHON3_DEV_VERSION="3.9.7-r4"
ARG PYTHON3_PIP_VERSION="20.3.4-r1"
ARG MUSL_DEV_VERSION="1.2.2-r7"
ARG GCC_VERSION="10.3.1_git20211027-r0"
ARG WIRINGPI_VERSION="2.50-r0"
ARG RPI_GPIO_VERSION="0.7.1"

RUN apk add --no-cache \
        bash \
        python3=$PYTHON3_VERSION \
        python3-dev=$PYTHON3_DEV_VERSION \
        py3-pip=$PYTHON3_PIP_VERSION \
        musl-dev=$MUSL_DEV_VERSION \
        gcc=$GCC_VERSION \
        wiringpi=$WIRINGPI_VERSION && \
    python3 -m pip install --no-cache-dir \
        rpi.gpio==$RPI_GPIO_VERSION

COPY scripts/* /root/
RUN chmod +x /root/docker-entrypoint.sh
WORKDIR /root

ENTRYPOINT ["/root/docker-entrypoint.sh"]


