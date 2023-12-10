import uasyncio
import network
from machine import Pin
from board import Board
from wlan_credentials import WIFI_SSID, WIFI_PASSWORD

led = Pin("LED", Pin.OUT)


def init_board():
    global led
    BOARD_TYPE = Board().type
    print("Board type: " + BOARD_TYPE)

    if BOARD_TYPE == Board.BoardType.PICO_W:
        led = Pin("LED", Pin.OUT)
    elif BOARD_TYPE == Board.BoardType.PICO:
        led = Pin(25, Pin.OUT)
    elif BOARD_TYPE == Board.BoardType.ESP8266:
        led = Pin(2, Pin.OUT)
    else:
        led = Pin(2, Pin.OUT)


def change_led_status(led_on: bool) -> None:
    if led_on:
        led.on()
    else:
        led.off()


async def loading(delay: float = 0.5) -> None:
    led_on_status = False
    while True:
        led_on_status = not led_on_status
        change_led_status(led_on=led_on_status)
        await uasyncio.sleep(delay)


async def create_wlan_connection() -> str:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    while not wlan.isconnected():  # and wlan.status() != 3:
        print(f"Trying to connect to {WIFI_SSID}")
        await uasyncio.sleep(1)

    if not wlan.isconnected():
        raise RuntimeError("network connection failed")
    change_led_status(led_on=True)
    ip = wlan.ifconfig()[0]
    return ip


async def connect_to_wlan() -> str:
    loading_task = uasyncio.create_task(loading())
    ip = await create_wlan_connection()
    loading_task.cancel()
    return ip
