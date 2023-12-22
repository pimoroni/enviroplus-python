#!/usr/bin/env python3
# -*- coding: utf-8 -*-

f"Sorry! This program requires Python >= 3.6 😅. Run with \"python3 check-install.py\""

CONFIG_FILE = "/boot/config.txt"

print("""Checking Enviro+ install, please wait...""")

errors = 0
check_apt = False

try:
    import apt
    check_apt = True
except ImportError:
    print("⚠️  Could not import \"apt\". Unable to verify system dependencies.")


apt_deps = {
    "python3",
    "python3-pip",
    "python3-numpy",
    "python3-smbus",
    "python3-pil",
    "python3-cffi",
    "python3-spidev",
    "python3-rpi.gpio",
    "libportaudio2"
}

deps = {
    "bme280": None,
    "pms5003": None,
    "ltr559": None,
    "ST7735": None,
    "ads1015": "0.0.7",
    "fonts": None,
    "font_roboto": None,
    "astral": None,
    "pytz": None,
    "sounddevice": None,
    "paho.mqtt": None
}

config = {
    "dtparam=i2c_arm=on",
    "dtparam=spi=on",
    "dtoverlay=adau7002-simple",
    "dtoverlay=pi3-miniuart-bt",
    "enable_uart=1"
}

if check_apt:
    print("\nSystem dependencies...")
    print("  Retrieving cache...")
    cache = apt.Cache()

    for dep in apt_deps:
        installed = False
        print(f"  Checking for {dep}".ljust(35), end="")
        try:
            installed = cache[dep].is_installed
        except KeyError:
            pass

        if installed:
            print("✅")
        else:
            print("⚠️  Missing!")
            errors += 1

print("\nPython dependencies...")

for dep, version in deps.items():
    print(f"  Checking for {dep}".ljust(35), end="")
    try:
        __import__(dep)
        print("✅")
    except ImportError:
        print("⚠️  Missing!")
        errors += 1

print("\nSystem config...")

config_txt = open(CONFIG_FILE, "r").read().split("\n")

def check_config(line):
    global errors
    print(f"  Checking for {line} in {CONFIG_FILE}: ", end="")
    for cline in config_txt:
        if cline.startswith(line):
            print("✅")
            return
    print("⚠️  Missing!")
    errors += 1

for line in config:
    check_config(line)

if errors > 0:
    print("\n⚠️   Config errors were found! Something might be awry.")
else:
    print("\n✅  Looks good from here!")

print("\nHave you?")
print("  • Rebooted after installing")
print("  • Made sure to run examples with \"python3\"")
print("  • Checked for any errors when running \"sudo ./install.sh\"")
