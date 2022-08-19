# Enviro+

Designed for environmental monitoring, Enviro+ lets you measure air quality (pollutant gases and particulates), temperature, pressure, humidity, light, and noise level. Learn more - https://shop.pimoroni.com/products/enviro-plus

[![Build Status](https://travis-ci.com/pimoroni/enviroplus-python.svg?branch=master)](https://travis-ci.com/pimoroni/enviroplus-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/enviroplus-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/enviroplus-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)
[![Python Versions](https://img.shields.io/pypi/pyversions/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)

# Installing

You are best using the "One-line" install method if you want all of the UART serial configuration for the PMS5003 particulate matter sensor to run automatically.

**Note** The code in this repository supports both the Enviro+ and Enviro Mini boards. _The Enviro Mini board does not have the Gas sensor or the breakout for the PM sensor._

![Enviro Plus pHAT](./Enviro-Plus-pHAT.jpg)
![Enviro Mini pHAT](./Enviro-mini-pHAT.jpg)

:warning: This library now supports Python 3 only, Python 2 is EOL - https://www.python.org/doc/sunset-python-2/

## One-line (Installs from GitHub)

```bash
curl -sSL https://get.pimoroni.com/enviroplus | bash
```

**Note** report issues with one-line installer here: https://github.com/pimoroni/get

## Or... Install and configure dependencies from GitHub:

* `git clone https://github.com/pimoroni/enviroplus-python`
* `cd enviroplus-python`
* `sudo ./install.sh`

**Note** Raspbian/Raspberry Pi OS Lite users may first need to install git: `sudo apt install git`

## Or... Install from PyPi and configure manually:

* Run `sudo python3 -m pip install enviroplus`

**Note** this will not perform any of the required configuration changes on your Pi, you may additionally need to:

* Enable i2c: `raspi-config nonint do_i2c 0`
* Enable SPI: `raspi-config nonint do_spi 0`

And if you're using a PMS5003 sensor you will need to:

* Enable serial: `raspi-config nonint set_config_var enable_uart 1 /boot/config.txt`
* Disable serial terminal: `sudo raspi-config nonint do_serial 1`
* Add `dtoverlay=pi3-miniuart-bt` to your `/boot/config.txt`

And install additional dependencies:

```bash
sudo apt install python3-numpy python3-smbus python3-pil python3-setuptools
```

## Alternate Software & User Projects

* Enviro Plus Dashboard - https://gitlab.com/dedSyn4ps3/enviroplus-dashboard - A React-based web dashboard for viewing sensor data
* Enviro+ Example Projects - https://gitlab.com/dedSyn4ps3/enviroplus-python-projects - Includes original examples plus code to stream to Adafruit IO (more projects coming soon)
* enviro monitor - https://github.com/roscoe81/enviro-monitor
* mqtt-all - https://github.com/robmarkcole/rpi-enviro-mqtt - now upstream: [see examples/mqtt-all.py](examples/mqtt-all.py)
* enviroplus_exporter - https://github.com/tijmenvandenbrink/enviroplus_exporter - Prometheus exporter (with added support for Luftdaten and InfluxDB Cloud)
* homekit-enviroplus - https://github.com/sighmon/homekit-enviroplus - An Apple HomeKit accessory for the Pimoroni Enviro+
* go-enviroplus - https://github.com/rubiojr/go-enviroplus - Go modules to read Enviro+ sensors
* homebridge-enviroplus - https://github.com/mhawkshaw/homebridge-enviroplus - a Homebridge plugin to add the Enviro+ to HomeKit via Homebridge
* Enviro Plus Web - https://gitlab.com/idotj/enviroplusweb - Simple Flask application serves a web page with the current sensor readings and a graph over a specified time period

## Help & Support

* GPIO Pinout - https://pinout.xyz/pinout/enviro_plus
* Support forums - https://forums.pimoroni.com/c/support
* Discord - https://discord.gg/hr93ByC
