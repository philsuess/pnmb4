from machine import PWM
from micropython_servo_pdm_360 import ServoPDM360RP2Async, SmoothLinear


LEFT = 0
RIGHT = 1


def turn_off_motor(servos: tuple[ServoPDM360RP2Async, ServoPDM360RP2Async]) -> None:
    servos[LEFT].deinit()
    servos[RIGHT].deinit()


def start_motor(
    pwm_left_servo: PWM, pwm_right_servo: PWM
) -> tuple[ServoPDM360RP2Async, ServoPDM360RP2Async]:
    freq = 50
    min_us = 700
    max_us = 2300
    dead_zone_us = 90

    servo_left = ServoPDM360RP2Async(
        pwm=pwm_left_servo,
        min_us=min_us,
        max_us=max_us,
        dead_zone_us=dead_zone_us,
        freq=freq,
    )
    servo_right = ServoPDM360RP2Async(
        pwm=pwm_right_servo,
        min_us=min_us,
        max_us=max_us,
        dead_zone_us=dead_zone_us,
        freq=freq,
    )
    return servo_left, servo_right


def stop(servos: tuple[ServoPDM360RP2Async, ServoPDM360RP2Async]) -> None:
    servos[LEFT].stop_smooth(end_smoothing=SmoothLinear(50, 500))
    servos[RIGHT].stop_smooth(end_smoothing=SmoothLinear(50, 500))


def forward(servos: tuple[ServoPDM360RP2Async, ServoPDM360RP2Async]) -> None:
    servos[LEFT].turn_ccv_ms(
        time_ms=0,
        force=100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )
    servos[RIGHT].turn_cv_ms(
        time_ms=0,
        force=100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )


def backward(servos: tuple[ServoPDM360RP2Async, ServoPDM360RP2Async]) -> None:
    servos[LEFT].turn_cv_ms(
        time_ms=0,
        force=100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )
    servos[RIGHT].turn_ccv_ms(
        time_ms=0,
        force=100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )


def turn_left(servos: tuple[ServoPDM360RP2Async, ServoPDM360RP2Async]) -> None:
    servos[LEFT].turn_cv_ms(
        time_ms=0,
        force=100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )
    servos[RIGHT].turn_cv_ms(
        time_ms=0,
        force=100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )


def turn_right(servos: tuple[ServoPDM360RP2Async, ServoPDM360RP2Async]) -> None:
    servos[LEFT].turn_ccv_ms(
        time_ms=0,
        force=100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )
    servos[RIGHT].turn_ccv_ms(
        time_ms=0,
        force=100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )
