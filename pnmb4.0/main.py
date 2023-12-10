import re
import gc
import uasyncio
import network
from machine import Pin
from board import Board
from wlan_credentials import WIFI_SSID, WIFI_PASSWORD
from webpage import webpage_html

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


async def idle_loop():
    while True:
        await uasyncio.sleep(0.2)


async def main(background_task):
    async def start_server():
        server = await uasyncio.start_server(serve_client, "0.0.0.0", 80)

    async def server_and_background_task():
        await uasyncio.gather(start_server(), background_task())

    ip = await connect_to_wlan()
    print(f"connect to {ip}")
    await server_and_background_task()


async def serve_client(reader, writer):
    async def send_headers(
        status_code=200, content_type="text/html", content_length=None
    ):
        headers = f"HTTP/1.0 {status_code}\r\nContent-type: {content_type}\r\n"
        if content_length is not None:
            headers += f"Content-Length: {content_length}\r\n"
        headers += "\r\n"
        writer.write(headers)
        await writer.drain()

    gc.collect()
    try:
        headers = []
        while True:
            line = await reader.readline()
            # print("line: "+str(line))
            line = line.decode("utf-8").strip()
            if line == "":
                break
            headers.append(line)
        request_raw = str("\r\n".join(headers))
        # print(request_raw)

        request_pattern = re.compile(r"(GET|POST)\s+([^\s]+)\s+HTTP")
        match = request_pattern.search(request_raw)
        action_request = ""
        if match:
            method = match.group(1)
            url = match.group(2)
            # print(f"regex match: {method}, {url}")
            action_request = url
        else:  # regex didn't match, try splitting the request line
            request_parts = request_raw.split(" ")
            if len(request_parts) > 1:
                method = request_parts[0]
                url = request_parts[1]
                # print(f"non regex match: {method}, {url}")
                action_request = url
            else:
                # print("no match")
                pass

        if action_request == "/forward?":
            # forward()
            action_request = "forward"
        elif action_request == "/left?":
            # turn_left()
            action_request = "left"
        elif action_request == "/stop?":
            # stop()
            action_request = "stop"
        elif action_request == "/right?":
            # turn_right()
            action_request = "right"
        elif action_request == "/back?":
            # backward()
            action_request = "back"

        await send_headers()
        writer.write(webpage_html(action_request))
        await writer.drain()
        await writer.wait_closed()
    except OSError as e:
        print(e)


try:
    uasyncio.run(main(background_task=idle_loop))
except KeyboardInterrupt:
    print("Terminate")
finally:
    led.off()
    uasyncio.new_event_loop()
