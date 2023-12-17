# PNMB4.0

This first version is control code for two servos and a pico (w). Pico broadcasts a website with buttons (at least the commands "forward", "backward", "turn left", "turn right", and "stop") to control the servos remotely within the same wlan.

All the following refers to an implementation with a PicoW.

# micropython on linux and vscode

1. make sure you are part of the `dialout` group (`sudo usermod -a -G dialout <user>`)
2. install extension `MicroPico`
3. good to go.

# Technical setup

The following sensors are used and assumed to be on the pins. Further information on the code can be found in the next section.

| Sensor                  | Pins/PWM / connections                                      |
| ----------------------- | ----------------------------------------------------------- |
| Servos (2)              | `PWM(Pin(8))` for left motor, `PWM(Pin(9))` for right motor |
| Ultrasonic sensor       | `Pin(13, Pin.OUT)` for trigger, `Pin(17, Pin.IN)` for echo  |
| Analog speaker (no amp) | `PWM(Pin(22))` on plus                                      |

# Abstractions

## Motors

I used the great [micropython_servo_pdm_360](https://github.com/TTitanUA/micropython_servo_pdm_360) library by [TTitanUA](https://github.com/TTitanUA) to abstract the servos.

I further have an abstraction layer in [motor.py](motor.py). This allows for high-level functions such as `start_motor`, `stop_motor`, `forward` etc.

[test_motor.py](test_motor.py) demonstrates its use. [test_motor_async.py](test_motor_async.py) does it using async code.

## Ultrasonic sensor

I used the reference code from the great site [Elektronik Kompendium](https://www.elektronik-kompendium.de/sites/raspberry-pi/2701131.htm) to control the US sensor. In [us_sensor_HC_NR04.py](us_sensor_HC_SR04.py) I provide the high-level function `measure_distance_in_cm`.

## Loudspeaker (no amp)

[speaker.py](speaker.py) contains a lot of methods I took from an [article from tomshardware.com](https://www.tomshardware.com/how-to/buzzer-music-raspberry-pi-pico).

## main

[main.py](main.py) contains all high-level control. I looked up some async and web patterns from the [gurgleapps pico-web-server-control](https://github.com/gurgleapps/pico-web-server-control). They talk about it [here](https://gurgleapps.com/learn/projects/micropython-web-server-control-raspberry-pi-pico-projects). I found their loop control very helpful. Additional sensor functionality each running in its own async control loop can be added to the list in the `main` method - this application now scales nicely.

```python
async def main(background_task):
    (...)
    await uasyncio.gather(
        start_server(),
        measure_distance_for_us_sensor_loop(),
        control_audio_proximity_warning(),
        background_task(),
    )
```

# Licensing

[board.py](board.py) is taken from the [gurgleapps pico-web-server-control](https://github.com/gurgleapps/pico-web-server-control) project which is licensed under MIT.
