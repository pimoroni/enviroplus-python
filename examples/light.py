#!/usr/bin/env python3

import time
import logging
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559


logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""light.py - Print readings from the LTR559 Light & Proximity sensor.

Press Ctrl+C to exit!

""")

try:
    while True:
        lux = ltr559.get_lux()
        prox = ltr559.get_proximity()
        logging.info("""Light: {:05.02f} Lux
Proximity: {:05.02f}
""".format(lux, prox))
        time.sleep(1.0)
except KeyboardInterrupt:
    pass
