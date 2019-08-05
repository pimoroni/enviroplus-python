#!/usr/bin/env python

import time
from pms5003 import PMS5003, ReadTimeoutError
import logging

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""particulates.py - Print readings from the PMS5003 particulate sensor.

Press Ctrl+C to exit!

""")

pms5003 = PMS5003()
time.sleep(1.0)

try:
    while True:
        try:
            readings = pms5003.read()
            logging.info(readings)
            time.sleep(1.0)
        except ReadTimeoutError:
            pms5003 = PMS5003()
except KeyboardInterrupt:
    pass
