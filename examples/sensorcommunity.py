#!/usr/bin/env python3

import logging
import time
from subprocess import check_output

import requests
import st7735
from bme280 import BME280
from fonts.ttf import RobotoMedium as UserFont
from PIL import Image, ImageDraw, ImageFont
from pms5003 import PMS5003, ChecksumMismatchError, ReadTimeoutError
from smbus2 import SMBus

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")

logging.info("""sensorcommunity.py - Reads temperature, pressure, humidity,
PM2.5, and PM10 from Enviro plus and sends data to Sensor.Community,
the citizen science air quality project.

Note: you'll need to register with Sensor.Community at:
https://devices.sensor.community/ and enter your Raspberry Pi
serial number that's displayed on the Enviro plus LCD along
with the other details before the data appears on the
Sensor.Community map.

Press Ctrl+C to exit!

""")

bus = SMBus(1)

# Create BME280 instance
bme280 = BME280(i2c_dev=bus)

# Create LCD instance
disp = st7735.ST7735(
    port=0,
    cs=1,
    dc="GPIO9",
    backlight="GPIO12",
    rotation=270,
    spi_speed_hz=10000000
)

# Initialize display
disp.begin()

# Create PMS5003 instance
pms5003 = PMS5003()


# Read values from BME280 and PMS5003 and return as dict
def read_values():
    values = {}
    cpu_temp = get_cpu_temperature()
    raw_temp = bme280.get_temperature()
    comp_temp = raw_temp - ((cpu_temp - raw_temp) / comp_factor)
    values["temperature"] = f"{comp_temp:.2f}"
    values["pressure"] = f"{bme280.get_pressure() * 100:.2f}"
    values["humidity"] = f"{bme280.get_humidity():.2f}"
    try:
        pm_values = pms5003.read()
        values["P2"] = str(pm_values.pm_ug_per_m3(2.5))
        values["P1"] = str(pm_values.pm_ug_per_m3(10))
    except(ReadTimeoutError, ChecksumMismatchError):
        logging.info("Failed to read PMS5003. Resetting and retrying.")
        pms5003.reset()
        pm_values = pms5003.read()
        values["P2"] = str(pm_values.pm_ug_per_m3(2.5))
        values["P1"] = str(pm_values.pm_ug_per_m3(10))
    return values


# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp


# Get Raspberry Pi serial number to use as ID
def get_serial_number():
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if line.startswith("Serial"):
                return line.split(":")[1].strip()


# Check for Wi-Fi connection
def check_wifi():
    if check_output(["hostname", "-I"]):
        return True
    else:
        return False


# Display Raspberry Pi serial and Wi-Fi status on LCD
def display_status():
    wifi_status = "connected" if check_wifi() else "disconnected"
    text_colour = (255, 255, 255)
    back_colour = (0, 170, 170) if check_wifi() else (85, 15, 15)
    id = get_serial_number()
    message = f"{id}\nWi-Fi: {wifi_status}"
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    x1, y1, x2, y2 = font.getbbox(message)
    size_x = x2 - x1
    size_y = y2 - y1
    x = (WIDTH - size_x) / 2
    y = (HEIGHT / 2) - (size_y / 2)
    draw.rectangle((0, 0, 160, 80), back_colour)
    draw.text((x, y), message, font=font, fill=text_colour)
    disp.display(img)


def send_to_sensorcommunity(values, id):
    pm_values = dict(i for i in values.items() if i[0].startswith("P"))
    temp_values = dict(i for i in values.items() if not i[0].startswith("P"))

    pm_values_json = [{"value_type": key, "value": val} for key, val in pm_values.items()]
    temp_values_json = [{"value_type": key, "value": val} for key, val in temp_values.items()]

    resp_pm = None
    resp_bmp = None

    try:
        resp_pm = requests.post(
            "https://api.sensor.community/v1/push-sensor-data/",
            json={
                "software_version": "enviro-plus 1.0.0",
                "sensordatavalues": pm_values_json
            },
            headers={
                "X-PIN": "1",
                "X-Sensor": id,
                "Content-Type": "application/json",
                "cache-control": "no-cache"
            },
            timeout=5
        )
    except requests.exceptions.ConnectionError as e:
        logging.warning(f"Sensor.Community PM Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        logging.warning(f"Sensor.Community PM Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        logging.warning(f"Sensor.Community PM Request Error: {e}")

    try:
        resp_bmp = requests.post(
            "https://api.sensor.community/v1/push-sensor-data/",
            json={
                "software_version": "enviro-plus 1.0.0",
                "sensordatavalues": temp_values_json
            },
            headers={
                "X-PIN": "11",
                "X-Sensor": id,
                "Content-Type": "application/json",
                "cache-control": "no-cache"
            },
            timeout=5
        )
    except requests.exceptions.ConnectionError as e:
        logging.warning(f"Sensor.Community Climate Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        logging.warning(f"Sensor.Community Climate Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        logging.warning(f"Sensor.Community Climate Request Error: {e}")

    if resp_pm is not None and resp_bmp is not None:
        if resp_pm.ok and resp_bmp.ok:
            return True
        else:
            logging.warning(f"Sensor.Community Error. PM: {resp_pm.reason}, Climate: {resp_bmp.reason}")
            return False
    else:
        return False


# Compensation factor for temperature
comp_factor = 2.25

# Raspberry Pi ID to send to Sensor.Community
id = "raspi-" + get_serial_number()

# Width and height to calculate text position
WIDTH = disp.width
HEIGHT = disp.height

# Text settings
font_size = 16
font = ImageFont.truetype(UserFont, font_size)

# Log Raspberry Pi serial and Wi-Fi status
logging.info(f"Raspberry Pi serial: {get_serial_number()}")
wifi_status = "connected" if check_wifi() else "disconnected"
logging.info(f"Wi-Fi: {wifi_status}\n")

time_since_update = 0
update_time = time.time()

# Main loop to read data, display, and send to Sensor.Community
while True:
    try:
        values = read_values()
        time_since_update = time.time() - update_time
        if time_since_update > 145:
            logging.info(values)
            update_time = time.time()
            if send_to_sensorcommunity(values, id):
                logging.info("Sensor.Community Response: OK")
            else:
                logging.warning("Sensor.Community Response: Failed")
        display_status()
    except Exception as e:
        logging.warning(f"Main Loop Exception: {e}")
