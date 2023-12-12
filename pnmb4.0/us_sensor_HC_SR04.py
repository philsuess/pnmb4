import uasyncio
from time import ticks_us, ticks_diff
from machine import Pin


async def measure_distance_in_cm(trigger: Pin, echo: Pin) -> float:
    time_passed_in_ticks = await _measure_ticks_differences(trigger, echo)
    return convert_to_distance_in_cm(time_passed_in_ticks)


def convert_to_distance_in_cm(time_passed_in_ticks: int) -> float:
    # see https://www.elektronik-kompendium.de/sites/raspberry-pi/2701131.htm
    return time_passed_in_ticks * 0.03432 / 2


async def _measure_ticks_differences(trigger: Pin, echo: Pin) -> int:
    # see https://www.elektronik-kompendium.de/sites/raspberry-pi/2701131.htm
    trigger.low()
    uasyncio.sleep(0.000002)
    trigger.high()
    uasyncio.sleep(0.000005)
    trigger.low()
    # Zeitmessungen
    while echo.value() == 0:
        signaloff = ticks_us()
    while echo.value() == 1:
        signalon = ticks_us()
    # Vergangene Zeit ermitteln
    return ticks_diff(signalon, signaloff)
