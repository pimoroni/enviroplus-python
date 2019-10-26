# Enviro+

Designed for environmental monitoring, Enviro+ lets you measure air quality (pollutant gases and particulates), temperature, pressure, humidity, light, and noise level. Learn more - https://shop.pimoroni.com/products/enviro-plus

[![Build Status](https://travis-ci.com/pimoroni/enviroplus-python.svg?branch=master)](https://travis-ci.com/pimoroni/enviroplus-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/enviroplus-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/enviroplus-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)
[![Python Versions](https://img.shields.io/pypi/pyversions/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)

# Installing

You're best using the "One-line" install method if you want all of the UART serial configuration for the PMS5003 particulate matter sensor to run automatically.

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

* Run `sudo pip install enviroplus`

**Note** this wont perform any of the required configuration changes on your Pi, you may additionally need to:

* Enable i2c: `raspi-config nonint do_i2c 0`
* Enable SPI: `raspi-config nonint do_spi 0`

And if you're using a PMS5003 sensor you will need to:

* Enable serial: `raspi-config nonint set_config_var enable_uart 1 /boot/config.txt`
* Disable serial terminal: `sudo raspi-config nonint do_serial 1`
* Add `dtoverlay=pi3-miniuart-bt` to your `/boot/config.txt`
* Add `core_freq=250` to your `/boot/config.txt`
* Add `core_freq_min=250` to your `/boot/config.txt`

And install additional dependencies:

```
sudo apt install python-numpy python-smbus python-pil python-setuptools
```

## Help & Support

* GPIO Pinout - https://pinout.xyz/pinout/enviro_plus
* Support forums - http://forums.pimoroni.com/c/support
* Discord - https://discord.gg/hr93ByC
