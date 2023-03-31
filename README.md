# [Fork of Enviro+ Python library by Pimoroni](https://github.com/pimoroni/enviroplus-python)

[![Enviro+ Python library tests](https://github.com/argtus/enviroplus-python/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/argtus/enviroplus-python/actions/workflows/test.yml)
[![Snyk Security Scan](https://github.com/argtus/enviroplus-python/actions/workflows/snyk.yml/badge.svg?branch=main)](https://github.com/argtus/enviroplus-python/actions/workflows/snyk.yml)
[![Secret Scan](https://github.com/argtus/enviroplus-python/actions/workflows/github-code-scanning/codeql/badge.svg?branch=main)](https://github.com/argtus/enviroplus-python/actions/workflows/github-code-scanning/codeql)
[![Coveralls Test Status](https://coveralls.io/repos/github/argtus/enviroplus-python/badge.svg?branch=main)](https://coveralls.io/github/argtus/enviroplus-python?branch=main)
[![PyPi Package](https://img.shields.io/pypi/v/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)
[![Python Versions](https://img.shields.io/pypi/pyversions/enviroplus.svg)](https://pypi.python.org/pypi/enviroplus)

## Functional Changes

I've done changes by adding code relevant to plant growth monitoring, which is conveniently placed under [modified_code](https://github.com/argtus/enviroplus-python/tree/master/modified_code).

### Lux to DLI conversion

The LTR559 sensor reports its readings as Lux, which is a unit of measurement for illuminance defined as one lumen per square meter (lm/m²). The Lux measurements take into account the sensitivity of the human eye to different wavelengths of light as not all are equal to the human eye. Two light sources with the same number of lumens may appear to have different brightness to the human eye if they emit different colors of light. It doesn't measure well how the amount of light impacts plants growth and development.

Daily Light Integral (DLI) on the other hand is a measure of the total amount of photosynthetically active radiation (PAR) that a plant receives over the course of a day. It is expressed as the number of moles of photons per square meter per day (mol/m²/d) and is commonly used in horticulture to quantify the amount of light that plants receive. The DLI required by a plant can vary depending on the species and growth stage, and it is important to provide the appropriate amount of light to optimize plant growth and productivity.

Lux can be converted to DLI though by first converting it to PPFD and then myliplying it with the amount of hours light is on ie. photoperiod and finally dividing the result by one million.

For the PFFD conversion I've assumed that the light used is a commonly available LED strip meant for growing plants. Those have white, blue and red LEDs, which are are more efficient for photosynthesis. This kind of a light has a factor 0.025 when doing the Lux conversion.
$$lx * 0.025 = PPFD(μmol/m²/s)$$

Then to PFFD can then be converted to DLI. I've assumed the photoperiod is 16 hours:
$$(PPFD * 60s * 60m * 16h) / 1 000 000 = DLI (mol/m²/d)$$

## Codebase Maintenance

I've also changed GitHub Actions and more specifically Enviro+ Python library tests to be compatible with Python `latest` and the latest versions of the dependencies. In addition, I've also added Dependabot to pump the GitHub Actions and `pip` dependencies as well as enabled CodeQL and Snyk security scans.

<details>
  <summary>Original README</summary>

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

- `git clone https://github.com/pimoroni/enviroplus-python`
- `cd enviroplus-python`
- `./install.sh`

**Note** Libraries will be installed in the "pimoroni" virtual environment, you will need to activate it to run examples:

```
source ~/.virtualenvs/pimoroni/bin/activate
```

**Note** Raspbian/Raspberry Pi OS Lite users may first need to install git: `sudo apt install git`

## Or... Install from PyPi and configure manually:

- `python3 -m venv --system-site-packages $HOME/.virtualenvs/pimoroni`
- Run `python3 -m pip install enviroplus`

And install additional dependencies:

```bash
sudo apt install python3-numpy python3-smbus python3-pil python3-setuptools
```

**Note** this will not perform any of the required configuration changes on your Pi, you may additionally need to:

- Enable i2c: `raspi-config nonint do_i2c 0`
- Enable SPI: `raspi-config nonint do_spi 0`

And if you're using a PMS5003 sensor you will need to:

### Bookworm

- Enable serial: `raspi-config nonint do_serial_hw 0`
- Disable serial terminal: `raspi-config nonint do_serial_cons 1`
- Add `dtoverlay=pi3-miniuart-bt` to your `/boot/config.txt`

### Bullseye

- Enable serial: `raspi-config nonint set_config_var enable_uart 1 /boot/config.txt`
- Disable serial terminal: `sudo raspi-config nonint do_serial 1`
- Add `dtoverlay=pi3-miniuart-bt` to your `/boot/config.txt`

## Alternate Software & User Projects

- Enviro Plus Dashboard - https://gitlab.com/dedSyn4ps3/enviroplus-dashboard - A React-based web dashboard for viewing sensor data
- Enviro+ Example Projects - https://gitlab.com/dedSyn4ps3/enviroplus-python-projects - Includes original examples plus code to stream to Adafruit IO (more projects coming soon)
- enviro monitor - https://github.com/roscoe81/enviro-monitor
- mqtt-all - https://github.com/robmarkcole/rpi-enviro-mqtt - now upstream: [see examples/mqtt-all.py](examples/mqtt-all.py)
- enviroplus_exporter - https://github.com/tijmenvandenbrink/enviroplus_exporter - Prometheus exporter (with added support for Luftdaten and InfluxDB Cloud)
- homekit-enviroplus - https://github.com/sighmon/homekit-enviroplus - An Apple HomeKit accessory for the Pimoroni Enviro+
- go-enviroplus - https://github.com/rubiojr/go-enviroplus - Go modules to read Enviro+ sensors
- homebridge-enviroplus - https://github.com/mhawkshaw/homebridge-enviroplus - a Homebridge plugin to add the Enviro+ to HomeKit via Homebridge
- Enviro Plus Web - https://gitlab.com/idotj/enviroplusweb - Simple Flask application serves a web page with the current sensor readings and a graph over a specified time period

## Help & Support

- GPIO Pinout - https://pinout.xyz/pinout/enviro_plus
- Support forums - https://forums.pimoroni.com/c/support
- Discord - https://discord.gg/hr93ByC

</details>
