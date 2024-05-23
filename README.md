# Enviro+

Designed for environmental monitoring, Enviro+ lets you measure air quality (pollutant gases and particulates), temperature, pressure, humidity, light, and noise level. Learn more - https://shop.pimoroni.com/products/enviro-plus

[![Build Status](https://img.shields.io/github/actions/workflow/status/pimoroni/enviroplus-python/test.yml?branch=main)](https://github.com/pimoroni/enviroplus-python/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/enviroplus-python/badge.svg?branch=main)](https://coveralls.io/github/pimoroni/enviroplus-python?branch=main)
[![PyPi Package](https://img.shields.io/pypi/v/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)
[![Python Versions](https://img.shields.io/pypi/pyversions/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)

# Installing

**Note** The code in this repository supports both the Enviro+ and Enviro Mini boards. _The Enviro Mini board does not have the Gas sensor or the breakout for the PM sensor._

![Enviro Plus pHAT](https://raw.githubusercontent.com/pimoroni/enviroplus-python/main/Enviro-Plus-pHAT.jpg)
![Enviro Mini pHAT](https://raw.githubusercontent.com/pimoroni/enviroplus-python/main/Enviro-mini-pHAT.jpg)

:warning: This library now supports Python 3 only, Python 2 is EOL - https://www.python.org/doc/sunset-python-2/

## Install and configure dependencies from GitHub:

* `git clone https://github.com/pimoroni/enviroplus-python`
* `cd enviroplus-python`
* `./install.sh`

**Note** Libraries will be installed in the "pimoroni" virtual environment, you will need to activate it to run examples:

```
source ~/.virtualenvs/pimoroni/bin/activate
```

**Note** Raspbian/Raspberry Pi OS Lite users may first need to install git: `sudo apt install git`

## Or... Install from PyPi and configure manually:

* `python3 -m venv --system-site-packages $HOME/.virtualenvs/pimoroni`
* Run `python3 -m pip install enviroplus`

And install additional dependencies:

```bash
sudo apt install python3-numpy python3-smbus python3-pil python3-setuptools
```

**Note** this will not perform any of the required configuration changes on your Pi, you may additionally need to:

* Enable i2c: `raspi-config nonint do_i2c 0`
* Enable SPI: `raspi-config nonint do_spi 0`

And if you're using a PMS5003 sensor you will need to:

### Bookworm

* Enable serial: `raspi-config nonint do_serial_hw 0`
* Disable serial terminal: `raspi-config nonint do_serial_cons 1`
* Add `dtoverlay=pi3-miniuart-bt` to your `/boot/firmware/config.txt`

### Bullseye

* Enable serial: `raspi-config nonint set_config_var enable_uart 1 /boot/config.txt`
* Disable serial terminal: `sudo raspi-config nonint do_serial 1`
* Add `dtoverlay=pi3-miniuart-bt` to your `/boot/config.txt`

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
