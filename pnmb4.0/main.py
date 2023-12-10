import re
import gc
import uasyncio
from pi_board_utils import init_board, change_led_status, connect_to_wlan
from webpage import webpage_html

shutdown_pnmb4 = False
server = ""


async def handle_action_request(action_request: str) -> str:
    global server
    if "forward" in action_request:
        # forward()
        action_request = "forward"
    elif "left" in action_request:
        # turn_left()
        action_request = "left"
    elif "stop" in action_request:
        # stop()
        action_request = "stop"
    elif "right" in action_request:
        # turn_right()
        action_request = "right"
    elif "back" in action_request:
        # backward()
        action_request = "back"

    return action_request


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
            # method = match.group(1)
            url = match.group(2)
            # print(f"regex match: {method}, {url}")
            action_request = url
        else:  # regex didn't match, try splitting the request line
            request_parts = request_raw.split(" ")
            if len(request_parts) > 1:
                # method = request_parts[0]
                url = request_parts[1]
                # print(f"non regex match: {method}, {url}")
                action_request = url
            else:
                # print("no match")
                pass

        if "shutdown" in action_request:
            print("Shutting down")
            await stop_server()
            return
        verified_action_request = await handle_action_request(action_request)

        await send_headers()
        writer.write(webpage_html(verified_action_request))
        await writer.drain()
        await writer.wait_closed()
    except OSError as e:
        print(e)


async def idle_loop():
    global shutdown_pnmb4
    while not shutdown_pnmb4:
        await uasyncio.sleep(0.2)


async def start_server():
    global server
    server = await uasyncio.start_server(serve_client, "0.0.0.0", 80)


async def stop_server():
    global server
    server.close()
    await server.wait_closed()
    shutdown_pnmb4 = True
    server = None


async def main(background_task):
    async def server_and_background_task():
        await uasyncio.gather(start_server(), background_task())

    ip = await connect_to_wlan()
    print(f"connect to {ip}")
    await server_and_background_task()


try:
    init_board()
    uasyncio.run(main(background_task=idle_loop))
except KeyboardInterrupt:
    print("Terminate")
finally:
    change_led_status(led_on=False)
    uasyncio.new_event_loop()
