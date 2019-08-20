#!/usr/bin/env python

import time
from enviroplus import gas
import logging

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""adc.py - Print readings from the MICS6814 Gas sensor.

Press Ctrl+C to exit!

""")

gas.enable_adc()
gas.set_adc_gain(4.096)

try:
    while True:
        readings = gas.read_all()
        logging.info(readings)
        time.sleep(1.0)
except KeyboardInterrupt:
    pass
