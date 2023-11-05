import network
import socket
import machine
from utime import sleep

ssid = "NataliesHeaven"
password = "09091982"
led_onboard = machine.Pin("LED", machine.Pin.OUT)


def forward():
    print("forward")


def backward():
    print("backward")


def turn_left():
    print("turn_left")


def turn_right():
    print("turn_right")


def stop():
    print("stop")


def connect():
    def change_led_status(led_on: bool):
        if led_on:
            led_onboard.on()
        else:
            led_onboard.off()

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    led_on_status = False
    while not wlan.isconnected():
        led_on_status = not led_on_status
        change_led_status(led_on=led_on_status)
        print(f"Establishing connection to {ssid}")
        sleep(1)
    ip = wlan.ifconfig()[0]
    change_led_status(led_on=True)
    print(f"connected to {ip}")
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


def webpage():
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>PNMB4 Control</title>
            </head>
            <center><b>
            <form action="./forward">
            <input type="submit" value="Vorw&auml;rts" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Links" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./stop">
            <input type="submit" value="Stop" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Rechts" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="R&uuml;ckw&auml;rts" style="height:120px; width:120px" />
            </form>
            </body>
            </html>
            """
    return str(html)


def serve(connection):
    # Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == "/forward?":
            forward()
        elif request == "/left?":
            turn_left()
        elif request == "/stop?":
            stop()
        elif request == "/right?":
            turn_right()
        elif request == "/back?":
            backward()
        html = webpage()
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    led_onboard.off()
    machine.reset()

led_onboard.off()
