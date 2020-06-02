"""
Run mqtt broker on localhost: sudo apt-get install mosquitto mosquitto-clients
"""
#!/usr/bin/env python3

import argparse
import requests
import ST7735
import time
from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError
from subprocess import PIPE, Popen, check_output
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import json

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# mqtt callbacks
def on_connect(client, userdata, flags, rc):
    print(f"CONNACK received with code {rc}")
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))


# Read values from BME280 and PMS5003 and return as dict
def read_values(bme280, pms5003):
    # Compensation factor for temperature
    comp_factor = 2.25

    values = {}
    cpu_temp = get_cpu_temperature()
    raw_temp = bme280.get_temperature()
    comp_temp = raw_temp - ((cpu_temp - raw_temp) / comp_factor)
    values["temperature"] = float("{:.2f}".format(comp_temp))
    values["pressure"] = float("{:.2f}".format(bme280.get_pressure() * 100))
    values["humidity"] = float("{:.2f}".format(bme280.get_humidity()))
    try:
        pm_values = pms5003.read()
        values["P2"] = pm_values.pm_ug_per_m3(2.5)
        values["P1"] = pm_values.pm_ug_per_m3(10)
    except ReadTimeoutError:
        pms5003.reset()
        pm_values = pms5003.read()
        values["P2"] = pm_values.pm_ug_per_m3(2.5)
        values["P1"] = pm_values.pm_ug_per_m3(10)
    return values


# Get CPU temperature to use for compensation
def get_cpu_temperature():
    process = Popen(["vcgencmd", "measure_temp"], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index("=") + 1 : output.rindex("'")])


# Get Raspberry Pi serial number to use as ID
def get_serial_number():
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if line[0:6] == "Serial":
                return line.split(":")[1].strip()


# Check for Wi-Fi connection
def check_wifi():
    if check_output(["hostname", "-I"]):
        return True
    else:
        return False


# Display Raspberry Pi serial and Wi-Fi status on LCD
def display_status(disp):
    # Width and height to calculate text position
    WIDTH = disp.width
    HEIGHT = disp.height

    wifi_status = "connected" if check_wifi() else "disconnected"
    text_colour = (255, 255, 255)
    back_colour = (0, 170, 170) if check_wifi() else (85, 15, 15)
    id = get_serial_number()
    message = "{}\nWi-Fi: {}".format(id, wifi_status)
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    size_x, size_y = draw.textsize(message, font)
    x = (WIDTH - size_x) / 2
    y = (HEIGHT / 2) - (size_y / 2)
    draw.rectangle((0, 0, 160, 80), back_colour)
    draw.text((x, y), message, font=font, fill=text_colour)
    disp.display(img)


def main():
    """Main."""

    print(
        """mqtt-all.py - Reads temperature, pressure, humidity,
    PM2.5, and PM10 from Enviro plus and sends data over mqtt.

    Press Ctrl+C to exit!

    """
    )

    mqtt_broker = "localhost"
    mqtt_port = 1883
    mqtt_topic = "enviroplus"

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.connect(mqtt_broker, port=mqtt_port)

    bus = SMBus(1)

    # Create BME280 instance
    bme280 = BME280(i2c_dev=bus)

    # Create LCD instance
    disp = ST7735.ST7735(
        port=0, cs=1, dc=9, backlight=12, rotation=270, spi_speed_hz=10000000
    )

    # Initialize display
    disp.begin()

    # Create PMS5003 instance
    pms5003 = PMS5003()

    # Raspberry Pi ID
    device_serial_number = get_serial_number()
    id = "raspi-" + device_serial_number

    # Text settings
    font_size = 16
    font = ImageFont.truetype(UserFont, font_size)

    # Display Raspberry Pi serial and Wi-Fi status
    print("Raspberry Pi serial: {}".format(get_serial_number()))
    print("Wi-Fi: {}\n".format("connected" if check_wifi() else "disconnected"))
    print("MQTT broker IP: {}".format(mqtt_broker))

    time_since_update = 0
    update_time = time.time()

    # Main loop to read data, display, and send over mqtt
    mqtt_client.loop_start()
    while True:
        try:
            time_since_update = time.time() - update_time
            values = read_values(bme280, pms5003)
            print(values)
            mqtt_client.publish(mqtt_topic, json.dumps(values))
            if time_since_update > 145:
                update_time = time.time()
            display_status(disp)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
