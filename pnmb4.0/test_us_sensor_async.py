import uasyncio
from machine import Pin, PWM
from us_sensor_HC_SR04 import measure_distance_in_cm
from speaker import warn_by_time_between_beeps

trigger = Pin(13, Pin.OUT)
echo = Pin(17, Pin.IN)
speaker_out = PWM(Pin(22))


async def main():
    while True:
        distance_in_cm = await measure_distance_in_cm(trigger, echo)
        print(f"Distance is {distance_in_cm} cm")
        if distance_in_cm < 20:
            warn_by_time_between_beeps(
                speaker=speaker_out, severity_from_1_to_10=int(10 - distance_in_cm / 2)
            )
        await uasyncio.sleep(0.11)


try:
    uasyncio.run(main())
except KeyboardInterrupt:
    print("Terminate")
finally:
    print("Goodbye")
    uasyncio.new_event_loop()
