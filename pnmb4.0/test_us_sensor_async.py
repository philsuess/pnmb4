import uasyncio
from machine import Pin
from us_sensor_HC_SR04 import measure_distance_in_cm

trigger = Pin(13, Pin.OUT)
echo = Pin(17, Pin.IN)


async def main():
    while True:
        distance_in_cm = await measure_distance_in_cm(trigger, echo)
        print(f"Distance is {distance_in_cm} cm")
        await uasyncio.sleep(1)


try:
    uasyncio.run(main())
except KeyboardInterrupt:
    print("Terminate")
finally:
    print("Goodbye")
    uasyncio.new_event_loop()
