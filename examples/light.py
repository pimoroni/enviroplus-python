#!/usr/bin/env python

import time
import ltr559


print("""light.py - Print readings from the LTR559 Light & Proximity sensor.

Press Ctrl+C to exit!

""")

try:
    while True:
        lux = ltr559.get_lux()
        prox = ltr559.get_proximity()
        print("""Light: {:05.02f} Lux
Proximity: {:05.02f}
""".format(lux, prox))
        time.sleep(1.0)
except KeyboardInterrupt:
    pass
