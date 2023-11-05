import network
import socket
import motor
from machine import Pin, PWM, reset as pico_reset
import uasyncio as asyncio
from utime import sleep

ssid = "NataliesHeaven"
password = "09091982"
led_onboard = Pin("LED", Pin.OUT)

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


def main():
    ip = connect()
    connection = open_socket(ip)
    serve(connection)


try:
    # asyncio.run(main())
    main()
except KeyboardInterrupt:
    led_onboard.off()
    motor.turn_off_motor(pnmb4_wheels)
    pico_reset()
finally:
    motor.turn_off_motor(pnmb4_wheels)
    led_onboard.off()
    pico_reset()
