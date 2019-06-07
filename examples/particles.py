#!/usr/bin/env python

import time
from pms5003 import PMS5003


print("""particles.py - Print readings from the PM5003 Particle sensor.

Press Ctrl+C to exit!
        
""")

pms5003 = PMS5003()
time.sleep(1.0)


try:
    while True:
        readings = pms5003.read()
        print(readings)
        time.sleep(1.0)
except KeyboardInterrupt:
    pass
