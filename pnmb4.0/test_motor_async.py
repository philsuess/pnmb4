from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360RP2Async, SmoothLinear
import uasyncio as asyncio

servo_pwm_left = PWM(Pin(8))
servo_pwm_right = PWM(Pin(9))

freq = 50
min_us = 700
max_us = 2300
dead_zone_us = 90

# create a servo object
servo_left = ServoPDM360RP2Async(
    pwm=servo_pwm_left,
    min_us=min_us,
    max_us=max_us,
    dead_zone_us=dead_zone_us,
    freq=freq,
)
servo_right = ServoPDM360RP2Async(
    pwm=servo_pwm_right,
    min_us=min_us,
    max_us=max_us,
    dead_zone_us=dead_zone_us,
    freq=freq,
)


async def main():
    print("Gegen die Uhr")
    servo_left.turn_ccv_ms()
    servo_right.turn_ccv_ms()

    # wait 3 seconds
    await asyncio.sleep(3)

    print("Mit der Uhr")
    servo_left.turn_cv_ms()
    servo_right.turn_cv_ms()

    # wait 3 seconds
    await asyncio.sleep(3)

    print("turn clockwise with a force of 30 for 2 seconds")
    servo_left.turn_cv_ms(time_ms=2000, force=30)
    servo_right.turn_cv_ms(time_ms=2000, force=30)

    # wait 3 seconds
    await asyncio.sleep(3)

    print(
        "turn clockwise with a force of 50 with a smoothing at the beginning 2 seconds"
    )
    servo_left.turn_cv_ms(force=50, start_smoothing=SmoothLinear(50, 2000))
    servo_right.turn_cv_ms(force=50, start_smoothing=SmoothLinear(50, 2000))

    # wait 5 seconds
    await asyncio.sleep(5)

    print("smoothly stop the servo")
    servo_left.stop_smooth(end_smoothing=SmoothLinear(50, 500))
    servo_right.stop_smooth(end_smoothing=SmoothLinear(50, 500))

    # wait 3 seconds
    await asyncio.sleep(3)

    print(
        "turn counter-clockwise with a force of 100 for 2 seconds with a smoothing at the start and at the end"
    )
    servo_left.turn_ccv_ms(
        2000,
        100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )
    servo_right.turn_ccv_ms(
        2000,
        100,
        start_smoothing=SmoothLinear(50, 1000),
        end_smoothing=SmoothLinear(50, 500),
    )

    # wait 5 seconds
    await asyncio.sleep(5)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    servo_left.deinit()
    servo_right.deinit()
