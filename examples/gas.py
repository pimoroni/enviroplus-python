#!/usr/bin/env python

import time
from envirophatplus import gas


print("""gas.py - Print readings from the MICS6812 Gas sensor.

Press Ctrl+C to exit!
        
""")

try:
    while True:
        readings = gas.read_all()
        print(readings)
        time.sleep(1.0)
except KeyboardInterrupt:
    pass
