import re
import gc
import uasyncio
from machine import Pin, PWM
from pi_board_utils import init_board, change_led_status, connect_to_wlan
from webpage import webpage_html
import motor
from us_sensor_HC_SR04 import measure_distance_in_cm

shutdown_pnmb4 = False
server = ""
servo_pwm_left = PWM(Pin(8))
servo_pwm_right = PWM(Pin(9))
pnmb4_wheels = motor.start_motor(
    pwm_left_servo=servo_pwm_left, pwm_right_servo=servo_pwm_right
)
us_sensor_trigger = Pin(13, Pin.OUT)
us_sensor_echo = Pin(17, Pin.IN)
last_measured_distance_to_sensor_in_cm: float = 0.0


async def handle_action_request(action_request: str) -> str:
    global server
    if "forward" in action_request:
        motor.forward(pnmb4_wheels)
        action_request = "forward"
    elif "left" in action_request:
        motor.turn_left(pnmb4_wheels)
        action_request = "left"
    elif "stop" in action_request:
        motor.stop(pnmb4_wheels)
        action_request = "stop"
    elif "right" in action_request:
        motor.turn_right(pnmb4_wheels)
        action_request = "right"
    elif "back" in action_request:
        motor.backward(servos=pnmb4_wheels)
        action_request = "back"
    elif "shutdown" in action_request:
        await stop_server()
        action_request = "shutdown"

    return action_request


async def send_response(writer, html_content):
    async def send_headers(
        status_code=200, content_type="text/html", content_length=None
    ):
        headers = f"HTTP/1.0 {status_code}\r\nContent-type: {content_type}\r\n"
        if content_length is not None:
            headers += f"Content-Length: {content_length}\r\n"
        headers += "\r\n"
        writer.write(headers)
        await writer.drain()

    await send_headers()
    writer.write(html_content)
    await writer.drain()
    await writer.wait_closed()


async def serve_client(reader, writer):
    async def get_raw_request():
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
        return request_raw

    def get_action_request(raw_request):
        request_pattern = re.compile(r"(GET|POST)\s+([^\s]+)\s+HTTP")
        match = request_pattern.search(raw_request)
        action_request = ""
        if match:
            # method = match.group(1)
            url = match.group(2)
            # print(f"regex match: {method}, {url}")
            action_request = url
        else:  # regex didn't match, try splitting the request line
            request_parts = raw_request.split(" ")
            if len(request_parts) > 1:
                # method = request_parts[0]
                url = request_parts[1]
                # print(f"non regex match: {method}, {url}")
                action_request = url
            else:
                # print("no match")
                pass
        return action_request

    gc.collect()
    try:
        request_raw = await get_raw_request()
        action_request = get_action_request(request_raw)
        verified_action_request = await handle_action_request(action_request)
        await send_response(writer, html_content=webpage_html(verified_action_request))
    except OSError as e:
        print(e)


async def idle_loop():
    global shutdown_pnmb4
    while not shutdown_pnmb4:
        await uasyncio.sleep(0.2)


async def measure_distance_for_us_sensor_loop(frequency_in_seconds: float = 1.0):
    global last_measured_distance_to_sensor_in_cm
    global shutdown_pnmb4
    while not shutdown_pnmb4:
        last_measured_distance_to_sensor_in_cm = await measure_distance_in_cm(
            us_sensor_trigger, us_sensor_echo
        )
        print(f"Distance to us sensor: {last_measured_distance_to_sensor_in_cm} cm")
        await uasyncio.sleep(frequency_in_seconds)


async def start_server():
    global server
    server = await uasyncio.start_server(serve_client, "0.0.0.0", 80)


async def stop_server():
    global server
    global shutdown_pnmb4
    server.close()
    await server.wait_closed()
    shutdown_pnmb4 = True
    server = None


async def main(background_task):
    ip = await connect_to_wlan()
    print(f"connect to {ip}")
    await uasyncio.gather(
        start_server(), measure_distance_for_us_sensor_loop(), background_task()
    )


try:
    init_board()
    uasyncio.run(main(background_task=idle_loop))
except KeyboardInterrupt:
    print("Terminate")
finally:
    change_led_status(led_on=False)
    motor.turn_off_motor(pnmb4_wheels)
    print("Goodbye")
    uasyncio.new_event_loop()
