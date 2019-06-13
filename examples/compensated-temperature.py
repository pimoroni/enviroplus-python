#!/usr/bin/env python

import time
from bme280 import BME280
from subprocess import PIPE, Popen

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

print("""compensated-temperature.py - Use the CPU temperature to compensate temperature
readings from the BME280 sensor. Method adapted from Initial State's Enviro pHAT
review: https://medium.com/@InitialState/tutorial-review-enviro-phat-for-raspberry-pi-4cd6d8c63441

Press Ctrl+C to exit!

""")

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

factor = 0.8

while True:
    cpu_temp = get_cpu_temperature()
    raw_temp = bme280.get_temperature()
    comp_temp = raw_temp - ((cpu_temp - raw_temp) / factor)
    print("Compensated temperature: {:05.2f} *C".format(comp_temp))
    time.sleep(1.0)
