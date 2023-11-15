#!/usr/bin/env python3

import logging
import time

from bme280 import BME280
from smbus2 import SMBus

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")

logging.info("""weather.py - Print readings from the BME280 weather sensor.

Press Ctrl+C to exit!

""")

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

while True:
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    logging.info(f"""Temperature: {temperature:05.2f} °C
Pressure: {pressure:05.2f} hPa
Relative humidity: {humidity:05.2f} %
""")
    time.sleep(1)
