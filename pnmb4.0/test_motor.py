import motor
from machine import Pin, PWM
import uasyncio as asyncio


servo_pwm_left = PWM(Pin(8))
servo_pwm_right = PWM(Pin(9))
pnmb4_wheels = motor.start_motor(
    pwm_left_servo=servo_pwm_left, pwm_right_servo=servo_pwm_right
)


def forward():
    print("forward")
    motor.forward(pnmb4_wheels)


def backward():
    print("backward")
    motor.backward(pnmb4_wheels)


def turn_left():
    print("turn_left")
    motor.turn_left(pnmb4_wheels)


def turn_right():
    print("turn_right")
    motor.turn_right(pnmb4_wheels)


def stop():
    print("stop")
    motor.stop(pnmb4_wheels)


async def main():
    print("Vorwärts!")
    forward()
    await asyncio.sleep(3)

    print("Rückwärts!")
    backward()
    await asyncio.sleep(3)

    print("Links um!")
    motor.turn_left(pnmb4_wheels)
    await asyncio.sleep(3)

    print("Rechts um!")
    motor.turn_right(pnmb4_wheels)
    await asyncio.sleep(3)

    print("Stop!")
    motor.stop(pnmb4_wheels)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    motor.turn_off_motor(pnmb4_wheels)
    print("Schönen Tag noch.")
