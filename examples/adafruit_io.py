"""
This code comes directly from Adafruit's learning guide on building an environmental monitor
either with a Raspberry Pi, or Feather. I wanted to see if I could use it, minus a few bits and bobs,
to regularly send enviro-data using my Pimoroni Enviro+ Pi-HAT to my AIO dashboard all while running another
python program provided by Pimoroni to display all the values nicely on it's OLED display.

I kept having conflicts every time I tried to incorporate AIO into their code, so I decided to use this base code
along side it to resolve the conflicts. Just add both the 'weather-and-light.py' and this file to your /etc/rc.local
boot file, and you will be able to see the values both locally as well as your Adafruit IO dashboard!

                                                                                          ~dedSyn4ps3

"""

"""
'environmental_monitor.py'
===============================================================================
Example of sending I2C sensor data
from multiple sensors to Adafruit IO.
 
Tutorial Link: https://learn.adafruit.com/adafruit-io-air-quality-monitor
 
Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!
 
Author(s): Brent Rubell for Adafruit Industries
Copyright (c) 2018 Adafruit Industries
Licensed under the MIT license.
All text above must be included in any redistribution.
 
Dependencies:
    - Adafruit_Blinka (CircuitPython, on Pi.)
        (https://github.com/adafruit/Adafruit_Blinka)

    - Adafruit_CircuitPython_BME280.
        (https://github.com/adafruit/Adafruit_CircuitPython_BME280)
"""


#!/usr/bin/env python3

# Import standard python modules
import time

# import Adafruit Blinka
import board
import busio
import adafruit_bme280

# import Adafruit IO REST client
from Adafruit_IO import Client, Feed, RequestError

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

# Create an instance of the REST client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we already have the feeds, assign them.

    temperature_feed = aio.feeds('temperature')
    humidity_feed = aio.feeds('humidity')
    pressure_feed = aio.feeds('pressure')
    altitude_feed = aio.feeds('altitude')

except RequestError: # if we don't, create and assign them.

    temperature_feed = aio.create_feed(Feed(name='temperature'))
    humidity_feed = aio.create_feed(Feed(name='humidity'))
    pressure_feed = aio.create_feed(Feed(name='pressure'))
    altitude_feed = aio.create_feed(Feed(name='altitude'))

# Create busio I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Create BME280 object.
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.sea_level_pressure = 1013.25


while True:

    try:

        # Read BME280
        temp_data = bme280.temperature
        temp_data = int(temp_data) * 1.8 + 22          #The 22 is just a slight correction to offset heat dissipation from the pi's hardware
        humid_data = bme280.humidity
        pressure_data = bme280.pressure
        alt_data = bme280.altitude

        # Send BME280 Data
        
        aio.send(temperature_feed.key, temp_data)
        aio.send(humidity_feed.key, int(humid_data))

        time.sleep(2)
        
        aio.send(pressure_feed.key, int(pressure_data))
        aio.send(altitude_feed.key, int(alt_data))

        # Avoid timeout from aio
        time.sleep(30)

    except Exception:

        break