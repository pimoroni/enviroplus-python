# Enviro+

Designed for environmental monitoring, Enviro+ lets you measure air quality (pollutant gases and particulates), temperature, pressure, humidity, light, and noise level. Learn more - https://shop.pimoroni.com/products/enviro-plus


[![Build Status](https://travis-ci.com/pimoroni/enviroplus-python.svg?branch=master)](https://travis-ci.com/pimoroni/enviroplus-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/enviroplus-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/enviroplus-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)
[![Python Versions](https://img.shields.io/pypi/pyversions/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)

# Installing

You're best using the "One-line" install method if you want all of the UART serial configuration for the PMS5003 particulate matter sensor to run automatically.

**Note** The code in this repository supports both the Enviro+ and Enviro Mini boards. _The Enviro Mini board does not have the Gas sensor or the breakout for the PM sensor._

![Enviro Plus pHAT](./Enviro-Plus-pHAT.jpg)
![Enviro Mini pHAT](./Enviro-mini-pHAT.jpg)

:warning: This library now supports Python 3 only, Python 2 is EOL - https://www.python.org/doc/sunset-python-2/

## One-line (Installs from GitHub)

```
curl -sSL https://get.pimoroni.com/enviroplus | bash
```

**Note** report issues with one-line installer here: https://github.com/pimoroni/get

## Or... Install and configure dependencies from GitHub:

* `git clone https://github.com/pimoroni/enviroplus-python`
* `cd enviroplus-python`
* `sudo ./install.sh`

**Note** Raspbian Lite users may first need to install git: `sudo apt install git`

## Or... Install from PyPi and configure manually:

* Run `sudo python3 -m pip install enviroplus`

**Note** this wont perform any of the required configuration changes on your Pi, you may additionally need to:

* Enable i2c: `raspi-config nonint do_i2c 0`
* Enable SPI: `raspi-config nonint do_spi 0`

And if you're using a PMS5003 sensor you will need to:

* Enable serial: `raspi-config nonint set_config_var enable_uart 1 /boot/config.txt`
* Disable serial terminal: `sudo raspi-config nonint do_serial 1`
* Add `dtoverlay=pi3-miniuart-bt` to your `/boot/config.txt`

And install additional dependencies:

```
sudo apt install python3-numpy python3-smbus python3-pil python3-setuptools
```

## Alternate Software & User Projects

* enviro monitor - https://github.com/roscoe81/enviro-monitor
* mqtt-all - https://github.com/robmarkcole/rpi-enviro-mqtt - now upstream: [see examples/mqtt-all.py](examples/mqtt-all.py)
* adafruit_io.py - https://github.com/dedSyn4ps3/enviroplus-python/blob/master/examples/adafruit_io.py - uses Adafruit Blinka and BME280 libraries to publish to Adafruit IO
* enviroplus_exporter - https://github.com/tijmenvandenbrink/enviroplus_exporter - Prometheus exporter (with added support for Luftdaten and InfluxDB Cloud)
* homekit-enviroplus - https://github.com/sighmon/homekit-enviroplus - An Apple HomeKit accessory for the Pimoroni Enviro+
* go-enviroplus - https://github.com/rubiojr/go-enviroplus - Go modules to read Enviro+ sensors

## Help & Support

* GPIO Pinout - https://pinout.xyz/pinout/enviro_plus
* Support forums - http://forums.pimoroni.com/c/support
* Discord - https://discord.gg/hr93ByC

# Changelog
0.0.6
-----

* Fix noise by specifying adau7002 device

0.0.5
-----

* Drop Python 2.x support
* Add "available()" method for gas sensor

0.0.4
-----

* Add support for ads1015 >= v0.0.7 (ADS1115 ADCs)
* Packaging tweaks

0.0.3
-----

* Fix "self.noise_floor" bug in get_noise_profile

0.0.2
-----

* Add support for extra ADC channel in Gas
* Handle breaking change in new ltr559 library
* Add Noise functionality

0.0.1
-----

* Initial Release
